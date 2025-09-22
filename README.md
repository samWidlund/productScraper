# Tool to quickly find the best prices and simplify reselling

# Main purpose/plan
- auto fetch products based on price, notify user via phone push notification.
- ADDITIONAL, insert info about product -> auto fill account form? 
- ADDITIONAL, insert info about product -> upload product on multiple platforms at once

## platforms 
- facebook Marketplace
- facebook 
- ebay
- tradera
- blocket
- vinted?
- plick?

# backlog
- [x] working telegram api bot using python
- [x] setup github actions
- [x] working workflow to run the python bot script
- [ ] begin working with scraping tool
    - [ ] research - api? selenium? scrapy?
    - [ ] run workflow on schedule, if product found -> trigger telegramBot 
    - [ ] ai to analyze products?
- [ ] input product info in telegram chat -> publish product on platforms?
    - [ ] ebay API, do the rest semi automatic?

# ideas
https://github.com/kyleronayne/marketplace-api
https://github.com/scrapy/scrapy
https://github.com/D4Vinci/Scrapling

# get started
.gitignore file with:
.env
__pycache__/
*.pyc
*.pyo
