import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

APIFY_TOKEN=os.getenv("APIFY_TOKEN")

# Initialize the ApifyClient with your API token
client = ApifyClient(APIFY_TOKEN)

# Prepare the Actor input
run_input = {
    "startUrls": [
        { "url": "https://www.facebook.com/marketplace/110976692260411/search?query=arcteryx" },
    ],
    "resultsLimit": 20,
}

# Run the Actor and wait for it to finish
run = client.actor("U5DUNxhH3qKt5PnCf").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)