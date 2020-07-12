import git
import json
import time
import os

time_str = '%Y-%m-%d'

def getMessages(repo,branch):
	ret = [com.message for com in repo.iter_commits('master')]
	return ret

def getPostFromMessage(message):
	lines = message.split("\n")
	title = lines[0]
	if len(lines) > 2:
		body = "\n".join(lines[2:])
		
		# Replace text wrapping, single \n, in posts with spaces while retaining paragraph breaks.
		body = body.replace('\n\n','LINEBREAK')
		body = body.replace('\n',' ')
		body = body.replace('LINEBREAK','\n\n')
	else:
		body = title
	return (title,body)

def getPosts(repo,branch,project):
	return [Post(com,branch,project) for com in repo.iter_commits(branch)]

class Post:
	def __init__(self,commit,branch=None,project=None):
		self.commit = commit
		self.title, self.message = getPostFromMessage(commit.message)
		self.date = commit.committed_datetime.strftime(time_str)
		self.branch = branch
		self.author = commit.author
		self.project = project

	def __str__(self):
		ret = self.title
		ret += "\n" + self.message
		ret += "\n" + str(self.date)
		ret += "\ntags: branch:" + str(self.branch) + " author:" + str(self.author) + " project:" + self.project + "\n\n"
		return ret

	def json(self):
		return json.dumps(self.dict())

	def dict(self):
		data = {}
		data['author'] = str(self.author)
		data['branch'] = str(self.branch)
		data['project'] = str(self.project)
		data['title'] = self.title
		data['message'] = self.message
		data['date'] = str(self.date)
		return data

my_names = ['Toben Archer','Narcolapser','Toben']
others = set()
base = '/home/toben/Code/ssg/'

if __name__ == "__main__":
	#repos = [json.load(open(repo+'/info.json')) for repo in os.listdir('/home/toben/Code/ssg/')]
	repos = os.listdir(base)
	for repo in repos:
		if not os.path.isfile(base + repo+'/info.json'):
			print('Skipping project {} as it has no info.json file.'.format(repo))
			continue

		print('Generating posts for {}'.format(repo))
		project = json.load(open(base + repo+'/info.json'))
		project['posts'] = []

#		projects[repo['url']] = project
		r = git.Repo(base + repo)
		posts = getPosts(r,'master',repo)
		for p in posts:
			if str(p.author) not in my_names:
				others.add(str(p.author))
				continue
			project['posts'].append(p.dict())
		json.dump(project,open(base + repo+'/logs.json','w'),indent=4, sort_keys=True)
	
	for o in others: print(o)
