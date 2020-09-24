from flask import Flask, render_template, jsonify, send_file, abort
from datetime import datetime
import sys
import os
import json
import glob

app = Flask(__name__)

project_names = [project for project in os.listdir('/home/toben/Code/ssg/') if os.path.isfile('/home/toben/Code/ssg/'+project+'/info.json')]
project_files = ['/home/toben/Code/ssg/'+project+'/info.json' for project in project_names]

@app.route('/')
def index():
	return render_template('index.html')

def _project_comp(left, right):
	print(left)
	print(right)
	return left['rank'] > right['rank']

def _get_rank(project):
	return project['rank']

@app.route('/projects/')
def projects():
	projects = [json.loads(open(project).read()) for project in project_files]
	projects.sort(key=_get_rank)
	return jsonify(projects)

@app.route('/projects/<project>')
def project_info(project):
	if project not in project_names:
		return jsonify({'status':'failure'})
	
	return jsonify(json.loads(open('/home/toben/Code/ssg/'+project+'/info.json').read()))

@app.route('/projects/<project>/<resource>')
def project_resource(project,resource):
	if project not in project_names:
		return jsonify({'status':'failure'})
	
	if resource == 'README.md':
		return open('/home/toben/Code/ssg/{}/README.md'.format(project)).read()
	
	if resource == 'banner1.png':
		return send_file('/home/toben/Code/ssg/{}/banner1.png'.format(project))

	if resource == 'banner2.png':
		return send_file('/home/toben/Code/ssg/{}/banner2.png'.format(project))
	
	files = json.load(open('/home/toben/Code/ssg/{}/info.json'))['files']
	if resource in files:
		return send_file('/home/toben/Code/ssg/{}/{}'.format(project,resource))
	else:
		abort(404)

@app.route('/posts/')
def posts():
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
	return jsonify(posts)

@app.route('/posts/<post>')
def post(post):
	directories = glob.glob('/home/toben/Code/blog/*-*-*')
	posts = [directory[22:] for directory in directories]
	if post in posts:
		info = json.load(open('/home/toben/Code/blog/{}/info.json'.format(post)))
		info['date'] = post
	else:
		info = {'Status':'Failure'}
	return jsonify(info)

@app.route('/posts/<post>/<resource>')
def post_resource(post,resource):
	directories = glob.glob('/home/toben/Code/blog/*-*-*')
	posts = [directory[22:] for directory in directories]
	if post in posts:
		if resource == 'post.md':
			return open('/home/toben/Code/blog/{}/post.md'.format(post)).read()

		if resource == 'cover.jpg':
			return send_file('/home/toben/Code/blog/{}/cover.jpg'.format(post))

		files = json.load(open('/home/toben/Code/blog/{}/info.json'.format(post)))['files']
		print(files)
		print(resource)
		if resource in files:
			return send_file('/home/toben/Code/blog/{}/{}'.format(post,resource))
		else:
			abort(404)
	else:
		return jsonify({'Status':'Failure'})

@app.route('/posts/tags/')
def tags():
	directories = glob.glob('/home/toben/Code/blog/*-*-*')
	posts = []
	tags = []
	for directory in directories:
		info = json.load(open('{}/info.json'.format(directory)))
		posts.append(info)
		tags += info['tags']

	tags = set(tags)
	return jsonify(list(tags))

@app.route('/posts/tags/<tag>')
def tag(tag):
	print(tag)
	directories = glob.glob('/home/toben/Code/blog/*-*-*')
	posts = []
	for directory in directories:
		info = json.load(open('{}/info.json'.format(directory)))
		if tag.lower() in [tag.lower() for tag in info['tags']]:
			info['date'] = directory.split('/')[-1]
			posts.append(info)

	return jsonify(posts)

@app.route('/logs/')
def logs():
	projects = [json.loads(open(project).read()) for project in project_files]
	projects.sort(key= lambda project: project['rank'])
	for project in projects: project['url'] = '/logs' + project['url']
	return jsonify(projects)

@app.route('/logs/<project>')
def log(project):
	if project not in project_names:
		return jsonify({'status':'failure'})
	
	return jsonify(json.load(open('/home/toben/Code/ssg/'+project+'/logs.json')))

@app.route('/feed.<feed_type>')
def feed(feed_type):
	print('Getting feed for ' + feed_type)
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
		val['title'] = post['title']
		val['link'] = 'http://www.studiosleepygiraffe.com/blog/posts/{}'.format(post['date'])
		val['date'] = datetime.strptime(post['date'], '%Y-%m-%d')
		val['text'] = post['text']
		val['author'] = post['author']
		posts.append(val)
		
	for project in project_names:
		logs = json.load(open('/home/toben/Code/ssg/{}/logs.json'.format(project)))
		for log in logs['posts']:
			val = {}
			val['title'] = '{}: {}'.format(project.capitalize(), log['title'])
			val['link'] = 'http://www.studiosleepygiraffe.com/logs/{}'.format(project)
			val['date'] = datetime.strptime(log['date'], '%Y-%m-%d')
			val['text'] = log['message']
			val['author'] = log['author']
			posts.append(val)

	posts.sort(key=lambda post: post['date'], reverse=True)
	if feed_type == 'rss':
		return render_template('rss.xml', posts=posts[0:20])
	else:
		return jsonify(posts[0:20])


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=3000)
