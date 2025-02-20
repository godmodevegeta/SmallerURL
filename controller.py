from flask import Flask, redirect, request, make_response
# from dotenv import dotenv_values
from supabaseConfig import domain, numberOfCharacters, randomStringURL
# from supabaseConfig import supabaseClient
import random, re
import logging, requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
external_call = False

app = Flask(__name__)

# config = dotenv_values(".env")
smallToLong = {}
longToSmall = {}
numberOfCharacters = numberOfCharacters
domain = domain
randomStringURL = randomStringURL

@app.route("/api/hello/")
def hello():
    # response = supabaseClient.table("planets").select("*").execute()
    response = make_response()
    response.data = "Hello, there! :)\n"
    response.status_code = 200
    logger.info("The type is: ", type(response))
    return response

@app.route("/api/shorten/", methods=["GET", "POST"])
def shorten():
    if request.method == 'POST':
        try:
            longURL = request.get_json().get("longURL")
            if longURL is None:
                raise TypeError("longURL not found")
            if not longURL.startswith(('http://', 'https://')):
                longURL = 'https://' + longURL
        except Exception as e:
            logger.info ("INSIDE TRY-EXCEPT BLOCK")
            return "Unable to find longURL, please check request body\n",400
        # if not(is_valid_url(longURL)):
        #     return "URL not valid", 400
        
        if (longToSmall.get(longURL)):
            logger.debug (f"mapping for {longURL} already exists")
            return f"found url {longURL} and generated smallURL {domain}api/redirect/{longToSmall[longURL]}\n"
        smallURL = generateSmallURL()
        logger.debug(f'smallURL generated: {smallURL}\n')

        longToSmall[longURL] = smallURL
        smallToLong[smallURL] = longURL
        return f"longURL: {longURL} and generated smallURL: {domain}api/redirect/{longToSmall[longURL]}\n"
        
    
    else:
        return "<h1>Please input URL</h1>", 200

@app.route("/api/redirect/<smallURL>")
def redirectTo(smallURL):
    logger.info (f"searching longURL for {smallURL}")
    try:
        longURL = smallToLong.get(smallURL)
        if longURL is None:
            raise ValueError(f"mapping for {smallURL} NOT FOUND")
    except Exception as e:
        return "NO mappings found! Please first shorten the longURL first!"
    logger.debug("small->long mappings:", smallToLong)
    logger.info ("found longURL: {longURL}".format(longURL=longURL))
    return redirect(longURL)
  

def generateSmallURL():
    global external_call
    logger.info(f"External call to randomStringAPI: {external_call}")
    if external_call:
        try:
            randomString = requests.get(randomStringURL).json()[0]
            if randomString is None:
                raise TypeError("Call returned None\n")
        except Exception as e:
            logger.warning("External API returned None")
            logger.warning("Turning external_call OFF")
            external_call = False
            return generateSmallURL()
        logger.info(f"External Call to {randomStringURL} Successful with Response: {randomString}")
    else:
        randomString = random.random()
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
