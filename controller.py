from flask import Flask, request


app = Flask(__name__)

smallToLong = {}
longToSmall = {}

@app.route("/api/hello/")
def hello():
    return "<h1>Hello there!</h1>"

@app.route("/api/shorten", methods=["GET", "POST"])
def shorten():
    if request.method == 'POST':
        longURL = request.get_json().get("longURL")
        smallURL = generateSmallURL()
        longToSmall[longURL] = "http://127.0.0.1:5000/api/redirect/" + smallURL
        smallToLong[smallURL] = longURL
        return f"found url {longURL} and generated smallURL {longToSmall[longURL]}\n"
    
    else:
        return "<h1>Please input URL</h1>", 200

# @app.route("/api/redirect/")
# def redirect():


def generateSmallURL():
    return "smallxyx"