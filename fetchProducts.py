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

print("\nproducts found:")
for product in products:
    print(f"{product['title']} - {product['price']} {product['currency']} {product['url']}")