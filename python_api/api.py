from flask import Flask, render_template, jsonify, send_file, abort
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
		info = {'Status':'Failure'}

@app.route('/logs/')
def logs():
	projects = [json.loads(open(project).read()) for project in project_files]
	projects.sort(key=_get_rank)
	return jsonify(projects)

@app.route('/logs/<project>')
def log(project):
	print(project)
	print(project_names)
	if project not in project_names:
		return jsonify({'status':'failure'})
	
	return jsonify(json.loads(open('/home/toben/Code/ssg/'+project+'/logs.json').read()))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=3000)