from flask import Blueprint
from flask import request
from flask import Flask, render_template, send_file
from flask import Markup

import json
import os
import markdown

blog_api = Blueprint('blog_api', __name__)
BLOG_DIR = "/home/toben/Code/blog/"
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/../"

@blog_api.route("/")
def blog():
	filenames = os.listdir(BLOG_DIR)
	processed_posts = []
	for i in filenames:
		if '.json' in i:
			post = getPostInfo(i)
			if post:
				processed_posts.append(post)
	posts = {i['date']+": "+i['title']:i for i in processed_posts}
	titles = list(posts.keys())
	titles.sort(reverse=True)
	return render_template('blog.html',posts=posts,titles=titles)

def getPostInfo(fname):
	try:
		with open(BLOG_DIR + fname) as f:
			content = json.load(f)
		content['file'] = fname.replace('.json','')
	except Exception as e:
		print(e)
		return None
	return content

@blog_api.route("/<post>")
def blog_post(post):
	with open(BLOG_DIR + post + '.json') as f:
		content = json.load(f)
	if content['content_file']:
		md = open(BLOG_DIR + content['content_file']).read()
		content['content'] = Markup(markdown.markdown(md))
	return render_template('blogpost.html',title=post,content=content)

@blog_api.route("/cover/<fname>")
def get_cover(fname):
	print("Getting cover:" + BLOG_DIR + "covers/" + fname)
	if ".jpg" in fname:
		return send_file(BLOG_DIR + "covers/" + fname, mimetype='image/jpeg')

@blog_api.route("/tags/<tag>")
def get_posts_with_tag(tag):
	print("fetching posts with tag: " + tag)
	files = os.listdir(BLOG_DIR)
	posts = []
	for f in files:
		if '.json' in f:
			print(f)
			with open(BLOG_DIR + f) as open_file:
				content = json.load(open_file)
				if tag in content['tags']:
					print((content['date'],content['title']))
					posts.append((content['date'],content['title']))

	return render_template('blogtag.html', tag=tag, posts=posts)
