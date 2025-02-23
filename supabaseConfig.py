from supabase import create_client, Client
from dotenv import dotenv_values

config = dotenv_values(".env")

url: str = config.get("SUPABASE_URL")
key: str = config.get("SUPABASE_KEY")
numberOfCharacters: int = int(config.get('CHARACTERLIMIT'))
domain: str = str(config.get('DOMAIN'))
randomStringURL: str = str(config.get("RANDOMSTRINGURL"))
supabaseClient: Client = create_client(url, key)
DBTable: str = "SmallToLongUrl"

def insert(small: str, long: str):
    try:
        response = (
            supabaseClient.table(DBTable)
            .insert({"small": small, "long": long})
            .execute()
        )
    except Exception as e:
        return f"insertion of URL: {long} FAILED"
    if len(response.data) > 0:
        return True
    else:
        return False

def fetch(long: str):
    response = (
        supabaseClient.table(DBTable)
        .select("*")
        .eq("long", long)
        .execute().data
    )
    if len(response) > 0:
        return response[0].get("small")
    else:
        return None
    
