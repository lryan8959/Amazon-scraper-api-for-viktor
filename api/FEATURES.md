# Amazon Product Scraper API - Complete Feature List

## 📊 Extracted Data Fields (21+ fields)

### 1️⃣ Basic Product Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `status` | string | Scraping status | `"ok"` or `"not_found"` |
| `asin` | string | Amazon Standard Identification Number | `"B01LXJG04I"` |
| `url` | string | Full product URL | `"https://www.amazon.com/dp/B01LXJG04I"` |
| `title` | string | Product title | `"Echo Dot (3rd Gen)..."` |
| `price` | string | Current price with currency | `"$39.99"` |

### 2️⃣ Ratings & Reviews
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `rating` | float | Star rating (1-5) | `4.7` |
| `reviews_count` | integer | Total number of reviews | `456789` |

### 3️⃣ Media & Images
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `main_image` | string | Main product image URL (high-res) | `"https://m.media-amazon.com/..."` |
| `images` | array | All product images (up to 10) | `["url1", "url2", ...]` |

### 4️⃣ Brand & Seller Information ⭐
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `brand` | string | Product brand/manufacturer | `"Amazon"` |
| `store_url` | string | **Brand store page URL** ⭐ NEW | `"https://www.amazon.com/stores/Amazon/page/..."` |
| `seller` | string | Seller name | `"Amazon.com"` or `"Third Party Seller"` |
| `availability` | string | Stock status | `"In Stock"` or `"Currently unavailable"` |

### 5️⃣ Product Content
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `features` | array | Product features/bullet points | `["Feature 1", "Feature 2", ...]` |
| `description` | string | Full product description | `"Meet Echo Dot..."` |

### 6️⃣ Product Specifications
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `product_details` | object | Technical specifications | See below |

#### Product Details Object:
- Product Dimensions
- Item Weight
- ASIN
- Item model number
- Date First Available
- Manufacturer
- Best Sellers Rank
- And more...

### 7️⃣ Navigation & Categorization
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `categories` | array | Category breadcrumbs | `["Electronics", "Smart Home", ...]` |

### 8️⃣ Product Variants
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `variants` | object | Available product variations | See below |

#### Variants Object:
- `colors`: Array of available colors
- `sizes`: Array of available sizes
- Other variant types (styles, models, etc.)

### 9️⃣ Metadata
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `cached` | boolean | Whether result was from cache | `true` or `false` |

---

## 🎯 API Capabilities

### Core Features
- ✅ **Single Product Scraping** - GET/POST endpoints
- ✅ **Batch Processing** - Process multiple products via job queue
- ✅ **Built-in Caching** - 1-hour TTL (configurable)
- ✅ **API Key Authentication** - Secure access control
- ✅ **Automatic Retries** - Handles temporary failures
- ✅ **US Location Support** - Set delivery ZIP code

### Performance Features
- ✅ **Async/Await** - Non-blocking I/O
- ✅ **Job Queue** - Background processing for batches
- ✅ **Smart Delays** - 3-6 second delays between requests
- ✅ **Request Timeout** - 85-second default timeout
- ✅ **Cache Management** - Automatic cache cleanup (max 500 items)

### Deployment Features
- ✅ **Docker Support** - Containerized deployment
- ✅ **Docker Compose** - One-command setup
- ✅ **Cloud Ready** - Railway, Render, Fly.io, etc.
- ✅ **Environment Config** - Flexible configuration via .env
- ✅ **Health Checks** - `/health` endpoint for monitoring

### Developer Experience
- ✅ **Interactive API Docs** - Swagger UI at `/docs`
- ✅ **CORS Enabled** - Works with frontend apps
- ✅ **Error Handling** - Clear error messages
- ✅ **Job Status Tracking** - Poll job progress
- ✅ **Fresh Data Option** - Bypass cache when needed

---

## 🔄 API Endpoints

### Health & Status
- `GET /` - API information
- `GET /health` - Health check with system status

### Product Endpoints
- `GET /v1/product?url={ASIN}` - Get single product (query param)
- `POST /v1/product` - Get single product (request body)

### Batch Processing
- `POST /v1/jobs` - Create batch job
- `GET /v1/jobs/{job_id}` - Check job status
- `POST /v1/products` - Batch scrape (alias for jobs)

---

## 🎨 Use Cases

### E-commerce Applications
- Price tracking and monitoring
- Product catalog enrichment
- Competitor analysis
- Inventory management

### Data Analysis
- Market research
- Price trend analysis
- Review sentiment analysis
- Product comparison tools

### Automation
- Automated price alerts
- Stock monitoring
- Product data synchronization
- Affiliate program integration

---

## 📈 Scalability

### Current Limits (Configurable)
- Max products per batch: 5 (default)
- Cache size: 500 products
- Max jobs in queue: 200
- Request timeout: 85 seconds
- Max retries: 2 attempts

### Scaling Options
- Horizontal scaling with multiple instances
- Redis for distributed caching
- Load balancing support
- Proxy rotation for high volume

---

## 🔐 Security Features

- API key authentication (required)
- HTTPS support (via deployment platforms)
- Environment-based configuration
- No sensitive data logging
- Sandboxed browser execution

---

## ⚡ Performance

### Response Times
- Cached products: < 100ms
- Fresh scrape: 5-15 seconds (depending on page load)
- Batch jobs: 3-6 seconds per product

### Resource Usage
- Memory: ~500MB-1GB (Playwright + Chromium)
- CPU: Moderate (browser rendering)
- Network: Varies by page size

---

## 📝 Example Response

```json
{
  "status": "ok",
  "asin": "B01LXJG04I",
  "url": "https://www.amazon.com/dp/B01LXJG04I",
  "title": "Product Name",
  "price": "$39.99",
  "rating": 4.7,
  "reviews_count": 12345,
  "main_image": "https://m.media-amazon.com/images/I/...",
  "images": ["url1", "url2", "url3"],
  "brand": "Brand Name",
  "store_url": "https://www.amazon.com/stores/BrandName/page/...",
  "seller": "Amazon.com",
  "availability": "In Stock",
  "features": ["Feature 1", "Feature 2", "Feature 3"],
  "description": "Full product description...",
  "product_details": {
    "Product Dimensions": "10 x 8 x 2 inches",
    "Item Weight": "1.2 pounds",
    "ASIN": "B01LXJG04I"
  },
  "categories": ["Electronics", "Computers & Accessories"],
  "variants": {
    "colors": ["Black", "White", "Silver"],
    "sizes": ["Small", "Medium", "Large"]
  },
  "cached": false
}
```

---

**Version**: 1.1.0  
**Last Updated**: 2026-11-23  
**Status**: Production Ready ✅
