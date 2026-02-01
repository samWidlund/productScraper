import os
import json
from dotenv import load_dotenv
from apify_client import ApifyClient
from telegramBot import notify_product
from database.database import add_product

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

debug = False

# fetch produkts n notify
items = [] # debug
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    add_product(item['id'], item['marketplace_listing_title'], item['listing_price']['amount'], item['listingUrl'])

    # notify user

    # check if product is already found, then not notify? think the add_product does not add duplicates anyway, but the notification part must be modified
    # items.append(item) # debug

