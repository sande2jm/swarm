from context import core
from core import Swarm
import unittest
class SwarmTest(unittest.TestCase):
	def testinit(self):
		sw = Swarm(size=16)
		self.assertEqual(sw.instance,{'ami': 'ami-a4dc46db', 'init': '', 'role': 'arn:aws:iam::400029180276:instance-profile/s3Full_Access', 'type': 't2.micro', 'securityId': ['sg-eade92a1'], 'key': 'DLNAkey', 'securityGroup': ['SSH']})
		self.assertEqual(sw.code, {})
		self.assertEqual(sw.args, {'steps': 1, 'batch_size': 1, 'epochs': 1, 'lr': 1, 'drop_r': 1})
		sw = None

	def testSetCode(self):
		sw = Swarm(size=16)
		sw.set_code("launch.py", "https://github.com/sande2jm/ec2.git")
		self.assertEqual(sw.code['launch'],"launch.py")
		self.assertEqual(sw.code['github'],"https://github.com/sande2jm/ec2.git")
		sw = None
	def testMultipleSwarm(self):
		sw = Swarm(16)
		sw1 =Swarm(2)
		self.assertNotEqual(sw.size, sw1.size)

	def testCreate(self):
		sw = Swarm(2)
		init = """#!/bin/bash
		git clone https://github.com/sande2jm/ec2.git /home/ubuntu/ec2
		sudo apt-get update
		sudo apt-get install -y python3-pip
		pip3 install boto3"""
		role = 'arn:aws:iam::400029180276:instance-profile/s3Full_Access'
		ami = "ami-a4dc46db"
		_type = "t2.micro"
		securityId = ['sg-eade92a1']
		securityGroup = ['SSH']
		key = 'DLNAkey'

		sw.set_instance(key, init=init, role=role, securityId=securityId, securityGroup=securityGroup, ami=ami, _type=_type)

		instances = sw.create()
		hive.create_instructions(instances,"learning_rate", [])
		





role = , ami, _type, securityId, key, securityGroup

if __name__ == '__main__':
	unittest.main()