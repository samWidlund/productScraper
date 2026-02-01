import requests
import supabase
from supabase import auth
import os
from dotenv import load_dotenv

load_dotenv()

class SupabaseClient:
    def __init__(self):
        self.supabase_key = os.environ.get('SUPABASE_KEY')
        self.supabase_url = os.environ.get('SUPABASE_URL')

        if not self.supabase_key or not self.supabase_url:
            raise ValueError("Missing supabase_key or supabase_url environment variables")
        
        self.client = supabase.create_client(self.supabase_url, self.supabase_key)

    def add_product(self, itemid: str, title: str, price: float, url: str):

        user = supabase.auth.get_user()  
        user_id =  user['data']['user']['id']
        # det funkade innan jag lade till rls, måste lösa med owner_id nu

        response = self.client.table("products").insert({
            "itemid": itemid,
            "title": title,
            "price": price,
            "url": url,
            "owner_id": user_id
        }).execute()
        return response

    def is_new_product(self, itemid: str):
        response = self.client.table("products").select("*").eq("itemid", itemid).execute()
        print(f"Database check for itemid {itemid}, found {len(response.data)} records.")
        return len(response.data) == 0
