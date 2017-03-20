from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Studio Sleepy Giraffe. Website coming soon. Test 3"
if __name__ == "__main__":
    app.run()
