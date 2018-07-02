import boto3
from subprocess import call
import sys

class Swarm(object):
	def __init__(self,size=1):

		self.ec2 = boto3.resource('ec2')
		self.size = size
		self.instance = {}
		# self.instances = None
		# self.args = {}
		self.code = {}
		self.instance['ami'] = "ami-a4dc46db"
		self.instance['init'] = ""
		self.instance['role'] = 'arn:aws:iam::400029180276:instance-profile/s3Full_Access'
		self.instance['type'] = "t2.micro"
		self.instance['securityId'] = ['sg-eade92a1']
		self.instance['key'] = 'DLNAkey'
		self.instance['securityGroup'] = ['SSH']

	def describe(self):
		return {'instance': self.instance, 'code': self.code}

	def set_code(self,launch_path, github):
		self.code['launch'] = launch_path
		self.code['github'] = github
		str_n = lambda x: str(x) + "\n"
		l = ["#!/bin/bash","git clone https://github.com/sande2jm/aws_worker.git /home/ubuntu/aws_worker","sudo apt-get update","sudo apt-get install -y python3-pip","pip3 install boto3"]
		res = "".join(list(map(str_n, l)))
		self.instance['init'] = res

	def set_instance(self,key,init=None, role=None, ami=None, _type=None, securityId=None, securityGroup=None):
		self.instance['ami'] = ami
		if init: self.instance['init'] = init
		self.instance['role'] = role
		self.instance['type'] = _type
		self.instance['securityId'] = securityId
		self.instance['key'] = key
		self.instance['securityGroup'] = securityGroup

	def create(self):
		return self.ec2.create_instances(
			TagSpecifications=
			[{'ResourceType': 'instance','Tags': [{'Key': 'Name','Value': 'Swarm'},]},],
			ImageId=self.instance['ami'],
			InstanceType=self.instance['type'],
			MinCount=1,
			MaxCount=self.size,
			Monitoring={'Enabled': True},
			KeyName=self.instance['key'],
			SecurityGroupIds=self.instance['securityId'],
			SecurityGroups=self.instance['securityGroup'],
			UserData=self.instance['init'],
			IamInstanceProfile={
		    'Arn': self.instance['role']}
		    )


if __name__ == '__main__':
	s = Swarm(2)
	s.generate_args()

