import requests
import os
from dotenv import load_dotenv

load_dotenv()
supabase_key = os.getenv('DB_TOKEN')
supabase_url = os.getenv('URL_SUPABASE')

# När du hittar en ny produkt:
response = requests.post(
    f"{supabase_url}/rest/v1/products",
    headers={
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    },
    json={
        "itemid": "test123",
        "title": "arawdaw",
        "price": "999",
        "url": "google.com"
    }
)