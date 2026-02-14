import os
from dotenv import load_dotenv
import requests

# load enviroment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("BOT_CHAT_ID")
sent_notifications = 0

def notify_product(title, price, currency, url):
    global sent_notifications

    # stop if tokens not valid
    if not TOKEN or not CHAT_ID:
        print("error: BOT_TOKEN or BOT_CHAT_ID could not be found as environment variables")
        return False

    # telegram message
    text = f"🚨 Product found! 🚨\n{title}\n{price} {currency}\n{url}"
    url_api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    try:
        r = requests.post(url_api, data={"chat_id": CHAT_ID, "text": text}, timeout=10)
        r.raise_for_status() # throw exception when http error
        
        response = r.json()
        if response.get("ok"):
            print("notification sent!")
            sent_notifications += 1
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

def get_sent_notifications():
    return sent_notifications