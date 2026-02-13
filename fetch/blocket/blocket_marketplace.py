# https://blocket-api.se/examples/

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import os
from dotenv import load_dotenv
from apify_client import ApifyClient
from notification.telegramBot import notify_product
from database.database import SupabaseClient
from blocket_api import (
    BlocketAPI,
    Category,
    SortOrder,
    CarColor,
    CarModel,
    CarSortOrder,
    CarTransmission,
    Location,
)

## inital supabase client
# db = SupabaseClient()
# db.login()

# # counter variables
# total_items = 0
# new_items = 0

## blocket API client


api = BlocketAPI()

# search all of blocket
response = api.search(
    "jacka",
    sort_order=SortOrder.PRICE_ASC,
    locations=[Location.STOCKHOLM, Location.UPPSALA],
    category=Category.FRITID_HOBBY_OCH_UNDERHALLNING,
)

# The actual products are in the 'docs' key
products = response['docs']

for product in products:
    heading = product.get('heading', 'N/A')
    price = product.get('price', {})
    amount = price.get('amount', 'N/A')
    currency = price.get('price_unit', 'N/A')
    product_id = product.get('id', 'N/A')
    location = product.get('location', 'N/A')
    url = product.get('canonical_url', 'N/A')
    
    print(f"Title: {heading}")
    print(f"Price: {amount} {currency}")
    print(f"Location: {location}")
    print(f"ID: {product_id}")
    print(f"URL: {url}\n")
    # total_items += 1