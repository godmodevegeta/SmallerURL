from flask import Flask, request


app = Flask(__name__)

@app.route("/api/hello/")
def hello():
    return "<h1>Hello there!</h1>"

@app.route("/api/shorten", methods=["GET", "POST"])
def shorten():
    if request.method == 'POST':
        longURL = request.get_json().get("longURL")
        return f"found url {longURL}"
    
    else:
        return "<h1>Please input URL</h1>", 200

