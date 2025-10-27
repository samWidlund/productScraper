# script to fetch products form platforms n notify user via telegramBot

from telegramBot import notify_product
from ebay_api import EbayAPI
from database import add_product, is_new_product
import config

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

debug = False

print(f"\nproducts found: {len(products)}")

for product in products:

    # add product to db if new
    if is_new_product(product['id']):
        add_product(product['id'], product['title'], product['price'], product['url'])
        
        # send notification
        if not debug:
            notify_product(product['title'], product['price'], product['url'])
        else:
            print(f"NY: {product['title']} - {product['price']} {product['currency']}")
    else:
        print(f"match in database, product already found: {product['title']}")
