# Changelog

All notable changes to the Amazon Product Scraper API.

## [1.1.0] - 2026-11-23

### Added
- ⭐ **Store URL extraction** - Now extracts the brand store URL from Amazon product pages
  - Extracted from `#bylineInfo` link (brand link)
  - Falls back to "Visit the Store" links
  - Returns full Amazon store URL: `https://www.amazon.com/stores/...`
  - New field: `store_url` in API response

### Features
- Extract 21+ data fields from Amazon products
- Comprehensive product information including:
  - Basic info (ASIN, title, price, URL)
  - Ratings and reviews
  - All product images (high-resolution)
  - Brand name and **brand store URL**
  - Seller information
  - Availability status
  - Product features (bullet points)
  - Full product description
  - Product specifications
  - Categories and breadcrumbs
  - Variants (colors, sizes, styles)
- Built-in caching (1-hour TTL)
- API key authentication
- Automatic retry on failures
- Batch processing with job queue
- US delivery location configuration

### Technical
- FastAPI framework
- Playwright for browser automation
- Async/await architecture
- Docker containerization
- Multiple cloud deployment options

## [1.0.0] - 2026-11-23

### Initial Release
- Core scraping functionality
- RESTful API endpoints
- Docker deployment support
- Comprehensive documentation
