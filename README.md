# Automated product scraping tool for resellers

Automated marketplace scraper that monitors online platforms for products and notifies users via Telegram push notification. Combining multiple scraper APIs into one simple easy-to-use applicaton.

## Background

After years of reselling clothes, I grew tired of manually searching marketplaces for the best deals. Instead of spending hours doing it myself, I built a system that automates the process and lets software handle the work for me.

## Features

- Scheduled product fetching across multiple marketplaces
- Real-time Telegram notifications
- Product filtering by price and keyword
- Database integration preventing repeated notifications

## Supported Platforms

| Platform | Status |
|----------|--------|
| Facebook Marketplace | **Working** |
| eBay | **Working** |
| Blocket | **Working** |
| Tradera | **Working** |
| Vinted | **Working** |
| Depop | Planned |

## Requirements

- Python 3.10+
- eBay API credentials
- Apify API (Facebook scraper)
- Supabase account
- Telegram Bot token
- Github account (Actions)

## Setup

### Installation

1. Clone the repository
2. Create and activate a virtual environment

   - Linux / macOS (bash / zsh / fish)
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

   - Windows (PowerShell)
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

   > **Note:** Include `.venv/` in `.gitignore` to avoid committing the environment.

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file with your credentials:
   ```env
   BOT_TOKEN=your_telegram_token
   BOT_CHAT_ID=your_chat_id
   EBAY_CLIENT_ID=your_ebay_id
   EBAY_CLIENT_SECRET=your_ebay_secret
   APIFY_TOKEN=your_apify_token
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   SUPABASE_EMAIL=your_email
   SUPABASE_PASSWORD=your_password
   ```

### Running

**Locally:**

- Windows

```powershell
python fetch/facebook/fb_marketplace.py
```

- Linux / macOS

```bash
python3 fetch/facebook/fb_marketplace.py
```

**Automated:**
Configured to run every 3 hours via github actions. See `.github/workflows/workflow.yml` \
> **Note:** Make sure to include .env variables in repository secrets. 

### Scraping specifications
To specify what criteria the scraper should match, configure the variables in `fetch/fetch_variables.py`:
```python
search_term = "Arcteryx" # search word used when scraping each marketplace
price_cap_sek = 2000 # swedish listings
price_cap_USD = 200 # non swedish listings
```

## Project Structure

```
├── fetch/                    # Marketplace scrapers
│   ├── blocket/
│   ├── depop/
│   ├── ebay/
│   ├── facebook/
│   ├── tradera/
│   └── vinted/
├── database/                 # Database operations
├── publish/                  # Publishing utilities (currently empty)
├── notification/             # User bot notificiation       
└── README.md
```

## References
[EbayAPI](https://developer.ebay.com/develop) \
[TraderaAPI](https://pypi.org/project/tradera_api/) \
[BlocketAPI](https://blocket-api.se/) \
[FacebookAPI](https://apify.com/apify/facebook-pages-scraper) \
[VintedAPI](https://vinted-api.se/)

## License

MIT
