from flask import Flask, request, redirect
import random

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
        if (longToSmall.get(longURL)):
            print (f"mapping for {longURL} already exists")
            return f"found url {longURL} and generated smallURL http://127.0.0.1:5000/api/redirect/{longToSmall[longURL]}\n"
        smallURL = generateSmallURL()
        longToSmall[longURL] = smallURL
        smallToLong[smallURL] = longURL
        return f"found url {longURL} and generated smallURL http://127.0.0.1:5000/api/redirect/{longToSmall[longURL]}\n"
    
    else:
        return "<h1>Please input URL</h1>", 200

@app.route("/api/redirect/<smallURL>")
def redirectTo(smallURL):
    print ("searching for longURL for smallURL")
    longURL = smallToLong.get(smallURL)
    # print(smallToLong)
    print ("found longURL: {longURL}".format(longURL=longURL))
    return redirect(longURL)
  

def generateSmallURL():
    randomString = random.gauss()
    # print(randomString , " is type " , type(randomString))
    noDecimal = int(randomString * 100000)
    return str(abs(noDecimal))