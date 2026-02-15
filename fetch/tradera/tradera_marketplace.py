# alt use https://apify.com/ecomscrape/tradera-product-search-scraper/api/python

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tradera_api.tradera import TraderaAPI, BASE_URL, AuctionType
import json
from notification.telegramBot import notify_product, get_sent_notifications
from database.database import SupabaseClient

api = TraderaAPI()

search_types = [AuctionType.auction, AuctionType.buy_now]

def find_items(response: dict):
    for k in ("items", "results", "hits", "itemsResult", "data"):
        v = response.get(k)
        if isinstance(v, list):
            return v
    # fallback: first list value
    for v in response.values():
        if isinstance(v, list):
            return v
    return []

def pick(item: dict, *keys):
    for k in keys:
        if k in item:
            return item[k]
    return None

# items can be using different keys for same data, so try different options for each field
def extract_simple(item: dict):
    # id
    _id = pick(item, "id", "listingId", "itemId", "Id", "ItemId")
    
    # title - try more variations
    title = pick(item, 
                 "title", "name", "listingTitle", "itemName", 
                 "shortDescription", "heading", "Title", "Name") or ""
    
    # If still empty, try nested structures
    if not title and "item" in item:
        title = pick(item["item"], "title", "name", "Title") or ""
    
    # price and currency
    price_block = pick(item, "price", "currentPrice", "buyNowPrice", "startingPrice")
    if isinstance(price_block, dict):
        price = pick(price_block, "amount", "value", "Amount", "Value")
        currency = pick(price_block, "currency", "currencyCode", "currencyIso") or "SEK"
    else:
        price = price_block
        currency = pick(item, "currency", "currencyCode") or "SEK"
    
    # url
    url = pick(item, "url", "itemUrl", "listingUrl", "link", "permalink", "Url")
    if not url and _id:
        url = f"{BASE_URL}item/{_id}"
    
    return (_id, title, price, currency, url)


# initialize supabase client and counters
db = SupabaseClient()
db.login()

total_items = 0
new_items = 0

for st in search_types:
    res = api.search(query="Arcteryx", price=(0, 2000), auction_type=st)
    items = find_items(res)
    if not items:
        print(f"No items found for type {st.name} — showing a part of response:")
        print(json.dumps(res, indent=2, ensure_ascii=False)[:2000])
        continue

    for it in items[:50]:
        total_items += 1
        _id, title, price, currency, url = extract_simple(it)
        print(f"Found item: {title} at {price} {currency} ({url})")

        # normalize price to float when possible
        try:
            price_val = float(price) if price is not None else None
        except Exception:
            price_val = None

        # check DB and add + notify if new
        if db.is_new_product("tradera_products", str(_id)):
            db.add_product("tradera_products", str(_id), title, price_val, currency or "SEK", url)
            notify_product(title, price_val, currency or "SEK", url, auction_type=st.name)
            new_items += 1

print(f"Total items found: {total_items}")
print(f"New items found: {new_items}")
print(f"Sent notifications: {get_sent_notifications()}")