from flask import Flask, render_template, send_file
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
import json
import os

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
Bootstrap(app)

nav = Nav()
@nav.navigation()
def mynavbar():
	return Navbar('Stduio Sleepy Giraffe',
			View('Home', 'home'),
			View('Apps', 'apps'),
			View('Dev Log', 'devlogs'),
			View('About', 'about'),
			View('Contact', 'contact')
		)
nav.init_app(app)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/home")
def home():
	return render_template('home.html')

@app.route("/apps")
def apps():
	return render_template('apps.html')

@app.route("/app/<app_name>")
def disp_app(app_name):
	content = {'name':app_name}
	apps = json.load(open("resources/projects.json"))
	return render_template('app.html',content=content,posts=apps[app_name])

@app.route("/devlogs")
def devlogs():
	apps = json.load(open(APP_ROOT + "resources/git-post/repos.json"))
	return render_template('devlogs.html',apps=apps)

@app.route("/devlogs/<app_name>")
def disp_logs(app_name):
	content = {'name':app_name}
	apps = json.load(open(APP_ROOT + "resources/projects.json"))
	return render_template('devlog.html',content=content,posts=apps[app_name]['posts'])

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/contact")
def contact():
	return render_template('contact.html')

@app.route("/version")
def version():
	return "0.1.2"

@app.route("/static/<fname>")
def get_resource(fname):
	return send_file("static/" + fname, mimetype='image/jpeg')

if __name__ == "__main__":
	app.run()
