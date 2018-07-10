
from swarm_leader import Swarm_Leader
import boto3
import time
import yaml
import mpu.io
from subprocess import call


launch = "launch.py"
direc = "swarm"
github_clone = " git clone https://github.com/sande2jm/" + direc + ".git"
rm_repo = 'sudo rm -r ' + direc

with open("swarm_leader.yaml", 'r') as stream:
	config = yaml.load(stream)

size = 1
swarm_name = config['instance']['name']
leader = Swarm_Leader(size=size,config=config['instance'])
pip_installs = [
"#!/bin/bash", 
"sudo apt-get update",
"sudo apt-get install -y python3-pip",
"pip3 install boto3",
'pip3 install mpu', 
'pip3 install joblib',
'pip3 install pillow', 
'pip3 install numpy',
'pip3 install --upgrade pip',
'sudo python3 -m pip install paramiko']


leader.init(dependencies=pip_installs)
leader.populate()
leader.describe()
print(leader.locusts)


leader.gather(size = 1,group='swarm-leader')
print(leader.swarm.items())
leader.inject_code(rm_repo)
leader.inject_code(github_clone)
for x,params in leader.swarm.items():
	scp_pem_key = 'scp -i ../DLNAkey.pem ../DLNAkey.pem ubuntu@'+ params['public_dns_name']+':swarm/'
	call(scp_pem_key.split(" "))
	ssh = "ssh -i ../DLNAkey.pem ubuntu@" + params['public_dns_name']
	call(ssh.split(" "))	
