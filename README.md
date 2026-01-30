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
- [x] fetch fb marketplace
- [x] setup supabase and save products in cloud database
    - [ ] currenly only working with static information, connect with product fetch script
- [ ] ai to analyze products?
- [ ] input product info in telegram chat -> publish product on platforms?
    - [ ] ebay API, do the rest semi automatic?

# ideas
https://github.com/kyleronayne/marketplace-api
https://github.com/scrapy/scrapy
https://github.com/D4Vinci/Scrapling
https://console.apify.com/

# problems
- apify maximized plan? not free? 5 euro?

# get started
### .gitignore
```txt
    .env
    __pycache__/
    *.pyc
    *.pyo
```
