import supabase
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

class SupabaseClient:
    def __init__(self):
        self.supabase_key = os.environ.get('SUPABASE_KEY')
        self.supabase_url = os.environ.get('SUPABASE_URL')

        if not self.supabase_key or not self.supabase_url:
            raise ValueError("Missing supabase_key or supabase_url environment variables")
        
        self.Client = create_client(self.supabase_url, self.supabase_key)

    def login (self):
        response = self.Client.auth.sign_in_with_password(
            {
                "email": os.environ.get('SUPABASE_EMAIL'),
                "password": os.environ.get('SUPABASE_PASSWORD'),
            }
        )

        self.user_id = response.user.id

    def add_product(self, itemid: str, title: str, price: float, url: str):

        response = self.Client.table("products").insert({
            "itemid": itemid,
            "title": title,
            "price": price,
            "url": url,
            "user_id": self.user_id
        }).execute()
        return response

    def is_new_product(self, itemid: str):
        response = self.Client.table("products").select("*").eq("itemid", itemid).execute()
        print(f"Database check for itemid {itemid}, found {len(response.data)} records.")
        return len(response.data) == 0

