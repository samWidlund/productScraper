# https://blocket-api.se/examples/

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import os
from dotenv import load_dotenv
from notification.telegramBot import notify_product
from database.database import SupabaseClient
from blocket_api import (
    BlocketAPI,
    Category, ## optional category filter
    SortOrder,
    Location,
)

## inital supabase client
db = SupabaseClient()
db.login()

# # counter variables
total_items = 0
new_items = 0

## blocket API client
api = BlocketAPI()

# all swedish region blocket locations
BLEKINGE = Location.BLEKINGE
DALARNA = Location.DALARNA
GOTLAND = Location.GOTLAND
GAVLEBORG = Location.GAVLEBORG
HALLAND = Location.HALLAND
JAMTLAND = Location.JAMTLAND
JONKOPING = Location.JONKOPING
KALMAR = Location.KALMAR
KRONOBERG = Location.KRONOBERG
NORRBOTTEN = Location.NORRBOTTEN
SKANE = Location.SKANE
STOCKHOLM = Location.STOCKHOLM
SODERMANLAND = Location.SODERMANLAND
UPPSALA = Location.UPPSALA
VARMLAND = Location.VARMLAND
VASTERBOTTEN = Location.VASTERBOTTEN
VASTERNORRLAND = Location.VASTERNORRLAND
VASTMANLAND = Location.VASTMANLAND
VASTRA_GOTALAND = Location.VASTRA_GOTALAND
OREBRO = Location.OREBRO
OSTERGOTLAND = Location.OSTERGOTLAND

all_locations = [
    BLEKINGE, DALARNA, GOTLAND, GAVLEBORG, HALLAND, JAMTLAND, JONKOPING,
    KALMAR, KRONOBERG, NORRBOTTEN, SKANE, STOCKHOLM, SODERMANLAND, UPPSALA,
    VARMLAND, VASTERBOTTEN, VASTERNORRLAND, VASTMANLAND, VASTRA_GOTALAND,
    OREBRO, OSTERGOTLAND
]

# search all of blocket
response = api.search(
    "Arcteryx",
    sort_order=SortOrder.PRICE_ASC,
    locations=all_locations
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
    total_items += 1

    if db.is_new_product(product_id): # notify user and and product to db if new
        db.add_product(product_id, heading, amount, url)
        notify_product(heading, amount, url)
        new_items += 1

print(f"Total items found: {total_items}")
print(f"New items found: {new_items}")

