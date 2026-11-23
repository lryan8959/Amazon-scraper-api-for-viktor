# 🚀 Amazon Scraper API - Quick Guide for AI Agents

## ✅ Your Live API

**API URL:** `https://amazon-scraper-api-for-viktor-production.up.railway.app`  
**API Key:** `715bbbcda6fae35385f88bc58001c535`  
**Documentation:** https://amazon-scraper-api-for-viktor-production.up.railway.app/docs

---

## 📋 Quick Start

### 1️⃣ Get Single Product (Simple)

**Endpoint:** `GET /v1/product?url={ASIN}`

**Example:**
```bash
curl -H "X-API-Key: 715bbbcda6fae35385f88bc58001c535" \
  "https://amazon-scraper-api-for-viktor-production.up.railway.app/v1/product?url=B01LXJG04I"
```

**Response (21+ fields):**
```json
{
  "status": "ok",
  "asin": "B01LXJG04I",
  "url": "https://www.amazon.com/dp/B01LXJG04I",
  "title": "Product Title",
  "price": "$39.99",
  "rating": 4.7,
  "reviews_count": 12345,
  "main_image": "https://m.media-amazon.com/images/...",
  "images": ["url1", "url2", "url3"],
  "brand": "Brand Name",
  "store_url": "https://www.amazon.com/stores/...",
  "seller": "Amazon.com",
  "availability": "In Stock",
  "features": ["Feature 1", "Feature 2"],
  "description": "Product description...",
  "product_details": {
    "Product Dimensions": "...",
    "Item Weight": "...",
    "ASIN": "B01LXJG04I"
  },
  "categories": ["Electronics", "..."],
  "variants": {
    "colors": ["Black", "White"],
    "sizes": ["Small", "Medium"]
  },
  "cached": false
}
```

---

## 🤖 For AI Agents - Code Examples

### Python Example

```python
import requests
import json

# Configuration
API_URL = "https://amazon-scraper-api-for-viktor-production.up.railway.app"
API_KEY = "715bbbcda6fae35385f88bc58001c535"

def scrape_amazon_product(asin_or_url):
    """
    Scrape Amazon product data by ASIN or URL
    
    Args:
        asin_or_url: Amazon ASIN (e.g., "B01LXJG04I") or full URL
        
    Returns:
        dict: Product data with 21+ fields
    """
    headers = {"X-API-Key": API_KEY}
    params = {"url": asin_or_url}
    
    response = requests.get(
        f"{API_URL}/v1/product",
        headers=headers,
        params=params,
        timeout=120  # Can take 10-15 seconds for first scrape
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Example usage
if __name__ == "__main__":
    # Test with ASIN
    product = scrape_amazon_product("B01LXJG04I")
    
    print(f"Title: {product['title']}")
    print(f"Price: {product['price']}")
    print(f"Rating: {product['rating']}")
    print(f"Brand: {product['brand']}")
    print(f"Store: {product.get('store_url')}")
    print(f"\nFull data:")
    print(json.dumps(product, indent=2))
```

### JavaScript/Node.js Example

```javascript
const API_URL = "https://amazon-scraper-api-for-viktor-production.up.railway.app";
const API_KEY = "715bbbcda6fae35385f88bc58001c535";

async function scrapeAmazonProduct(asinOrUrl) {
    const response = await fetch(
        `${API_URL}/v1/product?url=${encodeURIComponent(asinOrUrl)}`,
        {
            headers: {
                "X-API-Key": API_KEY
            }
        }
    );
    
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${await response.text()}`);
    }
    
    return await response.json();
}

// Example usage
scrapeAmazonProduct("B01LXJG04I")
    .then(product => {
        console.log("Title:", product.title);
        console.log("Price:", product.price);
        console.log("Rating:", product.rating);
        console.log("Brand:", product.brand);
        console.log("Store URL:", product.store_url);
        console.log("\nFull data:", JSON.stringify(product, null, 2));
    })
    .catch(error => console.error("Error:", error));
```

### cURL Example

```bash
# Basic request
curl -H "X-API-Key: 715bbbcda6fae35385f88bc58001c535" \
  "https://amazon-scraper-api-for-viktor-production.up.railway.app/v1/product?url=B01LXJG04I"

# With full URL
curl -H "X-API-Key: 715bbbcda6fae35385f88bc58001c535" \
  "https://amazon-scraper-api-for-viktor-production.up.railway.app/v1/product?url=https://www.amazon.com/dp/B01LXJG04I"

# Force fresh scrape (bypass cache)
curl -H "X-API-Key: 715bbbcda6fae35385f88bc58001c535" \
  "https://amazon-scraper-api-for-viktor-production.up.railway.app/v1/product?url=B01LXJG04I&fresh=true"
```

---

## 🔄 Batch Processing (Multiple Products)

### Create a Batch Job

**Endpoint:** `POST /v1/jobs`

**Python Example:**
```python
def scrape_multiple_products(asins):
    """Scrape multiple products in a batch job"""
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "urls": asins,  # List of ASINs
        "fresh": False
    }
    
    # Create job
    response = requests.post(
        f"{API_URL}/v1/jobs",
        headers=headers,
        json=data
    )
    
    job = response.json()
    job_id = job["job_id"]
    print(f"Job created: {job_id}")
    
    # Poll for completion
    import time
    while True:
        status_response = requests.get(
            f"{API_URL}/v1/jobs/{job_id}",
            headers=headers
        )
        
        status = status_response.json()
        
        if status["status"] == "done":
            print(f"Complete! {status['successful']}/{status['total']} succeeded")
            return status["products"]
        
        print(f"Progress: {len(status['products'])}/{status['total']}")
        time.sleep(10)

