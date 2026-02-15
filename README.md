# Automated product scraping tool for resellers

Automated marketplace scraper that monitors online platforms for products and notifies users via Telegram push notification.

## Features

- Scheduled product fetching across multiple marketplaces
- Real-time Telegram notifications
- Product filtering by price and keywords
- **Planned**: Auto-fill account forms with product info
- **Planned**: Multi-platform product publishing

## Supported Platforms

| Platform | Status |
|----------|--------|
| Facebook Marketplace | **Working** |
| eBay | **Working** |
| Blocket | **Working** |
| Tradera | In development |
| Vinted | Planned |

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

**Automated via GitHub Actions:**
Configured to run every 3 hours. See `.github/workflows/workflow.yml`
> **Note:** When automated, make sure to include .env variables in repository secrets. 

## Project Structure

```
├── fetch/                    # Product fetchers
│   ├── facebook/
│   └── ebay/
├── database/                 # Database operations
├── publish/                  # Publishing utilities
├── notification/             # Bot notification       
└── README.md
```

## License

MIT
