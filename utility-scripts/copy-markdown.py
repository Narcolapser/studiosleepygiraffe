import json

server_path = "/var/www/studiosleepygiraffe/studiosleepygiraffe/resources/"

if __name__ == "__main__":
	repos = json.load(open("../studiosleepygiraffe/resources/repos.json",'r'))
	for repo in repos:
		try:
			ins = open(repo['path']+'/README.md','r').read()
			open(server_path+repo['url']+'.md','w').write(ins)
		except Exception as e:
			print("Failed to transfer markdown for {0} ran into: {1}".format(repo['name'],e))
