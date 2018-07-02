import boto3
import random
import json
from subprocess import call
import botocore
import paramiko
import time

class Hive():
	def __init__(self, layout, path):
		self.s3 = boto3.resource('s3')
		self.ec2 = boto3.resource('ec2')
		self.layout = layout
		self.instructions = {}
		self.swarm = []
		self.path = path

	def create_instructions(self,target,_range,swarm=None):
		start,end = _range
		if swarm: self.swarm = swarm
		for x in self.swarm:
			self.layout[target] = random.uniform(start,end)
			self.instructions[x.id] = self.layout

	def inject_instructions(self):
		with open('instructions.txt', 'w') as outfile:
			json.dump(self.instructions, outfile)
		self.s3.meta.client.upload_file('instructions.txt', 'swarm-instructions', 'instructions.txt')
		call(['rm', 'instructions.txt'])

	def broadcast(self, signal):
		pass

	def wait_for_swarm(self):
		count = 0
		while count < len(self.swarm):
			count = 0
			for i,x in enumerate(self.swarm):
				self.swarm[i] = self.ec2.Instance(x.id)
				print(x.id[15:], x.state['Name'])
				if x.state['Name'] == 'running':
					count += 1
			time.sleep(.3)


	def connect(self): 
		filters = [{'Name': 'tag:Name', 'Values': ['Swarm']}]
		for x in self.ec2.instances.filter(Filters=filters):
			if x.state['Name'] == 'running':
				self.swarm.append(x)
		print(self.swarm)
