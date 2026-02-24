from vinted_scraper import VintedScraper
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import os
from dotenv import load_dotenv
from notification.telegramBot import notify_product, get_sent_notifications
from database.database import SupabaseClient

load_dotenv()

db = SupabaseClient()
db.login()

total_items = 0
new_items = 0

MAX_PRICE_SEK = 1000

domain_currency = {
    "vinted.de": ("Tyskland", "EUR", 11.5),
    "vinted.pl": ("Polen", "PLN", 2.4),
    "vinted.fi": ("Finland", "EUR", 11.5),
    "vinted.dk": ("Danmark", "DKK", 1.55),
    "vinted.se": ("Sverige", "SEK", 1.0),
}

european_domains = list(domain_currency.keys())

search_query = os.getenv("VINTED_SEARCH_QUERY", "arcteryx")

print(f"Searching for '{search_query}' across {len(european_domains)} European Vinted domains...")

for domain in european_domains:
    try:
        country, currency_code, rate_to_sek = domain_currency[domain]
        price_to = int(MAX_PRICE_SEK / rate_to_sek)
        
        print(f"\nFetching {country} ({domain}) - max price: {price_to} {currency_code}...")
        scraper = VintedScraper(f"https://www.{domain}")
        items = scraper.search({"search_text": search_query, "price_to": price_to})
        
        for item in items:
            price_sek = float(item.price) * rate_to_sek if item.price else 0.0
            
            if price_sek > MAX_PRICE_SEK:
                continue
                
            total_items += 1
            print(f"  {item.title} - {item.price} {item.currency} (~{price_sek:.0f} SEK) - {item.url}")

            item_id = str(item.id) if item.id else None
            title = item.title or ""
            price = float(item.price) if item.price else 0.0
            currency = item.currency or ""
            url = item.url or ""

            if item_id and db.is_new_product("vinted_products", item_id):
                db.add_product("vinted_products", item_id, title, price, currency, url)
                notify_product(item.title, item.price, item.currency, item.url)
                new_items += 1
                
    except Exception as e:
        print(f"  Error fetching {domain}: {e}")

sent_notifications = get_sent_notifications()
print(f"Total items found: {total_items}")
print(f"New items found: {new_items}")
print(f"Sent notifications: {sent_notifications}")
