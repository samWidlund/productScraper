# alt use https://apify.com/ecomscrape/tradera-product-search-scraper/api/python

from tradera_api.tradera import TraderaAPI, BASE_URL, AuctionType
import json

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
    _id = pick(item, "id", "listingId", "itemId")

    # title
    title = pick(item, "title", "name", "listingTitle") or ""

    # price and currency
    price_block = pick(item, "price", "currentPrice", "buyNowPrice")
    if isinstance(price_block, dict):
        price = pick(price_block, "amount", "value")
        currency = pick(price_block, "currency", "currencyCode", "currencyIso") or "SEK"
    else:
        price = price_block
        currency = pick(item, "currency", "currencyCode") or "SEK"

    # url
    url = pick(item, "url", "itemUrl", "listingUrl", "link", "permalink")
    if not url and _id:
        url = f"{BASE_URL}item/{_id}"

    return (_id, title, price, currency, url)


all_printed = 0
for st in search_types:
    res = api.search(query="Arcteryx", price=(50, 10000), auction_type=st)
    items = find_items(res)
    if not items:
        print(f"No items found for type {st} — showing a part of response:")
        print(json.dumps(res, indent=2, ensure_ascii=False)[:2000])
        continue

    for it in items[:50]:
        base = list(extract_simple(it))
        # append auction type string
        base.append(st.name)
        print(tuple(base))
        all_printed += 1

print(f"Printed {all_printed} items across types: {[t.name for t in search_types]}")