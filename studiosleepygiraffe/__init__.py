from flask import Flask, render_template, send_file
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask import Markup
from xhtml2pdf import pisa
from StringIO import StringIO
import json
import os
import markdown

from blueprints.snow import snow_api

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"
BLOG_DIR = "/home/toben/Code/blog/"
#BLOG_DIR = APP_ROOT + "static/blog/"
Bootstrap(app)

app.register_blueprint(snow_api, url_prefix='/snow')

def getAppFromRepos(app_name):
	apps = json.load(open(APP_ROOT + "resources/repos.json"))
	for app in apps:
		if app['url'] == app_name:
			return app
	None

nav = Nav()
@nav.navigation()
def mynavbar():
	return Navbar("",
			View('Home', 'home'),
			View('Projects', 'apps'),
			View('Blog', 'blog'), #not sure why but this expects me to put contact here...
			View('Dev Log', 'devlogs'),
			View('About', 'about')
		)
nav.init_app(app)

@app.route("/")
def index():
#	return render_template('index.html')
#	return render_template('houses.html')
	return render_template('home.html')

@app.route("/houses")
def houses():
	houses = os.listdir(APP_ROOT + "static/housepics/")
	return render_template('houses.html',houses=houses)

@app.route("/house/<house_name>")
def house(house_name):
	photolist = os.listdir(APP_ROOT + "static/housepics/"+house_name)
	return render_template('house.html',photos=photolist,house=house_name)

@app.route("/home")
def home():
	return render_template('home.html')
#	return render_template('houses.html')

@app.route("/apps")
def apps():
	apps = json.load(open(APP_ROOT + "resources/repos.json"))
	return render_template('apps.html',apps=apps)

@app.route("/apps/<app_name>")
def disp_app(app_name):
	app = getAppFromRepos(app_name)
	print(app)
	content = open(APP_ROOT + "resources/" + app['url'] + ".md").read()
	content = Markup(markdown.markdown(content))
	return render_template('app.html',app=app,content=content)

@app.route("/devlogs")
def devlogs():
	apps = json.load(open(APP_ROOT + "resources/repos.json"))
	return render_template('devlogs.html',apps=apps)

@app.route("/devlogs/<app_name>")
def disp_logs(app_name):
	content = {'name':app_name}
	apps = json.load(open(APP_ROOT + "resources/projects.json"))
	for post in apps[app_name]['posts']:
		post['message'] = post['message'].replace('\n\n','<br>')
		post['message'] = post['message'].replace('\n','')
		post['message'] = post['message'].replace('<br>','\n\n')
	return render_template('devlog.html',content=content,posts=apps[app_name]['posts'])

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/blog")
def blog():
	filenames = os.listdir(BLOG_DIR)
	processed_posts = []
	for i in filenames:
		if '.json' in i:
			post = getPostInfo(i)
			if post:
				processed_posts.append(post)
	posts = {i['date']+": "+i['title']:i for i in processed_posts}
	titles = posts.keys()
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

@app.route("/blog/<post>")
def blog_post(post):
	with open(BLOG_DIR + post + '.json') as f:
		content = json.load(f)
	if content['content_file']:
		md = open(BLOG_DIR + content['content_file']).read()
		content['content'] = Markup(markdown.markdown(md))
	return render_template('blogpost.html',title=post,content=content)

@app.route("/blog/cover/<fname>")
def get_cover(fname):
	print("Getting cover:" + BLOG_DIR + "covers/" + fname)
	if ".jpg" in fname:
		return send_file(BLOG_DIR + "covers/" + fname, mimetype='image/jpeg')

@app.route("/blog/tags/<tag>")
def get_posts_with_tag(tag):
	print("fetching posts with tag: " + tag)
	return render_template('blogtag.html', tag=tag)

@app.route("/version")
def version():
	return "0.2.1"

@app.route("/static/<fname>")
def get_resource(fname):
	if fname == "style.css":
		print("Requested style.css")
		return send_file("static/style.css", mimetype="text/css")
	print(fname)
	if ".js" in fname:
		return send_file("static/"+fname,mimetype="text/script")
	return send_file("static/" + fname, mimetype='image/jpeg')

if __name__ == "__main__":
	app.run()
