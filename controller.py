from flask import Flask, request, redirect
# from dotenv import dotenv_values
from supabaseConfig import domain, numberOfCharacters, supabaseClient
import random, re
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)

app = Flask(__name__)

# config = dotenv_values(".env")
smallToLong = {}
longToSmall = {}
numberOfCharacters = numberOfCharacters
domain = domain

@app.route("/api/hello/")
def hello():
    response = supabaseClient.table("planets").select("*").execute()
    logger.info("The type is: ", type(response))
    return response

@app.route("/api/shorten", methods=["GET", "POST"])
def shorten():
    if request.method == 'POST':
        try:
            longURL = request.get_json().get("longURL")
            if longURL is None:
                raise TypeError("longURL not found")
        except Exception as e:
            logger.info ("INSIDE TRY-EXCEPT BLOCK")
            return "Unable to find longURL, please check request body\n",400
        if not(is_valid_url(longURL)):
            return "URL not valid", 400
        
        if (longToSmall.get(longURL)):
            logger.info (f"mapping for {longURL} already exists")
            return f"found url {longURL} and generated smallURL {domain}api/redirect/{longToSmall[longURL]}\n"
        smallURL = generateSmallURL()
        logger.info(f'smallURL generated: {smallURL}\n')
        longToSmall[longURL] = smallURL
        smallToLong[smallURL] = longURL
        return f"found url {longURL} and generated smallURL {domain}api/redirect/{longToSmall[longURL]}\n"
        
    
    else:
        return "<h1>Please input URL</h1>", 200

@app.route("/api/redirect/<smallURL>")
def redirectTo(smallURL):
    logger.info ("searching for longURL for smallURL")
    longURL = smallToLong.get(smallURL)
    # logger.info(smallToLong)
    logger.info ("found longURL: {longURL}".format(longURL=longURL))
    return redirect(longURL)
  

def generateSmallURL():
    randomString = random.random()
    # logger.info(randomString , " is type " , type(randomString))
    randomString = int(randomString * numberOfCharacters)
    randomString = str(abs(randomString))
    if (smallToLong.get(randomString)):
        logger.info(f"smallURL {randomString} already exists in map")
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
