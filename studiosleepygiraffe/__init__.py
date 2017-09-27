from flask import Flask, render_template, send_file
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask import Markup
import json
import os
import markdown

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"
Bootstrap(app)

def getAppFromRepos(app_name):
	apps = json.load(open(APP_ROOT + "resources/repos.json"))
	for app in apps:
		if app['url'] == app_name:
			return app
	None

nav = Nav()
@nav.navigation()
def mynavbar():
	return Navbar('Studio Sleepy Giraffe',
			View('Home', 'home'),
			View('Projects', 'apps'),
			View('Dev Log', 'devlogs'),
			View('About', 'about')
		)
nav.init_app(app)

@app.route("/")
def index():
	return render_template('home.html')

@app.route("/home")
def home():
	return render_template('home.html')

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

@app.route("/contact")
def contact():
	return render_template('contact.html')

@app.route("/version")
def version():
	return "0.1.2"

@app.route("/static/<fname>")
def get_resource(fname):
	if fname == "style.css":
		print("Requested style.css")
		return send_file("static/style.css", mimetype="text/css")
	print(fname)
	return send_file("static/" + fname, mimetype='image/jpeg')

if __name__ == "__main__":
	app.run()
