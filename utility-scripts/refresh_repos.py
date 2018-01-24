import json
import subprocess

with open('../studiosleepygiraffe/resources/repos.json') as f:
	repos = json.load(f)

for repo in repos:
	print(repo['path'])
	print(subprocess.check_output(['git','pull']))
#	proc = subprocess.Popen(['git','pull'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
