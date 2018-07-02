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

	def create_instructions(self,swarm,target,_range):
		start,end = _range
		for x in swarm:
			self.layout[target] = random.uniform(start,end)
			self.instructions[x.id] = self.layout

	def inject_instructions(self):
		with open('instructions.txt', 'w') as outfile:
			json.dump(self.instructions, outfile)
		self.s3.meta.client.upload_file('instructions.txt', 'swarm-instructions', 'instructions.txt')
		call(['rm', 'instructions.txt'])

	def broadcast(self, signal):
		pass
