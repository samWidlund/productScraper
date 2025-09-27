# script to fetch products form platforms n notify user via telegramBot

# https://github.com/kyleronayne/marketplace-api
# https://github.com/scrapy/scrapy
# https://github.com/D4Vinci/Scrapling

import requests
from dotenv import load_dotenv
from telegramBot import notify_product

load_dotenv()

runProgram = True
notify = "False"
# json placeholder
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print("Mock data:", response.json())

while runProgram:
    notify = input("Enter true to send message\n").lower()
    print(notify)
    if notify == "true":
        notify_product("GOOD SHIT!", "500 kr", "https://example.com") # function to call telegram bot
    if notify == "break":
        runProgram = False 