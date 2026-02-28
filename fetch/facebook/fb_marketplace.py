import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import os
from dotenv import load_dotenv
from apify_client import ApifyClient
from notification.telegramBot import notify_product, get_sent_notifications
from database.database import SupabaseClient
from fetch.fetch_variables import search_term

load_dotenv()
APIFY_TOKEN=os.getenv("APIFY_TOKEN")
client = ApifyClient(APIFY_TOKEN)

# define actor input
run_input = {
    "startUrls": [
        { "url": f"https://www.facebook.com/marketplace/110976692260411/search?query={search_term}" }, # arcteryx in sweden
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

    if db.is_new_product("facebook_products", item['id']): # notify user and and product to db if new
        db.add_product("facebook_products", item['id'], item['marketplace_listing_title'], item['listing_price'], item['amount'], item['listingUrl'])
        notify_product(item['marketplace_listing_title'], item['listing_price'], item['amount'], item['listingUrl'])
        new_items += 1

sent_notifications = get_sent_notifications()
print(f"Total items found: {total_items}")
print(f"New items found: {new_items}")
print(f"Sent notifications: {sent_notifications}")