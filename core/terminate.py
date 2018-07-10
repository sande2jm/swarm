#!/usr/bin/env python3
import boto3
import botocore
import time
import sys
start = time.clock()

ec2 = boto3.resource('ec2')
group = sys.argv[1]
print("Terminating "group, "...")
filters = [{'Name': 'tag:Name', 'Values': [group]}]
if group != 'all':
	for x in self.ec2.instances.filter(Filters=filters):
		if not x: pass
		if x.state['Name'] == 'running':
			x.terminate()
else:
	for x in self.ec2.instances.all():
		if not x: pass
		if x.state['Name'] == 'running':
			x.terminate()

end = time.clock()
print(end-start)