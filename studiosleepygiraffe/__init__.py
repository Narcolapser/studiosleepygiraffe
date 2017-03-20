from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
	return "Studio Sleepy Giraffe. Website coming soon."

@app.route("/version")
def version():
	return "0.0.6"

if __name__ == "__main__":
	app.run()
