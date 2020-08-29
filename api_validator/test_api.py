from datetime import datetime
import sys
import os
import json
import requests
import glob


project_names = [project for project in os.listdir('/home/toben/Code/ssg/') if os.path.isfile('/home/toben/Code/ssg/'+project+'/info.json')]
project_files = ['/home/toben/Code/ssg/'+project+'/info.json' for project in project_names]
project_info = [json.loads(open(project).read()) for project in project_files]
project_info.sort(key= lambda project: project['rank'])

base_url = 'http://localhost:3000'

class Test_API():
	
	def test_projects(self):
		projects = requests.get(base_url + '/projects').json()
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
			print(info)
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
		
	
	def test_tags(self):
		assert True
	
	def test_feeds(self):
		assert True
