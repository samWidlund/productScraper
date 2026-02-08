import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import os
from dotenv import load_dotenv
from apify_client import ApifyClient
from notification.telegramBot import notify_product
from database.database import SupabaseClient

load_dotenv()
APIFY_TOKEN=os.getenv("APIFY_TOKEN")
client = ApifyClient(APIFY_TOKEN)

# define actor input
run_input = {
    "startUrls": [
        { "url": "https://www.facebook.com/marketplace/110976692260411/search?query=arcteryx" }, # arcteryx in sweden
    ],
    "resultsLimit": 20,
}

# run actor
run = client.actor("U5DUNxhH3qKt5PnCf").call(run_input=run_input)

# initialize supabase client
db = SupabaseClient()
db.login()

# counter variables
total_items = 0
new_items = 0

print("Fetching products from Facebook Marketplace...")

# fetch produkts n notify
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f"Found item: {item['marketplace_listing_title']} at {item['listing_price']['amount']}")
    total_items += 1

    if db.is_new_product(item['id']): # notify user and and product to db if new
        db.add_product(item['id'], item['marketplace_listing_title'], item['listing_price']['amount'], item['listingUrl'])
        notify_product(item['marketplace_listing_title'], item['listing_price']['amount'], item['listingUrl'])
        new_items += 1

print(f"Total items found: {total_items}")
print(f"New items found: {new_items}")