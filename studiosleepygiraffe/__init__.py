from flask import Flask, render_template, send_file
#from flask_bootstrap import Bootstrap
#from flask_nav import Nav
#from flask_nav.elements import Navbar, View
from flask import Markup
from flask import request

import json
import os
import markdown

#from blueprints.snow import snow_api
#from blueprints.blog import blog_api
#from blueprints.resume import resume_api
import iot

#from utils import visit

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"
BLOG_DIR = "/home/toben/Code/blog/"
# BLOG_DIR = APP_ROOT + "static/blog/"
#Bootstrap(app)

#app.register_blueprint(snow_api, url_prefix='/snow')
#app.register_blueprint(blog_api, url_prefix='/blog')
#app.register_blueprint(resume_api, url_prefix='/resume')


def get_application_from_repositories(app_name):
    applications = json.load(open(APP_ROOT + "resources/repos.json"))
    for application in applications:
        if application['url'] == app_name:
            return application
    None


#nav = Nav()


#@nav.navigation()
#def mynavbar():
#    return Navbar("",
#            View('Home', 'home'),
#            View('Projects', 'apps'),
#            View('Blog', 'blog'),
#            View('Dev Log', 'devlogs'),
#            View('About', 'about')
#        )


#nav.init_app(app)


#@app.before_request
#def init_log_visit():
#    visit.log_visit(request)


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
    app = get_application_from_repositories(app_name)
    print(app)
    content = open(APP_ROOT + "resources/" + app['url'] + ".md").read()
    content = Markup(markdown.markdown(content))
    return render_template('app.html',app=app,content=content)


@app.route("/devlogs")
def devlogs():
    apps = json.load(open(APP_ROOT + "resources/repos.json"))
    return render_template('devlogs.html',apps=apps)
    
@app.route("/projects.json")
def devlogsjson():
    return open(APP_ROOT + "resources/repos.json").read()

@app.route("/project/<name>")
def project(name):
    md = open(APP_ROOT + "resources/" + name + ".md").read()
    content = Markup(markdown.markdown(md))
    return content 

@app.route("/devlog/<app_name>.json")
def devlogjson(app_name):
    content = {'name':app_name}
    apps = json.load(open(APP_ROOT + "resources/projects.json"))
    for post in apps[app_name]['posts']:
        post['message'] = post['message'].replace('\n\n','<br>')
        post['message'] = post['message'].replace('\n','')
        post['message'] = post['message'].replace('<br>','\n\n')
        post['date'] = post['date'][0:10]
    return json.dumps(apps[app_name]['posts'])


@app.route("/devlogs/<app_name>")
def disp_logs(app_name):
    content = {'name':app_name}
    apps = json.load(open(APP_ROOT + "resources/projects.json"))
    for post in apps[app_name]['posts']:
        post['message'] = post['message'].replace('\n\n','<br>')
        post['message'] = post['message'].replace('\n',' ')
        post['message'] = post['message'].replace('<br>','\n\n')
    return render_template('devlog.html',content=content,posts=apps[app_name]['posts'])


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/blog.json")
def blog():
	filenames = os.listdir(BLOG_DIR)
	processed_posts = []
	for i in filenames:
		if '.json' in i:
			post = getPostInfo(i)
			if post:
				processed_posts.append(post)
	return json.dumps(processed_posts)
#	posts = {i['date']+": "+i['title']:i for i in processed_posts}
#	titles = list(posts.keys())
#	titles.sort(reverse=True)
#	return json.dumps(posts)

@app.route("/blog/<mdfile>")
def blogpost(mdfile):
	md = open(BLOG_DIR + mdfile).read()
	content = Markup(markdown.markdown(md))
	return content

def getPostInfo(fname):
	try:
		with open(BLOG_DIR + fname) as f:
			content = json.load(f)
		content['file'] = fname.replace('.json','')
	except Exception as e:
		print(e)
		return None
	return content

@app.route("/version")
def version():
    return "0.3.0"


@app.route("/static/<file_name>")
def get_resource(file_name):
    if file_name == "style.css":
        print("Requested style.css")
        return send_file("static/style.css", mimetype="text/css")
    print(file_name)
    if ".js" in file_name:
        return send_file("static/"+file_name, mimetype="text/script")
    return send_file("static/" + file_name, mimetype='image/jpeg')

@app.route("/components/<file_name>")
def get_components(file_name):
    return send_file("components/"+file_name, mimetype="text/script")


@app.route("/iot/<device>/<method>")
def device_request(device, method):
    print("sent a request to {0} for the method {1}".format(device,method))
    iot.run(device, method)
    return str({'result': 'success'})


if __name__ == "__main__":
    app.run()
