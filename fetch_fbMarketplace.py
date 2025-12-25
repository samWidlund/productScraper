import os
from dotenv import load_dotenv
from apify_client import ApifyClient
from telegramBot import notify_product
import json

load_dotenv()
APIFY_TOKEN=os.getenv("APIFY_TOKEN")
client = ApifyClient(APIFY_TOKEN)

run_input = {
    "startUrls": [
        { "url": "https://www.facebook.com/marketplace/110976692260411/search?query=arcteryx" }, # arcteryx in sweden
    ],
    "resultsLimit": 20,
}

# run actor
run = client.actor("U5DUNxhH3qKt5PnCf").call(run_input=run_input)

# fetch produkts n notify
items = [] # debug
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
    items.append(item) # debug
    notify_product(item['marketplace_listing_title'], item['listing_price']['amount'], item['listingUrl'])

# write output to json file for debug
with open("output/fb_marketplace.json", "w") as f:
    json.dump(items, f, indent=4)

