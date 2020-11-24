from datetime import datetime
import sys
import os
import json
import requests
import glob
import xmltodict


project_names = [project for project in os.listdir('/home/toben/Code/ssg/') if os.path.isfile('/home/toben/Code/ssg/'+project+'/info.json')]
project_files = ['/home/toben/Code/ssg/'+project+'/info.json' for project in project_names]
project_info = [json.loads(open(project).read()) for project in project_files]
project_info.sort(key= lambda project: project['rank'])
for project in project_info: project['url'] = '/projects' + project['url']

# Python
base_url = 'http://localhost:5000'

# Ruby
#base_url = 'http://localhost:3000'

class Test_API():
	
	def test_projects(self):
		projects = requests.get(base_url + '/projects').json()
		print(projects)
		print(project_info)
		assert projects == project_info
	
	def test_posts(self):
		# Test the overal post fetch
		directories = glob.glob('/home/toben/Code/blog/*-*-*')
		posts = []
		for directory in directories:
			post = {}
			post['date'] = directory[22:]
			post['url'] = '/posts/' + directory[22:]
			info = json.load(open('{}/info.json'.format(directory)))
			post['title'] = info['title']
			post['cover'] = 'cover.jpg'
			post['author'] = info['author']
			
			posts.append(post)
		posts.sort(key=lambda post: post['date'],reverse=True)
		assert requests.get(base_url + '/posts').json() == posts
		
		# Test fetching each post's info
		for post in posts:
			req = requests.get(base_url + post['url']).json()
			info = json.load(open('/home/toben/Code/blog/{}/info.json'.format(post['date'])))
			info['date'] = post['date']
			assert req == info
			
			assert requests.get(base_url + '{}/post.md'.format(post['url'] )).status_code == 200
			assert requests.get(base_url + '{}/cover.jpg'.format(post['url'] )).status_code == 200

			for resource in info['files']:
				assert requests.get(base_url + '{}/{}'.format(post['url'], resource )).status_code == 200
			
			# Request I file I know is there but should not have access to.
			assert requests.get(base_url + '{}/info.md'.format(post['url'] )).status_code == 404
			
			# Request nonsense
			assert requests.get(base_url + '{}/nonsense'.format(post['url'] )).status_code == 404
			


	def test_logs(self):
		# Test getting projects:
		local_projects = [json.loads(open(project).read()) for project in project_files]
		local_projects.sort(key= lambda project: project['rank'])
		for project in local_projects: project['url'] = '/logs' + project['url']
		assert requests.get(base_url + '/logs').json() == local_projects
		
		# Test getting each log
		for project in project_names:
			log = json.load(open('/home/toben/Code/ssg/'+project+'/logs.json'))
			assert log == requests.get(base_url + '/logs/' + project).json()

	def test_tags(self):
		# check that each tag has blog posts
		directories = glob.glob('/home/toben/Code/blog/*-*-*')
		posts = []
		tags = []
		for directory in directories:
			info = json.load(open('{}/info.json'.format(directory)))
			posts.append(info)
			tags += info['tags']

		tags = set(tags)

		assert requests.get(base_url + '/posts/tags').json().sort() == list(tags).sort()
		
		for tag in tags:
			posts = []
			for directory in directories:
				info = json.load(open('{}/info.json'.format(directory)))
				if tag.lower() in [tag.lower() for tag in info['tags']]:
					info['date'] = directory.split('/')[-1]
					posts.append(info)
			assert requests.get(base_url + '/posts/tags/' + tag).json() == posts

	def test_feeds(self):
		# Check RSS feed
		directories = glob.glob('/home/toben/Code/blog/*-*-*')
		blog_posts = []
		for post in [directory[22:] for directory in directories]:
			info = json.load(open('/home/toben/Code/blog/{}/info.json'.format(post)))
			info['date'] = post
			info['text'] = '\n'.join(open('/home/toben/Code/blog/{}/post.md'.format(post)).read().split('\n')[0:3])
			blog_posts.append(info)

		posts = []
		for post in blog_posts:
			val = {}
			val[u'title'] = post['title']
			val[u'link'] = u'http://studiosleepygiraffe.com/blog/posts/{}'.format(post['date'])
			val[u'date'] = datetime.strptime(post['date'], '%Y-%m-%d')
			val[u'text'] = post['text']
			val[u'author'] = post['author']
			posts.append(val)
			
		for project in project_names:
			logs = json.load(open('/home/toben/Code/ssg/{}/logs.json'.format(project)))
			for log in logs['posts']:
				val = {}
				val[u'title'] = u'{}: {}'.format(project.capitalize(), log['title'])
				val[u'link'] = u'http://studiosleepygiraffe.com/logs/{}'.format(project)
				val[u'date'] = datetime.strptime(log['date'], '%Y-%m-%d')
				val[u'text'] = log['message']
				val[u'author'] = log['author']
				posts.append(val)

		posts.sort(key=lambda post: post['date'], reverse=True)
		
		posts = posts[0:20]
		for post in posts:
			post[u'date'] = post[u'date'].strftime('%a, %d %b %Y 00:00:00 GMT')
		
		posts = json.loads(json.dumps(posts))
			
		assert posts == requests.get(base_url + '/feed.json').json()
		rss = xmltodict.parse(requests.get(base_url + '/feed.rss').text)
		rss = json.loads(json.dumps(rss))
		assert rss['rss']['channel']['title'] == 'Studio Sleepy Giraffe'
		assert rss['rss']['channel']['link'] == 'http://www.studiosleepygiraffe.com/'
		assert rss['rss']['channel']['description'] == 'What has been happening at SSG.'
		
		# Ensure the correct posts are coming through. 
		for i,item in enumerate(rss['rss']['channel']['item']):
			assert item['title'] == posts[i]['title']

