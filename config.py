import os
from dotenv import load_dotenv

load_dotenv()
EBAY_CLIENT_ID = os.getenv('EBAY_CLIENT_ID')
EBAY_CLIENT_SECRET = os.getenv('EBAY_CLIENT_SECRET')
EBAY_SANDBOX = True  # Change to False for production

if EBAY_CLIENT_ID and EBAY_CLIENT_SECRET:
    print("Success fetching ebay enviroment variables")
else:
    ("Error fetching ebay enviroment variables")
