import os
from dotenv import load_dotenv

load_dotenv()
EBAY_CLIENT_ID = os.getenv('EBAY_CLIENT_ID')
EBAY_CLIENT_SECRET = os.getenv('EBAY_CLIENT_SECRET')
EBAY_SANDBOX = False  # false = production

if not EBAY_CLIENT_ID or not EBAY_CLIENT_SECRET:
    raise RuntimeError("Missing EBAY_CLIENT_ID or EBAY_CLIENT_SECRET in environment")
