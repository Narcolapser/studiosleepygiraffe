from flask import Flask, render_template, send_file
from flask import Markup
from flask import request
#from xhtml2pdf import pisa
from io import StringIO

import pdfkit
import json
import os
import markdown

import iot

#from utils import visit

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"
BLOG_DIR = "/home/toben/Code/blog/"


def get_application_from_repositories(app_name):
    applications = json.load(open(APP_ROOT + "resources/repos.json"))
    for application in applications:
        if application['url'] == app_name:
            return application
    None


#@app.before_request
#def init_log_visit():
#    visit.log_visit(request)


@app.route("/")
def index():
    return render_template('home.html')

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

@app.route("/blog.json")
def blog():
    filenames = os.listdir(BLOG_DIR)
    processed_posts = []
    for i in filenames:
        if '.json' in i:
            post = getPostInfo(i)
            if post:
                processed_posts.append(post)
    processed_posts.sort(key=lambda val: val['date'], reverse=True)
    return json.dumps(processed_posts)

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
    return "2.0.0"

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


@app.route("/resume/html")
def resume_html():
    return resume()


@app.route("/resume/Toben_Archer.pdf")
def resume_pdf():
    template = resume()
    out_loc = '/tmp/resume.pdf'
    pdfkit.from_string(template,out_loc)
#    pdf = open(out_loc,'rb').read()
#    return send_file(pdf, attachment_filename="Toben_Archer.pdf", mimetype='application/pdf')
    return send_file('/tmp/resume.pdf',attachment_filename="Toben_Archer.pdf",mimetype='application/pdf')


def resume():
    resume_json = json.load(open(APP_ROOT + "resources/resume.json"))
    return render_template('resume.html', resume=resume_json)


if __name__ == "__main__":
    app.run()
