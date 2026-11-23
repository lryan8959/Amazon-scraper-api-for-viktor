# Amazon Product Scraper API

A FastAPI-based service that scrapes Amazon product data by ASIN or product URL.

## Features

- ✅ Single product scraping via GET or POST
- ✅ Batch processing with job queue
- ✅ Built-in caching (1-hour default TTL)
- ✅ API key authentication
- ✅ Automatic retry on failures
- ✅ US delivery location configuration
- ✅ Comprehensive product data extraction

## Extracted Data

The API extracts the following product information:

- **Basic Info**: ASIN, title, URL
- **Pricing**: Current price
- **Ratings**: Star rating and review count
- **Images**: Main image and all product images
- **Brand**: Product brand/manufacturer and store URL
- **Availability**: Stock status
- **Features**: Bullet points
- **Description**: Product description
- **Details**: Dimensions, weight, ASIN, date first available, etc.
- **Categories**: Product categories and breadcrumbs
- **Variants**: Available colors, sizes, styles
- **Seller**: Seller information

## Quick Start

### Local Development

1. **Install dependencies:**
```bash
cd api
pip install -r requirements.txt
playwright install chromium
```

2. **Set environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Run the server:**
```bash
uvicorn app:app --reload --port 8000
```

4. **Test the API:**
```bash
curl -H "X-API-Key: demo-key-12345" \
  "http://localhost:8000/v1/product?url=B07B3NJDNB"
```

### Docker Deployment

1. **Build and run with Docker Compose:**
```bash
cd api
docker-compose up -d
```

2. **Check health:**
```bash
curl http://localhost:8000/health
```

## API Endpoints

### Health Check
```bash
GET /health
```

Returns API status, browser status, and cache info.

### Single Product (GET)
```bash
GET /v1/product?url=B07B3NJDNB&fresh=false
Headers:
  X-API-Key: your-api-key
```

### Single Product (POST)
```bash
POST /v1/product
Headers:
  X-API-Key: your-api-key
Body:
{
  "url": "https://www.amazon.com/dp/B07B3NJDNB",
  "fresh": false
}
```

### Batch Processing (Jobs)
```bash
POST /v1/jobs
Headers:
  X-API-Key: your-api-key
Body:
{
  "urls": ["B07B3NJDNB", "B08N5WRWNW"],
  "fresh": false
}

Response:
{
  "job_id": "abc123def456",
  "status": "queued",
  "poll": "/v1/jobs/abc123def456"
}
```

### Check Job Status
```bash
GET /v1/jobs/{job_id}
Headers:
  X-API-Key: your-api-key
```

## Example Response

```json
{
  "status": "ok",
  "asin": "B07B3NJDNB",
  "url": "https://www.amazon.com/dp/B07B3NJDNB",
  "title": "Echo Dot (3rd Gen) - Smart speaker with Alexa - Charcoal",
  "price": "$39.99",
  "rating": 4.7,
  "reviews_count": 456789,
  "main_image": "https://m.media-amazon.com/images/I/...",
  "images": [
    "https://m.media-amazon.com/images/I/...",
    "https://m.media-amazon.com/images/I/..."
  ],
  "brand": "Amazon",
  "store_url": "https://www.amazon.com/stores/Amazon/page/...",
  "availability": "In Stock",
  "features": [
    "Improved speaker quality - Better speaker quality than Echo Dot Gen 2",
    "Voice control your music - Stream songs from Amazon Music, Apple Music, Spotify, and more",
    "Ready to help - Ask Alexa to play music, answer questions, make calls, and more"
  ],
  "description": "Meet Echo Dot - Our most popular smart speaker...",
  "product_details": {
    "Product Dimensions": "3.9 x 3.9 x 1.7 inches",
    "Item Weight": "10.6 ounces",
    "ASIN": "B07B3NJDNB",
    "Date First Available": "September 27, 2018"
  },
  "categories": [
    "Electronics",
    "Home Audio",
    "Speakers",
    "Smart Speakers"
  ],
  "variants": {
    "colors": ["Charcoal", "Heather Gray", "Sandstone"]
  },
  "seller": "Amazon.com",
  "cached": false
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_KEYS` | `demo-key-12345` | Comma-separated API keys |
| `CACHE_TTL` | `3600` | Cache TTL in seconds |
| `MAX_BATCH` | `5` | Max products per batch job |
| `REQUEST_TIMEOUT` | `85` | Request timeout in seconds |
| `US_ZIP` | `10001` | US ZIP code for delivery location |
| `REQUIRE_US_ZIP` | `0` | Require US location (1=yes, 0=no) |
| `MAX_RETRIES` | `2` | Max retries on failure |
| `PROXY_URL` | - | Optional proxy URL |

## Deployment Options

### Railway
1. Fork this repo
2. Connect to Railway
3. Set environment variables
4. Deploy

### Render
1. Create new Web Service
2. Connect repository
3. Build: `cd api && pip install -r requirements.txt && playwright install chromium`
4. Start: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### Fly.io
```bash
cd api
fly launch
fly deploy
```

### DigitalOcean App Platform
1. Create new app
2. Select repository
3. Set build command: `cd api && pip install -r requirements.txt && playwright install chromium`
4. Set run command: `uvicorn app:app --host 0.0.0.0 --port 8080`

## Rate Limiting

Amazon may block excessive requests. Best practices:

- Use caching (enabled by default)
- Add delays between requests (3-6 seconds for batch jobs)
- Use residential proxies for high-volume scraping
- Rotate user agents (currently set to Chrome)

## Legal Notice

This tool is for educational purposes. Always comply with Amazon's Terms of Service and robots.txt. Use responsibly and at your own risk.

## Support

For issues or questions, please open a GitHub issue.
