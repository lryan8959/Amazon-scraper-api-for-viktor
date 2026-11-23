# Cravealicious Site + Amazon Product Scraper API

This repository contains:
1. **Cravealicious Website** - Static HTML site in the root directory
2. **Amazon Product Scraper API** - FastAPI service in the `/api` directory

## Amazon Product Scraper API

A powerful API for scraping Amazon product data by ASIN or product URL.

### Quick Start

```bash
cd api
./deploy.sh
```

This will start the API on `http://localhost:8000`

### Features

✅ Scrape any Amazon product by ASIN or URL  
✅ Extract: title, price, rating, reviews, images, brand, features, description, variants, and more  
✅ Built-in caching (1-hour TTL)  
✅ Batch processing with job queue  
✅ API key authentication  
✅ Automatic retries on failures  
✅ Docker ready  
✅ Deploy to Railway, Render, Fly.io, etc.

### API Documentation

Once running, visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Example Usage

```bash
# Get product data
curl -H "X-API-Key: demo-key-12345" \
  "http://localhost:8000/v1/product?url=B07B3NJDNB"

# Response includes:
{
  "status": "ok",
  "asin": "B07B3NJDNB",
  "title": "Echo Dot (3rd Gen)...",
  "price": "$39.99",
  "rating": 4.7,
  "reviews_count": 456789,
  "images": [...],
  "features": [...],
  "product_details": {...},
  ...
}
```

### Full Documentation

See [api/README.md](api/README.md) for complete API documentation.

See [api/DEPLOYMENT.md](api/DEPLOYMENT.md) for deployment guides.

## Repository Structure

```
cravealicious-site/
├── index.html              # Main website
├── assets/                 # Website assets
└── api/                    # Amazon Scraper API
    ├── app.py             # FastAPI application
    ├── scraper.py         # Scraping logic
    ├── requirements.txt   # Python dependencies
    ├── Dockerfile         # Docker configuration
    ├── docker-compose.yml # Docker Compose setup
    ├── deploy.sh          # Quick deployment script
    ├── test_client.py     # Test client
    ├── README.md          # API documentation
    └── DEPLOYMENT.md      # Deployment guides
```

## License

MIT License - See LICENSE file for details
# Amazon-scraper-api-for-viktor
