from vinted_scraper import VintedScraper
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv
from notification.telegramBot import notify_product, get_sent_notifications
from database.database import SupabaseClient

## inital supabase client
db = SupabaseClient()
db.login()

# # counter variables
total_items = 0
new_items = 0

scraper = VintedScraper("https://www.vinted.com")
se_scraper = VintedScraper("https://www.vinted.se")
items = scraper.search({"search_text": "arcteryx"})
se_items = se_scraper.search({"search_text": "arcteryx"})
items.extend(se_items)

print(f"Fetching vinted marketplace... ")
for item in items:
    total_items += 1
    print(f"{item.title} - {item.price} {item.currency} - {item.url} - {item.id}")

    if db.is_new_product("vinted_products", item.id):
        db.add_product("vinted_products", item.id, item.title, item.price, item.currency, item.url)
        notify_product(item.title, item.price, item.currency, item.url)
        new_items += 1

sent_notifications = get_sent_notifications()
print(f"Total items found: {total_items}")
print(f"New items found: {new_items}")
print(f"Sent notifications: {sent_notifications}")