from context import core
from core import Swarm
from core import Hive

swarm = Swarm(8)
swarm.set_code("aws_worker/launch.py", "https://github.com/sande2jm/aws_worker.git")

role = 'arn:aws:iam::400029180276:instance-profile/s3Full_Access'
ami = "ami-a4dc46db"
_type = "t2.micro"
securityId = ['sg-eade92a1']
securityGroup = ['SSH']
key = 'DLNAkey'

swarm.set_instance(key, role=role, securityId=securityId, securityGroup=securityGroup, ami=ami, _type=_type)

info = swarm.describe()

instances = swarm.create()
print(instances)
hive = Hive({'steps': 1, 
			'batch_size': 1, 
			'epochs': 1, 
			'learning_rate': 1, 
			'drop_r': 1}, info['code']['launch']) 
hive.create_instructions("learning_rate", [0.0001, 0.01], swarm=instances)
hive.inject_instructions()
hive.wait_for_swarm()
hive.broadcast('start')