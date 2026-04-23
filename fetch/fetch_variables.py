import os
from dotenv import load_dotenv

load_dotenv()

# fetch variables from worfklow .env, otherwise uses default value. Change the default value to config when running locally. 
search_term = os.environ.get("SEARCH_TERM") or "salomon adv skin 12" 
min_price_sek = int(os.environ.get("MIN_PRICE_SEK") or 500)
max_price_sek = int(os.environ.get("MAX_PRICE_SEK") or 2000)
min_price_usd = int(os.environ.get("MIN_PRICE_USD") or 50)
max_price_usd = int(os.environ.get("MAX_PRICE_USD") or 200)