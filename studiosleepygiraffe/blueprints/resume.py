from flask import Blueprint
from flask import request
from flask import Flask, render_template, send_file
from flask import Markup
from xhtml2pdf import pisa
from io import StringIO

import os
import json

resume_api = Blueprint('resume_api', __name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/../"


@resume_api.route("/resume")
def resume_html():
    return resume()


@resume_api.route("/resume.pdf")
def resume_pdf():
    template = resume()
    pdf = StringIO()
    pisa.CreatePDF(StringIO(template.encode('utf-8')),pdf)
    pdf.seek(0)
    return send_file(pdf, attachment_filename="Toben_Archer.pdf", mimetype='application/pdf')


def resume():
    resume_json = json.load(open(APP_ROOT + "resources/resume.json"))
    return render_template('resume.html', resume=resume_json)
