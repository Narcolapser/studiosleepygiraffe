from flask import Blueprint
from flask import request
from flask import Flask, render_template, send_file
from flask import Markup
from xhtml2pdf import pisa
from io import StringIO

import os

snow_api = Blueprint('snow_api', __name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/../"

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def get_clearings(month):
	clearings = []

	month_num = months.index(month) + 1
	
	csv = open(APP_ROOT + "resources/snow.csv").read().split('\n')
	for cl in csv:
		if len(cl) < 3:
			continue
		mon, day = cl.split(',')
		if int(mon) == month_num:
			clearings.append(day)
	
	return clearings


def get_snow_template(month):
	month = month.capitalize()
	month_num = months.index(month) + 1
	if month_num < 10:
		month_num = "0" + str(month_num)
	else:
		month_num = str(month_num)

	clearings = get_clearings(month)
	
	return render_template('snow.html', clearings=clearings,month=month,month_num=month_num)


@snow_api.route("/<month>")
def get_snow(month):
	return get_snow_template(month)


@snow_api.route("/<month>.pdf")
def get_snow_pdf(month):
	template = get_snow_template(month)
	pdf = StringIO()
	pisa.CreatePDF(StringIO(template.encode('utf-8')), pdf)
	pdf.seek(0)
	return send_file(pdf,attachment_filename=month+".pdf", mimetype='application/pdf')
