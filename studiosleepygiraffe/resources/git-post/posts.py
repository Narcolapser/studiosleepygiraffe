import git
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
		ret += "\ntags: branch:" + self.branch + " author:" + self.author + " project:" + self.project + "\n\n"
		return ret

	


if __name__ == "__main__":
	repos = open("repos",'r').readlines()
	for repo in repos:
		branch = "master"
		r = git.Repo("~/Eurus/ssg\ projects/" + repo + "/")
		posts = getPosts(r,branch,repo)
		for p in posts:
			print(p)

