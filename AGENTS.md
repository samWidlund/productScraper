# AGENTS.md - Agentic Coding Guidelines

This file provides guidelines for AI agents operating in this repository.

## Project Overview

ProductScraper is an automated marketplace scraper that monitors online platforms (Facebook, eBay, Blocket, Tradera, Vinted, Depop) for products and notifies users via Telegram push notifications. It uses Python with Supabase for database storage.

## Build, Lint, and Test Commands

### Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run individual scrapers
python fetch/vinted/vinted_marketplace.py
python fetch/ebay/ebay_marketplace.py
python fetch/blocket/blocket_marketplace.py
python fetch/tradera/tradera_marketplace.py
python fetch/facebook/fb_marketplace.py
```

### Linting and Type Checking

```bash
# Lint with ruff (installed in .venv)
.venv/bin/ruff check .

# Type check with mypy (installed in .venv)
.venv/bin/mypy .
```

### Testing

```bash
# Run all tests with pytest (installed in .venv)
.venv/bin/pytest

# Run a single test file
.venv/bin/pytest tests/test_filename.py

# Run a specific test function
.venv/bin/pytest tests/test_filename.py::test_function_name

# Run tests matching a pattern
.venv/bin/pytest -k "test_pattern"
```

Note: Currently there are no formal tests in `tests/`. The file `testing.py` at root is a scratchpad for manual testing, not a test suite.

## Code Style Guidelines

### General Style

- Use **Python 3.10+** compatibility
- Follow PEP 8 style guide
- Use **4 spaces** for indentation (not tabs)
- Maximum line length: **120 characters** (soft limit)
- Use snake_case for variables, functions, and module names
- Use PascalCase for class names
- Use UPPER_SNAKE_CASE for constants

### Imports

Organize imports in the following order (separate with blank lines between groups):

1. Standard library imports (`os`, `sys`, `pathlib`, `requests`, etc.)
2. Third-party imports (`supabase`, `dotenv`, `vinted_scraper`, etc.)
3. Local/application imports (from `notification.`, `database.`, `fetch.`)

Example:
```python
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests
from dotenv import load_dotenv

from notification.telegramBot import notify_product
from database.database import SupabaseClient
from fetch.fetch_variables import search_term
```

Note: When importing from sibling modules, use `sys.path.insert()` to add the project root to the path.

### Type Hints

- Add type hints for function parameters and return types when beneficial for clarity
- Use `Optional[X]` instead of `X | None` for Python 3.10 compatibility
- Example:
```python
def add_product(self, table: str, itemid: str, title: str, price: float, currency: str, url: str) -> dict:
```

### Naming Conventions

- **Variables**: `snake_case` (e.g., `total_items`, `search_term`)
- **Functions**: `snake_case` (e.g., `notify_product`, `get_sent_notifications`)
- **Classes**: `PascalCase` (e.g., `SupabaseClient`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `BOT_TOKEN`, `MAX_RETRIES`)
- **Modules/Files**: `snake_case` (e.g., `telegramBot.py`, `ebay_api.py`)

### Error Handling

- Use try/except blocks for network calls and external API interactions
- Catch specific exceptions when possible (`requests.exceptions.RequestException`)
- Always log errors with descriptive messages using `print()`
- Return `False` or `None` on failure rather than raising in most cases
- Example:
```python
try:
    r = requests.post(url_api, data={"chat_id": CHAT_ID, "text": text}, timeout=10)
    r.raise_for_status()
    return True
except requests.exceptions.RequestException as e:
    print(f"network error: {e}")
    return False
except Exception as e:
    print(f"unexpected error: {e}")
    return False
```

### Logging

- Use `print()` for logging output (current convention)
- Include descriptive messages with context
- Example: `print(f"Total items found: {total_items}")`

### Database Operations

- Use the `SupabaseClient` class from `database/database.py` for all DB operations
- Always call `db.login()` after initializing the client
- Use `db.is_new_product()` before inserting to avoid duplicates
- Table names: `vinted_products`, `ebay_products`, etc.

### Environment Variables

- Never hardcode credentials in source code
- Use `os.environ.get()` or `os.getenv()` to read from environment
- Use `load_dotenv()` to load from `.env` file
- Validate required env vars at startup and raise `ValueError` if missing

Example:
```python
load_dotenv()

class SupabaseClient:
    def __init__(self):
        self.supabase_key = os.environ.get('SUPABASE_KEY')
        self.supabase_url = os.environ.get('SUPABASE_URL')
        
        if not self.supabase_key or not self.supabase_url:
            raise ValueError("Missing supabase_key or supabase_url environment variables")
```

### File Organization

```
productScraper/
├── fetch/                    # Marketplace scrapers
│   ├── blocket/
│   ├── depop/
│   ├── ebay/
│   │   ├── ebay_api.py       # API wrapper
│   │   ├── ebay_marketplace.py  # Main scraper entry point
│   │   └── config.py         # eBay-specific config
│   ├── facebook/
│   ├── tradera/
│   ├── vinted/
│   └── fetch_variables.py    # Search parameters
├── database/
│   └── database.py           # Supabase client
├── notification/
│   └── telegramBot.py        # Telegram notification functions
├── publish/                  # Publishing utilities
├── testing.py                # Manual testing scratchpad
└── requirements.txt
```

### Marketplace Scraper Pattern

Each marketplace scraper should:
1. Initialize `SupabaseClient` and call `login()`
2. Set up the marketplace-specific scraper/API
3. Iterate through products
4. Check if product is new with `db.is_new_product()`
5. Add product to DB with `db.add_product()`
6. Send notification with `notify_product()` (if applicable)
7. Print summary statistics

### Adding a New Marketplace

1. Create directory under `fetch/` (e.g., `fetch/newmarketplace/`)
2. Create `newmarketplace_marketplace.py` as the main entry point
3. Follow the scraper pattern above
4. Add any required API/config files in the directory
5. Update `.github/workflows/workflow.yml` if running in CI/CD
6. Add to the supported platforms list in `README.md`

### Git Workflow

- Create feature branches for new functionality
- Run ruff and mypy before committing
- Do not commit `.env` files or credentials
- The `.gitignore` excludes `.venv/`, `__pycache__/`, and `.env`

### Dependencies

Key dependencies (see `requirements.txt`):
- `python-dotenv` - Environment variable loading
- `requests` - HTTP requests
- `supabase` - Database client
- `apify_client` - Facebook Marketplace scraping
- `blocket-api` - Blocket scraping
- `vinted_scraper` - Vinted scraping
- `tradera_api` - Tradera scraping (separate job in CI due to httpx version conflict)

### CI/CD

GitHub Actions workflow (`.github/workflows/workflow.yml`):
- Runs on Python 3.14 for most scrapers
- Tradera job runs separately on Python 3.11 (httpx version conflict)
- Secrets are stored in GitHub environment `telegramApi`
