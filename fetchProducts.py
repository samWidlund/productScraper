# script to fetch products form platforms n notify user via telegramBot

from telegramBot import notify_product
from ebay_api import EbayAPI
import config

ebay = EbayAPI(
    client_id=config.EBAY_CLIENT_ID,
    client_secret=config.EBAY_CLIENT_SECRET,
    sandbox=config.EBAY_SANDBOX
)

products = ebay.search(
    query="arcteryx jacket",
    max_price=15, # price cap is mentioned twice?
    marketplace='US' # test change from US
)

debug = False

print("\nproducts found:")
for product in products:

    if debug: # if set to True, print all products found
        print(f"\n{product['title']} - {product['price']} {product['currency']} {product['url']}")

    if not debug:
        notify_product(product['title'], product['price'], product['url'])
