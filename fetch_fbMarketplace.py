import os
import json
from dotenv import load_dotenv
from apify_client import ApifyClient
from telegramBot import notify_product
from database.database import add_product, is_new_product, init_database

load_dotenv()
APIFY_TOKEN=os.getenv("APIFY_TOKEN")
client = ApifyClient(APIFY_TOKEN)

init_database()

run_input = {
    "startUrls": [
        { "url": "https://www.facebook.com/marketplace/110976692260411/search?query=arcteryx" }, # arcteryx in sweden
    ],
    "resultsLimit": 20,
}

# run actor
run = client.actor("U5DUNxhH3qKt5PnCf").call(run_input=run_input)

debug = False

# fetch produkts n notify
items = [] # debug
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    items.append(item) # debug
    
    # add product to db if new
    if is_new_product(item['id']):
        # Try to add product first, only notify if successfully added
        if add_product(item['id'], item['marketplace_listing_title'], item['listing_price']['amount'], item['listingUrl']):
            # send notification
            if not debug:
                notify_product(item['marketplace_listing_title'], item['listing_price']['amount'], item['listingUrl'])
            else:
                print(f"NY: {item['marketplace_listing_title']} - {item['listing_price']['amount']} SEK")
        else:
            print(f"Failed to add product to database: {item['marketplace_listing_title']}")
    else:
        print(f"match in database, product already found: {item['marketplace_listing_title']}")

## UNCOMMENT TO DEBUG ## 
# with open("output/fb_marketplace.json", "w") as f:
#     json.dump(items, f, indent=4)

