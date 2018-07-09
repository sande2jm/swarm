
from .swarm3 import Swarm3
import boto3
import time
import yaml
import mpu.io


launch = "launch.py"
direc = "swarm"
github_clone = " git clone https://github.com/sande2jm/" + direc + ".git"
rm_repo = 'sudo rm -r ' + direc

with open("command.yaml", 'r') as stream:
	config = yaml.load(stream)

size = 1
swarm_name = config['instance']['name']
swarm = Swarm3(size=size,config=config['instance'])
pip_installs = [
'pip3 install mpu', 
'pip3 install joblib',
'pip3 install pillow', 
'pip3 install numpy',
'pip3 install --upgrade pip',
'sudo python3 -m pip install paramiko']


swarm.init(dependencies=pip_installs)
swarm.populate()
swarm.describe()
print(dir(swarm.locusts[0]))

# hive = Hive3()
#hive.gather(swarm=swarm.locusts)
# hive.generate_swarm_parameters()
# hive.inject_behavior([github_clone])

print("ssh -i DLNAkey.pem ubuntu@" + swarm.locusts[0].public_dns_name)