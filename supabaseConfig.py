from supabase import create_client, Client
from dotenv import dotenv_values
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

config = dotenv_values(".env")

url: str = config.get("SUPABASE_URL")
key: str = config.get("SUPABASE_KEY")
numberOfCharacters: int = int(config.get('CHARACTERLIMIT'))
domain: str = str(config.get('DOMAIN'))
randomStringURL: str = str(config.get("RANDOMSTRINGURL"))
supabaseClient: Client = create_client(url, key)
DBTable: str = "SmallToLongUrl"

def insert(small: str, long: str):
    logger.info("Initiating Call to Supabase")
    try:
        response = (
            supabaseClient.table(DBTable)
            .insert({"small_code": small, "long": long})
            .execute()
        )
    except Exception as e:
        return f"insertion of URL: {long} FAILED"
    if len(response.data) > 0:
        logger.info(f"Insertion of {response.data} complete in Suapabase")
        return True
    else:
        return False

def fetch_small(long: str):
    logger.info("Initiating Call to Supabase")
    response = (
        supabaseClient.table(DBTable)
        .select("*")
        .eq("long_code", long)
        .execute().data
    )
    if len(response) > 0:
        logger.info(f"Call to Supabase successful with response {response.data}")
        return response[0].get("small_code")
    else:
        return None
    
def fetch_long(small: str):
    logger.info("Initiating Call to Supabase")
    response = (
        supabaseClient.table(DBTable)
        .select("*")
        .eq("small_code", small)
        .execute().data
    )
    if len(response) > 0:
        logger.info(f"Call to Supabase successful with response {response.data}")
        return response[0].get("long_code")
    else:
        return None

