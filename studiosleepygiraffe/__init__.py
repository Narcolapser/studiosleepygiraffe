from flask import Flask, render_template, send_file
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
import json

app = Flask(__name__)
Bootstrap(app)

nav = Nav()
@nav.navigation()
def mynavbar():
        return Navbar('Stduio Sleepy Giraffe',
                      View('Home', 'home'),
                      View('Apps', 'apps'),
                      View('Dev Log', 'devlog'),
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
        print(apps[app_name])
        return render_template('app.html',content=content,posts=apps[app_name])

@app.route("/devlog")
def devlog():
        return render_template('devlog.html')

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
