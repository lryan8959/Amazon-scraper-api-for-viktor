# ⭐ Store URL Feature Added!

## What's New

The API now extracts the **brand store URL** from Amazon product pages.

### New Field: `store_url`

```json
{
  "asin": "B01LXJG04I",
  "brand": "Brand Name",
  "store_url": "https://www.amazon.com/stores/BrandName/page/XXXXX",
  ...
}
```

## How It Works

The scraper extracts the store URL using two methods:

1. **Primary**: From the `#bylineInfo` brand link
   - Most products have this clickable brand name
   - Links directly to the brand's Amazon store page

2. **Fallback**: From "Visit the Store" links
   - Searches for any link containing `/stores/`
   - Common on products with multiple sellers

## Example Usage

### Test with Product B01LXJG04I

```bash
curl -H "X-API-Key: test-key-12345" \
  "http://localhost:8000/v1/product?url=B01LXJG04I"
```

### Expected Response (excerpt)

```json
{
  "status": "ok",
  "asin": "B01LXJG04I",
  "url": "https://www.amazon.com/dp/B01LXJG04I",
  "title": "Product Title",
  "brand": "Brand Name",
  "store_url": "https://www.amazon.com/stores/BrandName/page/12345ABC",
  ...
}
```

## Use Cases

### 1. Brand Analysis
Track all products from a specific brand by visiting their store page.

### 2. Competitive Research
Find similar products from the same brand.

### 3. Brand Discovery
Explore a brand's full product catalog.

### 4. Affiliate Marketing
Link directly to brand stores for better conversions.

### 5. Product Recommendations
Show customers more products from brands they like.

## Technical Details

### Extraction Logic (scraper.py:148-173)

```python
# Store URL
try:
    store_link = await page.query_selector("#bylineInfo")
    if store_link:
        href = await store_link.get_attribute("href")
        if href:
            # Convert relative URL to absolute
            if href.startswith("/"):
                result["store_url"] = f"https://www.amazon.com{href}"
            else:
                result["store_url"] = href

    # Alternative: Look for "Visit the Store" link
    if "store_url" not in result:
        visit_store = await page.query_selector('a[href*="/stores/"]')
        if visit_store:
            href = await visit_store.get_attribute("href")
            if href:
                if href.startswith("/"):
                    result["store_url"] = f"https://www.amazon.com{href}"
                else:
                    result["store_url"] = href
except:
    pass
```

### Field Availability

- ✅ Available for most branded products
- ✅ Works with Amazon's own brands
- ✅ Works with third-party brands
- ⚠️ May be missing for unbranded/generic items
- ⚠️ May be missing for some marketplace sellers

## Updated Files

- ✅ `scraper.py` - Added store URL extraction logic
- ✅ `test_api_demo.py` - Updated demo with store_url field
- ✅ `api/README.md` - Updated documentation
- ✅ `API_SUMMARY.md` - Added store_url to summary
- ✅ `CHANGELOG.md` - Version 1.1.0 changelog
- ✅ `FEATURES.md` - Complete feature list with store_url

## Testing

### Python Test
```python
import requests

response = requests.get(
    "http://localhost:8000/v1/product",
    params={"url": "B01LXJG04I"},
    headers={"X-API-Key": "test-key-12345"}
)

data = response.json()
print(f"Brand: {data.get('brand')}")
print(f"Store: {data.get('store_url')}")
```

### cURL Test
```bash
curl -s -H "X-API-Key: test-key-12345" \
  "http://localhost:8000/v1/product?url=B01LXJG04I" \
  | jq '.store_url'
```

## Version

- **API Version**: 1.1.0
- **Feature Added**: 2026-11-23
- **Status**: ✅ Production Ready

## Deployment

The updated code is ready to deploy:

```bash
# Local Docker
docker-compose down
docker-compose build
docker-compose up -d

# Or rebuild from scratch
docker-compose up -d --build

# Cloud (Railway/Render/Fly.io)
git add .
git commit -m "Add store_url extraction feature"
git push
```

---

**Total Data Fields**: 21+ fields  
**New Field**: `store_url` ⭐  
**Backward Compatible**: Yes (optional field)
