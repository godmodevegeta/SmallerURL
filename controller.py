from flask import Flask, jsonify, redirect, request, make_response
from typing import Optional, Dict, Tuple, Callable, Any
from dataclasses import dataclass
from functools import wraps
import logging
import requests
from supabaseConfig import domain, numberOfCharacters, randomStringURL, insert, fetch_small, fetch_long

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@dataclass(frozen=True)
class URLMapping:
    long_url: str
    short_code: str

class Result:
    def __init__(self, value, error=None):
        self.value = value
        self.error = error is None

    @classmethod
    def success(cls, value):
        return cls(value)

    @classmethod
    def failure(cls, error):
        return cls(None, error)

def with_error_handling(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Error in {f.__name__}: {str(e)}")
            return jsonify({"error": str(e)}), 400
    return wrapper

def validate_url(url: str) -> Result:
    """Pure function to validate URL format"""
    if not url:
        return Result.failure("URL cannot be empty")
    if not isinstance(url, str):
        return Result.failure("URL must be a string")
    
    normalized_url = url if url.startswith(('http://', 'https://')) else f'https://{url}'
    return Result.success(normalized_url)

def generate_short_code(existing_urls: Callable[[str], bool]) -> Result:
    """Pure function to generate short code"""
    try:
        response = requests.get(randomStringURL)
        if response.status_code != 200:
            return Result.failure("Failed to generate short code")
        
        short_code = response.json()[0]
        if existing_urls(short_code):
            return generate_short_code(existing_urls)
        
        return Result.success(short_code)
    except Exception as e:
        return Result.failure(f"Error generating short code: {str(e)}")

def create_short_url(short_code: str) -> str:
    """Pure function to create full short URL"""
    return f"{domain}api/redirect/{short_code}"

@app.route("/api/shorten/", methods=["POST"])
@with_error_handling
def shorten():
    """Handler for URL shortening"""
    json_data = request.get_json()
    if not json_data or 'longURL' not in json_data:
        return jsonify({"error": "Missing longURL in request"}), 400

    # Validate and normalize URL
    url_result = validate_url(json_data['longURL'])
    if not url_result.is_success:
        return jsonify({"error": url_result.error}), 400
    
    long_url = url_result.value

    # Check existing mapping
    existing_short = fetch_small(long_url)
    if existing_short:
        return jsonify({
            "longURL": long_url,
            "shortURL": create_short_url(existing_short)
        })

    # Generate new short code
    code_result = generate_short_code(lambda code: fetch_long(code) is not None)
    if not code_result.is_success:
        return jsonify({"error": code_result.error}), 500

    # Store new mapping
    if not insert(code_result.value, long_url):
        return jsonify({"error": "Failed to store URL mapping"}), 500

    return jsonify({
        "longURL": long_url,
        "shortURL": create_short_url(code_result.value)
    })

@app.route("/api/redirect/<short_code>")
@with_error_handling
def redirect_to(short_code: str):
    """Handler for URL redirection"""
    long_url = fetch_long(short_code)
    if not long_url:
        return jsonify({"error": "Short URL not found"}), 404
    return redirect(long_url)

@app.route("/api/hello/")
def hello():
    """Health check endpoint"""
    return make_response("Hello, there! :)\n", 200)
