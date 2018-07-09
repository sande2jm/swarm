import boto3
from subprocess import call
import sys

class Swarm3(object):
	def __init__(self,size=1, config=None):

		self.ec2 = boto3.resource('ec2', 'us-east-1')
		self.size = size
		self.config = config
		self.locusts = []
		self.existing = 0

	def init(self,dependencies=None):
		"""Python bare minimum pre-config enviornment"""

		cmds = ["#!/bin/bash", "sudo apt-get update","sudo apt-get install -y python3-pip","pip3 install boto3"]
		cmds += dependencies
		cmds = "".join(list(map(lambda x: str(x) + "\n", cmds)))
		self.config['init'] = cmds

	def head_count(self):
		"""Count number of already available locusts."""	
		filters = [{'Name': 'tag:Name', 'Values': [self.config['name']]}]
		for x in self.ec2.instances.filter(Filters=filters):
			if x and x.state['Name'] == 'running':
				self.existing += 1


	def describe(self):
		print("Swarm Created")
		print('size: ',self.size)
		print('name: ', self.config['name'])
		print('type: ', self.config['type'])
		print(self.size - self.existing, "new locusts created")
		print()
				

	def populate(self):
		"""Spawn the required number of locusts in the image of config"""
		self.head_count()
		if self.existing < self.size:
			self.locusts = self.ec2.create_instances(
				TagSpecifications=
				[{'ResourceType': 'instance','Tags': [{'Key': 'Name','Value': self.config['name']},]},],
				Placement={'AvailabilityZone': self.config['region'],},
				ImageId=self.config['ami'],
				InstanceType=self.config['type'],
				MinCount=1,
				MaxCount=self.size - self.existing,
				Monitoring={'Enabled': True},
				KeyName=self.config['key'],
				SecurityGroupIds=self.config['securityId'],
				SecurityGroups=self.config['securityGroup'],
				UserData=self.config['init'],
				IamInstanceProfile={
			    'Arn': self.config['role']}
			    )



