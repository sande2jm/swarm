from subprocess import call
import sys
with open('version.txt', 'r+') as f:
	v = f.readline()
with open('version.txt', 'w') as f:
	f.write(str(round(float(v),1) + 0.1))

call(['rm', '-r', '__pycache__'])
call(['rm', '-r', 'core/__pycache__'])
call(['rm', '-r', 'test/__pycache__'])
call(['git', 'add', '.'])
call(['git', 'commit', '-m', "version " + str(round(float(v),1))])
call(['git', 'push'])
