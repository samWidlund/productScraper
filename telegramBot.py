import os
from dotenv import load_dotenv
import requests
import sys

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("BOT_CHAT_ID")

def notify_product(title, price, url):
    if not TOKEN or not CHAT_ID:
        print("Fel: TOKEN eller CHAT_ID är inte satta som miljövariabler")
        return False
    
    text = f"🔥 Ny produkt hittad!\n\n{title}\nPris: {price} kr\n{url}"
    url_api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    try:
        r = requests.post(url_api, data={"chat_id": CHAT_ID, "text": text}, timeout=10)
        r.raise_for_status()  # throw exception when http error
        
        response = r.json()
        if response.get("ok"):
            print("message sent!")
            return True
        else:
            print(f"wrong answer from Telegram API: {response}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"network error: {e}")
        return False
    except Exception as e:
        print(f"unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = notify_product("Arc'teryx Beta LT Jacket", 999, "https://example.com/arcteryx")
    if not success:
        sys.exit(1)
 