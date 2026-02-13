import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from notification.telegramBot import notify_product
from fetch.ebay.ebay_api import EbayAPI
from database.database import SupabaseClient
import fetch.ebay.config as config

## inital supabase client
db = SupabaseClient()
db.login()

# counter variables
total_items = 0
new_items = 0

ebay = EbayAPI(
    client_id=config.EBAY_CLIENT_ID,
    client_secret=config.EBAY_CLIENT_SECRET,
    sandbox=config.EBAY_SANDBOX
)

products = ebay.search(
    query="Arcteryx",
    max_price=100,
    marketplace='US'
)

# fetch products n notify
print("Fetching products from eBay Marketplace...")
for product in products:
    print(f"Found item: {product['title']} at {product['price']} {product['currency']} id: {product['id']}")
    total_items += 1

    if db.is_new_product(product['id']): # notify user and and product to db if new
        db.add_product(product['id'], product['title'], product['price'], product['url'])
        notify_product(product['title'], product['price'], product['url'])
        new_items += 1

print(f"Total items found: {total_items}")
print(f"New items found: {new_items}")
