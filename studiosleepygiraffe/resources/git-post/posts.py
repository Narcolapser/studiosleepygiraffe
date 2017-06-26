import git
def getMessages(repo,branch):
	ret = [com.message for com in r.iter_commits('master')]
	return ret

def getPostFromMessage(message):
	lines = message.split("\n")
	title = lines[0]
	if len(lines) > 2:
		body = "\n".join(lines[2:])
	else:
		body = title
	return (title,body)

#for com in r.iter_commits('master'): print com.message

if __name__ == "__main__":
	repo = "~/Code/warehouse/"
	branch = "master"
	r = git.Repo(repo)
	messages = getMessages(r,branch)
	for m in messages:
		title,body = getPostFromMessage(m)
		print(title)
		print(body)

