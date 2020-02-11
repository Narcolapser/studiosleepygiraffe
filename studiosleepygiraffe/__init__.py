from flask import Flask, render_template, send_file
from flask import Markup
from flask import request

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


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')


@app.route("/static/<file_name>")
def get_resource(file_name):
    if file_name == "style.css":
        print("Requested style.css")
        return send_file("static/style.css", mimetype="text/css")
    print(file_name)
    if ".js" in file_name:
        return send_file("static/"+file_name, mimetype="text/script")

    return send_file("static/" + file_name, mimetype='image/jpeg')


@app.route("/iot/<device>/<method>")
def device_request(device, method):
    print("sent a request to {0} for the method {1}".format(device,method))
    iot.run(device, method)
    return str({'result': 'success'})


if __name__ == "__main__":
    app.run()
