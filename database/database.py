import requests
import os

supabase_key = os.environ.get('SUPABASE_KEY')
supabase_url = os.environ.get('SUPABASE_URL')

if not supabase_key or not supabase_url:
    raise ValueError("Missing supabase_key or supabase_url environment variables")


def add_product(itemid: str, title: str, price: float, url: str):
    response = requests.post(
        f"{supabase_url}/rest/v1/products",
        headers={
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates"
        },
        json={
            "itemid": itemid,
            "title": title,
            "price": price,
            "url": url
        }
    )