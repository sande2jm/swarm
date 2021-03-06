from context import core
from core import Swarm3
from core import Hive3
import boto3
import mpu
import yaml

with open("swarm/test/worker_yamls/swarm_digit_recognizer.yaml", 'r') as stream:
	config = yaml.load(stream)

direc = config['worker_direc_name']
github_clone = 'git clone https://github.com/'+ config['github_account'] + '/' + direc + '.git'
rm_repo = 'sudo rm -r ' + direc
launch = config['launch']
aws_services_info = config['aws_services_info']


ec2_config = config['ec2_config']

statics = config['statics']
variables = config['variables']
splits = config['splits']

# for k,v in config.items():
# 	print(k, v)
s3_info = aws_services_info['s3']
s3 = boto3.resource('s3')

# s3.Bucket(s3_info['bucket']).download_file(splits['json'], 'swarm/test/'+splits['json'])

size = ec2_config['size']
swarm_name = ec2_config['name']
swarm = Swarm3(size=size,config=ec2_config)

swarm.init(dependencies=ec2_config['dependencies'])
swarm.populate()
swarm.describe()

# json_input = mpu.io.read('swarm/test/'+splits['json'])
# splits =({'json':json_input['images']})
# splits = ({'images':json_input['images']})
# variables = ({'index': ((0,size), 'unique')})
# statics = {}

hive = Hive3(variable=variables, static=statics, split=splits, direc=direc)
hive.gather(size=size,group=swarm_name)
hive.generate_swarm_parameters()
hive.inject_behavior([rm_repo, github_clone])

hive.broadcast('python3 ' + direc + '/' +launch)
print("Waiting For Leader... ")
hive.monitor()
print('Work Completed')

