from context import core
from core import Swarm3
from core import Hive3
import boto3
import time
import yaml
import mpu.io
import boto3

with open("swarm/test/swarm.yaml", 'r') as stream:
	config = yaml.load(stream)


s3 = boto3.resource('s3')
launch = "launch.py"
direc = config['name']
github_clone = " git clone https://github.com/sande2jm/" + direc + ".git"
rm_repo = 'sudo rm -r ' + direc


# s3.Bucket('swarm-instructions').download_file('train.json', 'swarm/test/train.json')

size = 4
swarm_name = config['name']
swarm = Swarm3(size=size,config=config)
pip_installs = [
'pip3 install mpu', 
'pip3 install joblib',
'pip3 install pillow', 
'pip3 install numpy']

swarm.init(dependencies=pip_installs)
swarm.populate()
swarm.describe()

# json_input = mpu.io.read('swarm/test/train.json')
# splits = ({'images':json_input['images']})
# variables = ({'index': ((0,size), 'unique')})

hive = Hive3()
hive.gather(size=size,group=swarm_name)
# hive.generate_swarm_parameters()
# hive.inject_behavior([rm_repo, github_clone])
hive.inject_code(rm_repo)
hive.inject_code(github_clone)
hive.broadcast('python3 worker/launch.py')
print("Waiting For Leader... ")
hive.monitor()



