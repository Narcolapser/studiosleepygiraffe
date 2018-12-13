from flask import Flask, render_template, send_file
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask import Markup
from flask import request

import json
import os
import markdown

from blueprints.snow import snow_api
from blueprints.blog import blog_api
import iot

from util import log_visit

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"
BLOG_DIR = "/home/toben/Code/blog/"
#BLOG_DIR = APP_ROOT + "static/blog/"
Bootstrap(app)

app.register_blueprint(snow_api, url_prefix='/snow')
app.register_blueprint(blog_api, url_prefix='/blog')

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
            View('Blog', 'blog'),
            View('Dev Log', 'devlogs'),
            View('About', 'about')
        )
nav.init_app(app)

@app.before_request
def init_log_visit():
    log_visit(request)

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

@app.route("/about/resume")
def resumeHTML():
	return resume()

@app.route("/about/resume.pdf")
def resumePDF():
	template = resume()
	pdf = StringIO()
	pisa.CreatePDF(StringIO(template.encode('utf-8')),pdf)
	pdf.seek(0)
	return send_file(pdf,attachment_filename="Toben_Archer.pdf",mimetype='application/pdf')

def resume():
	resume_json = json.load(open(APP_ROOT + "resources/resume.json"))
	return render_template('resume.html',resume=resume_json)

@app.route("/blog")
def blog():
    pass

@app.route("/version")
def version():
    return "0.3.0"

@app.route("/static/<fname>")
def get_resource(fname):
    if fname == "style.css":
        print("Requested style.css")
        return send_file("static/style.css", mimetype="text/css")
    print(fname)
    if ".js" in fname:
        return send_file("static/"+fname,mimetype="text/script")
    return send_file("static/" + fname, mimetype='image/jpeg')


@app.route("/iot/<device>/<method>")
def device_request(device,method):
	print("sent a request to {0} for the method {1}".format(device,method))
	iot.run(device,method)
	return str({'result':'success'})

if __name__ == "__main__":
    app.run()
    
