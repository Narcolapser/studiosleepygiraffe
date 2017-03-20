from flask import Flask, render_template, send_file

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/version")
def version():
	return "0.0.8"

@app.route("/static/<fname>")
def get_resource(fname):
	return send_file("/static/" + fname, mimetype='image/jpeg')

if __name__ == "__main__":
	app.run()
