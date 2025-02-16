from supabase import create_client, Client
from dotenv import dotenv_values

config = dotenv_values(".env")

url: str = config.get("SUPABASE_URL")
key: str = config.get("SUPABASE_KEY")
numberOfCharacters: int = int(config.get('CHARACTERLIMIT'))
domain: str = str(config.get('DOMAIN'))
supabaseClient: Client = create_client(url, key)
