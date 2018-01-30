import json
import subprocess
import os
import datetime

with open('../studiosleepygiraffe/resources/repos.json') as f:
	repos = json.load(f)

tars = []
for repo in repos:
	os.chdir(repo['path'])
	os.chdir("..")
	print(repo['path'])
	tar = repo['path'].split('/')[-1]+'.tar'
	print(subprocess.check_output(['tar','-cvf',tar,repo['path']]))
	tars.append(tar)

repotar = datetime.datetime.now().strftime("%Y-%m-%d")+'-repos.tar.gz'
print(repotar)
print(subprocess.check_output(['tar','-czvf',repotar]+tars))
print("Archive made, preparing to copy")
print(subprocess.check_output(['scp',repotar,'mycroft:/media/toben/Eurus/backups/repos']))
print("Archive copied. removing temporary files")
for repo in repos:
	tar = repo['path'].split('/')[-1]+'.tar'
	print(subprocess.check_output(['rm',tar]))
#print(subprocess.check_output(['rm',repotar]))
