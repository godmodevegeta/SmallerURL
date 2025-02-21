from supabase import create_client, Client
from dotenv import dotenv_values

config = dotenv_values(".env")

url: str = config.get("SUPABASE_URL")
key: str = config.get("SUPABASE_KEY")
numberOfCharacters: int = int(config.get('CHARACTERLIMIT'))
domain: str = str(config.get('DOMAIN'))
randomStringURL: str = str(config.get("RANDOMSTRINGURL"))
supabaseClient: Client = create_client(url, key)

def insert(small: str, long: str):
    try:
        response = (
            supabaseClient.table("SmallToLongUrl")
            .insert({"small": small, "long": long})
            .execute()
        )
    except Exception as e:
        return f"insertion of URL: {long} FAILED"
    if len(response.data) > 0:
        return True
    else:
        return False

