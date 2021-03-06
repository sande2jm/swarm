import boto3
import random
import json
from subprocess import call
import botocore
import paramiko
import time
import random
import mpu.io
from .hive_helper import split_json 
from threading import Thread

class Hive3():
	def __init__(self, variable=None, static=None, split=None, direc = None ):
		self.s3 = boto3.resource('s3', 'us-east-1')
		self.ec2 = boto3.resource('ec2', 'us-east-1')
		self.direc = direc

		self.config = {'variable': variable,
						'static': static,
						'split': split}
		self.swarm = {}
		self.sqs = boto3.resource('sqs', 'us-east-1')
		self.queue = self.sqs.get_queue_by_name(QueueName='swarm.fifo')
		self.reports = {}
		self.client = boto3.client(
		    "sns",region_name="us-east-1")
		self.t1 = Thread(target=self.user_input, daemon=True)
		self.t1.start()
		self.state = ['running']

	def monitor(self):
		start = time.clock()
		d = set()
		while len(d) < len(self.swarm):
			for x in self.queue.receive_messages(MaxNumberOfMessages=10):
				message = json.loads(x.body)
				if message['message'] == 'working':
					self.reports.update({message['id']:(message['progress'], message['state'])})
				elif message['message']=='complete':
					self.reports.update({message['id']:(1.0, message['state'])})
					d.add(message['id'])

				x.delete()
			#self.display()
		end = time.clock()
		print(end-start)

		# Send your sms message.
		self.client.publish(
		    PhoneNumber="+17033807996",
		    Message="Swarm Done"
		)
	def user_input(self):
		while True:
			response = input()
			if response == 'show':
				self.display()
			else:
				if response == 'pause':
					self.state[0] = 'pause'
				elif response == 'start':
					self.state[0] = 'running'
				elif response == 'restart':
					self.state[0] = 'restart'
				elif response == 'exit':
					self.state[0] = 'exit'
				with open('state.txt', 'w') as f:
					f.write(self.state[0])
				for x,params in self.swarm.items():
					state_scp = 'scp -i swarm/DLNAkey.pem state.txt ubuntu@'+ params['public_dns_name']+':' + self.direc + '/'
					call(state_scp.split(" "))

		print("Done")

	def display(self):
		print("Swarm Report")
		for x,v in self.reports.items():
			print(x,v)
		time.sleep(.5)

	def gather(self,size=0, group=None): 
		while len(self.swarm) < size:
			l = []
			filters = [{'Name': 'tag:Name', 'Values': [group]}]

			for x in self.ec2.instances.filter(Filters=filters):
				if not x: pass
				if x.state['Name'] == 'running':
					self.swarm[x.id] = {'public_dns_name': x.public_dns_name}
					if len(self.swarm) == size: break
			if size < 16: print(list(self.swarm))
			else: print(len(self.swarm))
			time.sleep(.5)

	def generate_swarm_parameters(self):
		
		size = len(self.swarm)
		if len(self.config['split']) > 0:
			splits = split_json(self.config['split']['json'], size)
		i = 0
		for x,params in self.swarm.items():
			if len(self.config['static']) > 0:
				self.generate_static_parameters(params)
			if len(self.config['variable']) > 0:
				self.generate_variable_parameters(params,i)
			if len(self.config['split']) > 0:
				self.generate_split_parameters(params,splits[i],x)
			i += 1

	def generate_variable_parameters(self, params,i):
		for k2,v2 in self.config['variable'].items():
			print(v2)
			a,b, specs = v2
			if specs == 'unique':
				params.update({k2:i})
			elif specs == 'continuous_random':
				params.update({k2:round(random.uniform(a,b),6)})
			elif specs == 'discrete_random':
				params.update({k2:random.randint(a,b)})

	def generate_static_parameters(self,params):
		params.update(self.config['static'])

	def generate_split_parameters(self,params,split,x):
		for k3,data in self.config['split'].items():
			file_name = x[-4:]+ "_" +k3 +".json"
			size = len(self.swarm)
			n = int(len(data)/size)
			#create files from split data in 
			mpu.io.write(file_name, split)					
			params.update({k3:file_name})

	def inject_parameters(self):
		"""Upload the instructions to AWS S3"""
		print(list(self.swarm.values())[0])
		if len(list(self.swarm.values())[0]) > 1:
			with open('parameters.txt', 'w') as outfile:
				json.dump(self.swarm, outfile)
			self.s3.meta.client.upload_file('parameters.txt', 'swarm-instructions', 'parameters.txt')
			call(['rm', 'parameters.txt'])
			for x,params in self.swarm.items():
				file_name = params.get('json')
				if file_name:
					self.s3.meta.client.upload_file(file_name, 'swarm-instructions', "data/"+file_name)

	def inject_behavior(self, cmds):
		"""Setup all necessary dependencies for locust behavior"""
		self.inject_parameters()
		for cmd in cmds:
			self.inject_code(cmd)

	def inject_code(self, cmd):
		"""Control version of github repository on each x"""
		
		repeat = True
		while repeat:
			repeat = False	
			for x,params in self.swarm.items():
				print(x, cmd)
				if not self.connect_ssh(params['public_dns_name'],cmd):
					repeat = True
				time.sleep(.2)			

	def connect_ssh(self,public_dns, cmd):
		try:
			key = paramiko.RSAKey.from_private_key_file("swarm/DLNAkey.pem")
			client = paramiko.SSHClient()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			client.connect(hostname=public_dns, username="ubuntu", pkey=key)
			stdin, stdout, stderr = client.exec_command(cmd)
			print("Available ")
			ret = True
		except Exception as e:
			print('Unavailable, ', e)
			ret = False
		return ret


	def broadcast(self, cmd):
		finished = set()
		remaining = list(self.swarm)
		size = 0
		while len(finished) < len(remaining):
			for x in self.queue.receive_messages(WaitTimeSeconds=2, MaxNumberOfMessages=10):
				message = json.loads(x.body)
				if message['message'] == 'launched':
					finished.add(message['id'])
				x.delete()
			print(finished)
			progress = '{}/{}'.format(len(finished),len(remaining))
			for k,v in self.swarm.items():
				if not k in finished:
					#print(k, cmd, progress)
					try:
						key = paramiko.RSAKey.from_private_key_file("swarm/DLNAkey.pem")
						client = paramiko.SSHClient()
						client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
						client.connect(hostname=v['public_dns_name'], username="ubuntu", pkey=key, timeout=2)
						stdin, stdout, stderr = client.exec_command(cmd)
					except:
						print('Didnt work') 
			time.sleep(.3)		


