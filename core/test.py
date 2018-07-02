from swarm import Swarm
from hive import Hive

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

#instances = sw.create()
# hive = Hive({'steps': 1, 
# 			'batch_size': 1, 
# 			'epochs': 1, 
# 			'learning_rate': 1, 
# 			'drop_r': 1})
# hive.connect()
# hive.create_instructions("learning_rate", (0.0001, 0.01))
# hive.create_instructions("learning_rate", (0.0001, 0.01), swarm=instances)
# hive.inject_instructions()


