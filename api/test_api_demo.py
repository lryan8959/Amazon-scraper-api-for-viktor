#!/usr/bin/env python3
"""
Demo test showing the API structure and expected data format
This simulates what the API would return for the product B01LXJG04I
"""

import json

# This is the ASIN from the URL: https://www.amazon.com/dp/B01LXJG04I
ASIN = "B01LXJG04I"

# Simulated response showing all the data the API would extract
simulated_response = {
    "status": "ok",
    "asin": ASIN,
    "url": f"https://www.amazon.com/dp/{ASIN}",

    # Basic product information
    "title": "Product Title (would be extracted from #productTitle)",
    "price": "$XX.XX (would be extracted from .a-price .a-offscreen)",

    # Rating and reviews
    "rating": 4.5,  # Extracted from span[data-hook='rating-out-of-text']
    "reviews_count": 12345,  # Extracted from #acrCustomerReviewText

    # Images
    "main_image": "https://m.media-amazon.com/images/I/example-main.jpg",
    "images": [
        "https://m.media-amazon.com/images/I/example-1.jpg",
        "https://m.media-amazon.com/images/I/example-2.jpg",
        "https://m.media-amazon.com/images/I/example-3.jpg",
    ],

    # Brand and seller
    "brand": "Brand Name (from #bylineInfo)",
    "store_url": "https://www.amazon.com/stores/BrandName/page/XXXXX (from #bylineInfo href or Visit Store link)",
    "seller": "Amazon.com or Third-party seller (from #sellerProfileTriggerId)",

    # Availability
    "availability": "In Stock / Currently unavailable (from #availability span)",

    # Features/Bullet points
    "features": [
        "Feature 1 from bullet points",
        "Feature 2 from bullet points",
        "Feature 3 from bullet points",
        "Feature 4 from bullet points",
        "Feature 5 from bullet points",
    ],

    # Product description
    "description": "Full product description text (from #productDescription p)",

    # Product details/specifications
    "product_details": {
        "Product Dimensions": "10 x 8 x 2 inches",
        "Item Weight": "1.2 pounds",
        "ASIN": ASIN,
        "Item model number": "MODEL123",
        "Date First Available": "January 1, 2020",
        "Manufacturer": "Manufacturer Name",
        "Best Sellers Rank": "#123 in Category",
    },

    # Categories/Breadcrumbs
    "categories": [
        "Electronics",
        "Computers & Accessories",
        "Computer Accessories & Peripherals",
    ],

    # Variants (colors, sizes, etc.)
    "variants": {
        "colors": ["Black", "White", "Silver"],
        "sizes": ["Small", "Medium", "Large"],
    },

    # Metadata
    "cached": False,
    "scraped_at": "2026-11-23T22:50:00Z",
}

def test_api_structure():
    """Test that shows the API structure"""
    print("=" * 70)
    print("AMAZON PRODUCT SCRAPER API - TEST DEMO")
    print("=" * 70)
    print()
    print(f"Testing with ASIN: {ASIN}")
    print(f"URL: https://www.amazon.com/dp/{ASIN}")
    print()
    print("-" * 70)
    print("API ENDPOINT: GET /v1/product?url=B01LXJG04I")
    print("HEADERS: X-API-Key: test-key-12345")
    print("-" * 70)
    print()
    print("EXPECTED RESPONSE STRUCTURE:")
    print(json.dumps(simulated_response, indent=2))
    print()
    print("-" * 70)
    print("DATA FIELDS EXTRACTED:")
    print("-" * 70)

    fields = [
        ("Basic Info", ["status", "asin", "url", "title", "price"]),
        ("Ratings", ["rating", "reviews_count"]),
        ("Images", ["main_image", "images"]),
        ("Brand/Seller", ["brand", "store_url", "seller", "availability"]),
        ("Content", ["features", "description"]),
        ("Specifications", ["product_details"]),
        ("Navigation", ["categories"]),
        ("Variants", ["variants"]),
    ]

    for category, field_list in fields:
        print(f"\n✓ {category}:")
        for field in field_list:
            if field in simulated_response:
                value = simulated_response[field]
                if isinstance(value, (list, dict)):
                    count = len(value)
                    print(f"  - {field}: {type(value).__name__} with {count} items")
                else:
                    print(f"  - {field}: {value}")

    print()
    print("=" * 70)
    print("ACTUAL API USAGE (when running):")
    print("=" * 70)
    print()
    print("curl -H 'X-API-Key: test-key-12345' \\")
    print(f"  'http://localhost:8000/v1/product?url={ASIN}'")
    print()
    print("OR")
    print()
    print("curl -X POST http://localhost:8000/v1/product \\")
    print("  -H 'X-API-Key: test-key-12345' \\")
    print("  -H 'Content-Type: application/json' \\")
    print(f"  -d '{{\"url\": \"https://www.amazon.com/dp/{ASIN}\", \"fresh\": false}}'")
    print()
    print("=" * 70)
    print("TO START THE API:")
    print("=" * 70)
    print()
    print("Option 1 - Docker (recommended):")
    print("  docker-compose up -d")
    print()
    print("Option 2 - Python:")
    print("  pip install -r requirements.txt")
    print("  playwright install chromium")
    print("  uvicorn app:app --reload")
    print()
    print("=" * 70)

if __name__ == "__main__":
    test_api_structure()
