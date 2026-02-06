
import requests
import base64
from typing import List, Dict, Optional


class EbayAPI:
    
    # API endpoints
    SANDBOX_AUTH_URL = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
    SANDBOX_API_URL = "https://api.sandbox.ebay.com/buy/browse/v1"
    
    PROD_AUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"
    PROD_API_URL = "https://api.ebay.com/buy/browse/v1"
    
    MARKETPLACES = {
        'SE': 'EBAY_SE',
        'US': 'EBAY_US',
        'UK': 'EBAY_GB',
        'DE': 'EBAY_DE',
    }
    
    def __init__(self, client_id: str, client_secret: str, sandbox: bool = True):
        # get arguments from eBay Developer Portal
        self.client_id = client_id
        self.client_secret = client_secret
        self.sandbox = sandbox
        
        # choose api endpoint url
        if sandbox:
            self.auth_url = self.SANDBOX_AUTH_URL
            self.api_url = self.SANDBOX_API_URL
        else:
            self.auth_url = self.PROD_AUTH_URL
            self.api_url = self.PROD_API_URL
        
        self.access_token = None
    
    def get_access_token(self) -> str:

        # get OAuth access token, valid for 2 hours.        
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded}"
        }
        
        data = {
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope"
        }
        
        try:
            response = requests.post(self.auth_url, headers=headers, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            
            print(f"✅ access token obtained (expires in {token_data['expires_in']}s)")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            print(f"❌ failed to get access token: {e}")
            if hasattr(e.response, 'text'):
                print(f"response: {e.response.text}")
            raise
    
    def search(self, 
               query: str, 
               max_price: Optional[int] = None,
               min_price: Optional[int] = None,
               marketplace: str = 'SE',
               limit: int = 50) -> List[Dict]:
        """        
        Args:
            query: Search keywords (e.g., "arcteryx jacket")
            max_price: Maximum price filter
            min_price: Minimum price filter
            marketplace: Country code (SE, US, UK, DE)
            limit: Number of results to return (max 200)
            
        Returns:
            List of product dictionaries
        """
        # fetch token if we don't have one
        if not self.access_token:
            self.get_access_token()
        
        url = f"{self.api_url}/item_summary/search"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-EBAY-C-MARKETPLACE-ID": self.MARKETPLACES.get(marketplace, 'EBAY_SE')
        }
        
        params = {
            "q": query,
            "limit": min(limit, 200)  # eBay max is 200
        }
        
        # add price filters if specified
        filters = []
        if max_price:
            filters.append(f"price:[..{max_price}]")
        if min_price:
            filters.append(f"price:[{min_price}..]")
        
        if filters:
            # add currency filter
            filters.append("priceCurrency:SEK" if marketplace == 'SE' else "priceCurrency:USD")
            params["filter"] = ",".join(filters)
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_results(data)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ search failed: {e}")
            if hasattr(e.response, 'text'):
                print(f"response: {e.response.text}")
            return []
    
    def _parse_results(self, data: Dict) -> List[Dict]:
        """
        parse API repsone to user friendly information
        
        Args:
            data: Raw API response
            
        Returns:
            List of simplified product dictionaries
        """
        products = []
        
        if 'itemSummaries' not in data:
            print(f"ℹ️ No results found")
            return products
        
        for item in data['itemSummaries']:
            product = {
                'id': item.get('itemId'),
                'title': item.get('title'),
                'price': item.get('price', {}).get('value'),
                'currency': item.get('price', {}).get('currency'),
                'condition': item.get('condition'),
                'url': item.get('itemWebUrl'),
                'image_url': item.get('image', {}).get('imageUrl'),
                'seller': item.get('seller', {}).get('username'),
                'location': item.get('itemLocation', {}).get('city', 'Unknown')
            }
            products.append(product)
        
        # amount of products
        print(f"✅ found {len(products)} products")
        return products