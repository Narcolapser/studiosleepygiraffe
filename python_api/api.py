from flask import Flask, render_template, jsonify
import sys
import os
import json

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

@app.route('/projects')
def projects():
	projects = [json.loads(open(project).read()) for project in project_files]
	projects.sort(key=_get_rank)
	return jsonify(projects)

@app.route('/projects/<project>')
def project_info(project):
	print(project)
	print(project_names)
	if project not in project_names:
		return jsonify({'status':'failure'})
	
	return jsonify(json.loads(open('/home/toben/Code/ssg/'+project+'/info.json').read()))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=3000)
