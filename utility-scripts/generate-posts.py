import git
import json

def getMessages(repo,branch):
	ret = [com.message for com in repo.iter_commits('master')]
	return ret

def getPostFromMessage(message):
	lines = message.split("\n")
	title = lines[0]
	if len(lines) > 2:
		body = "\n".join(lines[2:])
	else:
		body = title
	return (title,body)

def getPosts(repo,branch,project):
	return [Post(com,branch,project) for com in repo.iter_commits(branch)]

class Post:
	def __init__(self,commit,branch=None,project=None):
		self.commit = commit
		self.title, self.message = getPostFromMessage(commit.message)
		self.date = commit.committed_datetime
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
		data = {}
		data['author'] = str(self.author)
		data['branch'] = str(self.branch)
		data['project'] = str(self.project)
		data['title'] = self.title
		data['message'] = self.message
		data['date'] = str(self.date)
		return json.dumps(data)

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

if __name__ == "__main__":
	repos = json.load(open("../ssg/public/projects.json",'r'))
	projects = {}
	for repo in repos:
		project = repo
		project['posts'] = []
#		try:
		branch = "master"
		r = git.Repo(repo['path'])
		posts = getPosts(r,branch,repo['name'])
		for p in posts:
			#print(p.json())
			#print((p.author,))
			if str(p.author) not in my_names:
				others.add(str(p.author))
				continue
			project['posts'].append(p.dict())
#		except Exception as e:
#			print("Skipping '{0}' because: {1}".format(repo,e))
		projects[repo['url']] = project
	json.dump(projects,open("../ssg/public/posts.json",'w'),indent=4, sort_keys=True)
	for o in others: print(o)
