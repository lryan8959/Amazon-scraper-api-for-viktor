#!/usr/bin/env python3
"""
Test script for deployed Amazon Scraper API
"""

import requests
import json
import sys

# Your deployed API
API_URL = "https://amazon-scraper-api-for-viktor-production.up.railway.app"
API_KEY = "715bbbcda6fae35385f88bc58001c535"

def test_health():
    """Test the health endpoint"""
    print("━" * 70)
    print("1️⃣  Testing Health Endpoint")
    print("━" * 70)
    print()

    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        print(f"Status Code: {response.status_code}")
        print()
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_product_scraping():
    """Test product scraping with ASIN B01LXJG04I"""
    print("━" * 70)
    print("2️⃣  Testing Product Scraping (ASIN: B01LXJG04I)")
    print("━" * 70)
    print()
    print("⏳ This may take 10-15 seconds for first request...")
    print()

    try:
        response = requests.get(
            f"{API_URL}/v1/product",
            params={"url": "B01LXJG04I"},
            headers={"X-API-Key": API_KEY},
            timeout=120
        )

        print(f"Status Code: {response.status_code}")
        print()

        if response.status_code == 200:
            data = response.json()

            print("━" * 70)
            print("📊 Key Fields Extracted:")
            print("━" * 70)
            print(f"Status:       {data.get('status')}")
            print(f"ASIN:         {data.get('asin')}")
            print(f"Title:        {data.get('title', 'N/A')[:60]}...")
            print(f"Price:        {data.get('price', 'N/A')}")
            print(f"Rating:       {data.get('rating', 'N/A')}")
            print(f"Reviews:      {data.get('reviews_count', 'N/A')}")
            print(f"Brand:        {data.get('brand', 'N/A')}")
            print(f"Store URL:    {data.get('store_url', 'N/A')}")
            print(f"Images:       {len(data.get('images', []))} found")
            print(f"Features:     {len(data.get('features', []))} found")
            print(f"Cached:       {data.get('cached', False)}")
            print()

            # Verify new features
            print("━" * 70)
            print("3️⃣  Verifying New Features")
            print("━" * 70)
            print()

            # Check store URL
            if data.get('store_url'):
                print(f"✅ Store URL extraction: WORKING")
                print(f"   {data['store_url']}")
            else:
                print("❌ Store URL extraction: NOT FOUND")
            print()

            # Check images
            if data.get('images'):
                print(f"✅ Images extraction: WORKING ({len(data['images'])} images)")
            else:
                print("❌ Images extraction: NOT FOUND")
            print()

            # Check features
            if data.get('features'):
                print(f"✅ Features extraction: WORKING ({len(data['features'])} features)")
            else:
                print("❌ Features extraction: NOT FOUND")
            print()

            # Show full response (optional)
            show_full = input("Show full JSON response? (y/n): ").lower().strip() == 'y'
            if show_full:
                print()
                print("━" * 70)
                print("Full Response:")
                print("━" * 70)
                print(json.dumps(data, indent=2))
                print()

            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print()
    print("🧪 Testing Your Deployed Amazon Scraper API")
    print("=" * 70)
    print()
    print(f"API URL: {API_URL}")
    print(f"API Key: {API_KEY}")
    print()

    # Test health
    health_ok = test_health()

    if not health_ok:
        print("⚠️  Health check failed. API might not be ready yet.")
        print("   Wait a minute and try again.")
        sys.exit(1)

    # Test product scraping
    scraping_ok = test_product_scraping()

    # Summary
    print()
    print("━" * 70)
    if health_ok and scraping_ok:
        print("✅ All Tests Passed!")
    else:
        print("⚠️  Some Tests Failed")
    print("━" * 70)
    print()
    print("📖 API Documentation:")
    print(f"   {API_URL}/docs")
    print()
    print("🔍 View Railway Logs:")
    print("   railway logs -f")
    print()

if __name__ == "__main__":
    main()
