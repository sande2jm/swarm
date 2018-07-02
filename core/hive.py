import boto3
import random
import json
from subprocess import call
class Hive():
	def __init__(self, layout):
		self.s3 = boto3.resource('s3')
		self.ec2 = boto3.resource('ec2')
		self.layout = layout
		self.instructions = {}
		self.swarm = []

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

	def connect(self):
		filters = [{'Name': 'tag:Name', 'Values': ['Swarm']}]
		for x in self.ec2.instances.filter(Filters=filters):
			if x.state['Name'] == 'running':
				self.swarm.append(x)
		print(self.swarm)
