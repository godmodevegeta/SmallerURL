from flask import Flask, jsonify, redirect, request, make_response
# from dotenv import dotenv_values
from supabaseConfig import domain, numberOfCharacters, randomStringURL, insert, fetch_small, fetch_long
# from supabaseConfig import supabaseClient
import random, re
import logging, requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# config = dotenv_values(".env")
smallToLong = {}
longToSmall = {}
numberOfCharacters = numberOfCharacters
domain = domain
randomStringURL = randomStringURL
external_call = True
supapostgresroute = False
cacheEnabled = False

@app.route("/api/hello/")
def hello():
    response = make_response()
    response.data = "Hello, there! :)\n"
    response.status_code = 200
    # logger.info("The type is: ", type(response))
    return response

@app.route("/api/shorten/", methods=["GET", "POST"])
def shorten():
    global supapostgresroute
    if request.method == 'POST':
        try:
            longURL = request.get_json().get("longURL")
            if longURL is None:
                raise TypeError("longURL not found")
            if not longURL.startswith(('http://', 'https://')):
                longURL = 'https://' + longURL
        except Exception as e:
            logger.exception("exception: {e}".format(e=e))
            return jsonify({"error": "Unable to find longURL, please check request body"}), 400
        # if not(is_valid_url(longURL)):
        #     return "URL not valid", 400

        # check if small URL already exists in supabase
        # logger.info("External calls to Supabase:", supapostgresroute)
        if (supapostgresroute):
            logger.info("Fetching mappings from supabase")
            smallURL = fetch_small(longURL)
            logger.info(f"smallURL found from supabase: {smallURL}")
            if smallURL != None:
                logger.debug (f"mapping for {longURL} already exists in SUPABASE")
                return jsonify({"longURL": longURL, 
                                "shortURL": f"{domain}api/redirect/{smallURL}"})

        # if small URL already exists in in-memory table
        elif (longToSmall.get(longURL)):
            return in_memory_find(longURL)
            
        # if no mappings exist in supabase or in-memory table
        smallURL = generateSmallURL()
        logger.debug(f'smallURL generated: {smallURL}\n')

        if supapostgresroute:
            logger.info(f"insertion to Supabase initiated")
            insert(smallURL, longURL)
            logger.info(f"inserted {longURL} to DATABASE")
        else:
            logger.info("in-memory mapping initiated")
            longToSmall[longURL] = smallURL
            smallToLong[smallURL] = longURL            
        return jsonify({"longURL": longURL, 
                        "shortURL": f"{domain}api/redirect/{smallURL}"})
    
    else:
        return jsonify({"message": "Please input URL in body"}), 200

@app.route("/api/redirect/<smallURL>")
def redirectTo(smallURL):
    if supapostgresroute:
        logger.info (f"searching longURL for {smallURL} in supabase")
        try:
            longURL = fetch_long(smallURL)
            if longURL is None:
                raise ValueError(f"mapping for {smallURL} NOT FOUND")
        except Exception as e:
            return jsonify({"error": "NO mappings found in SUPABASE! Please first shorten the longURL first!"}), 404
        logger.info ("found longURL: {longURL} from supabase".format(longURL=longURL))

    else:
        logger.info (f"searching longURL for {smallURL} in memory hash-table")
        try:
            longURL = smallToLong.get(smallURL)
            if longURL is None:
                raise ValueError(f"mapping for {smallURL} NOT FOUND")
        except Exception as e:
            return jsonify({"error": "NO mappings found! Please first shorten the longURL first!"}), 404
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
        if fetch_long(randomString):
            logger.info(f"{randomString} already exists in Supabase mapping. Generating ShortCode again.")
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

def in_memory_find(longURL):
    logger.info (f"mapping for {longURL} already exists")
    return jsonify({
        "longURL": longURL,
        "shortURL": f"{domain}api/redirect/{longToSmall[longURL]}"
    }), 200
