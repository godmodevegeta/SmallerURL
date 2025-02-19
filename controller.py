from flask import Flask, redirect, request
# from dotenv import dotenv_values
from supabaseConfig import domain, numberOfCharacters, supabaseClient
import random, re
# import logging

# logger = logging.getLogger(__name__)

app = Flask(__name__)

# config = dotenv_values(".env")
smallToLong = {}
longToSmall = {}
numberOfCharacters = numberOfCharacters
domain = domain

@app.route("/api/hello/")
def hello():
    response = supabaseClient.table("planets").select("*").execute()
    print("The type is: ", type(response))
    return response

@app.route("/api/shorten", methods=["GET", "POST"])
def shorten():
    if request.method == 'POST':
        try:
            longURL = request.get_json().get("longURL")
            if longURL is None:
                raise TypeError("longURL not found")
            if not longURL.startswith(('http://', 'https://')):
                longURL = 'https://' + longURL
        except Exception as e:
            print ("INSIDE TRY-EXCEPT BLOCK")
            return "Unable to find longURL, please check request body\n",400
        if not(is_valid_url(longURL)):
            return "URL not valid", 400
        
        if (longToSmall.get(longURL)):
            print (f"mapping for {longURL} already exists")
            return f"found url {longURL} and generated smallURL {domain}api/redirect/{longToSmall[longURL]}\n"
        smallURL = generateSmallURL()
        print(f'smallURL generated: {smallURL}\n')
        longToSmall[longURL] = smallURL
        smallToLong[smallURL] = longURL
        return f"found url {longURL} and generated smallURL {domain}api/redirect/{longToSmall[longURL]}\n"
        
    
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
    randomString = random.random()
    # print(randomString , " is type " , type(randomString))
    randomString = int(randomString * numberOfCharacters)
    randomString = str(abs(randomString))
    if (smallToLong.get(randomString)):
        print(f"smallURL {randomString} already exists in map")
        return generateSmallURL()
    return randomString

def is_valid_url(url: str) -> bool:
    pattern = re.compile(
        r'^(https?:\/\/)?'  # http:// or https://
        r'(([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,6})'  # domain name
        r'(\/[a-zA-Z0-9@:%._\+~#=]*)*'  # path
        r'(\?[a-zA-Z0-9@:%._\+~#&=]*)?'  # query string
        r'(#.*)?$'  # fragment locator
    )
    return re.match(pattern, url) is not None
