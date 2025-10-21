# script to fetch products form platforms n notify user via telegramBot

from telegramBot import notify_product # function to notify user
from ebay_api import EbayAPI
import config

ebay = EbayAPI(
    client_id=config.EBAY_CLIENT_ID,
    client_secret=config.EBAY_CLIENT_SECRET,
    sandbox=config.EBAY_SANDBOX
)

# search n print result
products = ebay.search(
    query="phone",
    max_price=100000,
    marketplace='US'
)

debug = True
price_cap = 19 # notification is sent to user when found product meets or is below this price

print("\nproducts found:")
for product in products:

    if debug: # if set to True, print all products found
        print(f"\n{product['title']} - {product['price']} {product['currency']} {product['url']}")

    if not debug and float(product['price']) <= price_cap:
        notify_product(product['title'], product['price'], product['url'])