# Example usage
products = scrape_multiple_products([
    "B01LXJG04I",
    "B08N5WRWNW",
    "B07B3NJDNB"
])

for product in products:
    if product.get("status") == "ok":
        print(f"{product['asin']}: {product['title']} - {product['price']}")
```

---

## 📊 All Available Data Fields

Your API extracts **21+ fields** from each product:

### Basic Info
- `status` - "ok" or "not_found"
- `asin` - Amazon Standard Identification Number
- `url` - Full product URL
- `title` - Product title
- `price` - Current price with currency

### Ratings & Reviews
- `rating` - Star rating (1-5)
- `reviews_count` - Total number of reviews

### Media
- `main_image` - Main product image URL (high-res)
- `images` - Array of all product images

### Brand & Seller ⭐
- `brand` - Product brand name
- **`store_url`** - Brand store page URL (NEW!)
- `seller` - Seller name
- `availability` - Stock status

### Content
- `features` - Array of bullet points
- `description` - Full product description

### Specifications
- `product_details` - Object with technical specs:
  - Product Dimensions
  - Item Weight
  - Model Number
  - Date First Available
  - Manufacturer
  - Best Sellers Rank
  - And more...

### Navigation
- `categories` - Array of category breadcrumbs

### Variants
- `variants` - Object with:
  - `colors` - Available colors
  - `sizes` - Available sizes
  - Other variant types

### Metadata
- `cached` - Whether result was from cache (true/false)

---

## ⚡ Performance Tips

### 1. Caching
- First request: 10-15 seconds (scraping Amazon)
- Cached requests: < 100ms
- Cache TTL: 1 hour (default)

### 2. Bypass Cache
Add `?fresh=true` to force fresh scrape:
```bash
curl -H "X-API-Key: YOUR_KEY" \
  "https://your-api.up.railway.app/v1/product?url=B01LXJG04I&fresh=true"
```

### 3. Rate Limiting
- Built-in delays: 3-6 seconds between batch requests
- Use batch jobs (`/v1/jobs`) for multiple products
- Max 5 products per batch (configurable)

---

## 🔐 Authentication

Always include your API key in the header:

```
X-API-Key: 715bbbcda6fae35385f88bc58001c535
```

**Keep your API key secure!** Don't commit it to public repositories.

---

## 🛠️ Error Handling

### Common Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Product data returned |
| 401 | Unauthorized | Check API key |
| 404 | Not Found | Product doesn't exist on Amazon |
| 502 | Scrape Failed | Amazon blocked or product unavailable |
| 504 | Timeout | Request took too long, retry |

### Example Error Handling (Python)

```python
def safe_scrape(asin):
    try:
        product = scrape_amazon_product(asin)
        
        if product.get("status") == "ok":
            return product
        elif product.get("status") == "not_found":
            print(f"Product {asin} not found on Amazon")
            return None
            
    except requests.exceptions.Timeout:
        print(f"Timeout scraping {asin}, retry in a moment")
        return None
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Invalid API key!")
        elif e.response.status_code == 502:
            print(f"Failed to scrape {asin}, Amazon may have blocked")
        return None
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

---

## 🎯 For AI Agents - Integration Guide

### OpenAI Function Calling

```python
{
    "name": "scrape_amazon_product",
    "description": "Scrape product data from Amazon by ASIN or URL. Returns title, price, rating, reviews, images, brand, store URL, features, description, specifications, and more.",
    "parameters": {
        "type": "object",
        "properties": {
            "asin_or_url": {
                "type": "string",
                "description": "Amazon ASIN (e.g., B01LXJG04I) or full product URL"
            },
            "fresh": {
                "type": "boolean",
                "description": "Bypass cache and get fresh data",
                "default": False
            }
        },
        "required": ["asin_or_url"]
    }
}
```

### LangChain Tool

```python
from langchain.tools import Tool

amazon_scraper = Tool(
    name="AmazonProductScraper",
    description="Scrapes Amazon product data including title, price, rating, reviews, images, brand, store URL, features, and specifications. Input should be an ASIN or Amazon product URL.",
    func=scrape_amazon_product
)
```

---

## 📚 Additional Resources

- **Interactive Docs:** https://amazon-scraper-api-for-viktor-production.up.railway.app/docs
- **Health Check:** https://amazon-scraper-api-for-viktor-production.up.railway.app/health
- **Test Page:** Use the test-api.html file for browser-based testing

---

## ✅ Quick Test

Test your setup:

```bash
# Health check (no API key needed)
curl https://amazon-scraper-api-for-viktor-production.up.railway.app/health

# Scrape a product
curl -H "X-API-Key: 715bbbcda6fae35385f88bc58001c535" \
  "https://amazon-scraper-api-for-viktor-production.up.railway.app/v1/product?url=B01LXJG04I"
```

---

**Your API is now live and ready to use!** 🎉

**Version:** 1.1.0  
**Features:** 21+ data fields including store URL extraction  
**Status:** ✅ Production Ready
