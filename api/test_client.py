#!/usr/bin/env python3
"""
Test client for the Amazon Product Scraper API
"""

import requests
import time
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "demo-key-12345"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}


def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))


def test_single_product():
    """Test single product scraping"""
    print("\n=== Testing Single Product ===")
    asin = "B07B3NJDNB"  # Echo Dot example

    response = requests.get(
        f"{BASE_URL}/v1/product",
        params={"url": asin},
        headers=headers,
        timeout=120
    )

    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Title: {data.get('title')}")
        print(f"Price: {data.get('price')}")
        print(f"Rating: {data.get('rating')}")
        print(f"Reviews: {data.get('reviews_count')}")
        print(f"Cached: {data.get('cached')}")
        print(f"\nFull response:")
        print(json.dumps(data, indent=2))
    else:
        print(response.text)


def test_batch_job():
    """Test batch job processing"""
    print("\n=== Testing Batch Job ===")

    # Create job
    job_data = {
        "urls": ["B07B3NJDNB", "B08N5WRWNW"],
        "fresh": False
    }

    response = requests.post(
        f"{BASE_URL}/v1/jobs",
        json=job_data,
        headers=headers
    )

    print(f"Job created - Status: {response.status_code}")
    job_info = response.json()
    job_id = job_info.get("job_id")
    print(f"Job ID: {job_id}")

    # Poll for completion
    max_wait = 300  # 5 minutes
    start_time = time.time()

    while time.time() - start_time < max_wait:
        response = requests.get(
            f"{BASE_URL}/v1/jobs/{job_id}",
            headers=headers
        )

        job_status = response.json()
        status = job_status.get("status")
        total = job_status.get("total")
        completed = len(job_status.get("products", []))

        print(f"Status: {status} - Completed: {completed}/{total}")

        if status == "done":
            print(f"\nSuccessful: {job_status.get('successful')}")
            print(f"Failed: {job_status.get('failed')}")
            print(f"\nProducts:")
            for product in job_status.get("products", []):
                if product.get("status") == "ok":
                    print(f"  - {product.get('asin')}: {product.get('title')}")
                else:
                    print(f"  - {product.get('input')}: ERROR - {product.get('error')}")
            break

        time.sleep(10)


def test_post_product():
    """Test POST endpoint for single product"""
    print("\n=== Testing POST Product ===")

    response = requests.post(
        f"{BASE_URL}/v1/product",
        json={"url": "https://www.amazon.com/dp/B07B3NJDNB", "fresh": False},
        headers=headers,
        timeout=120
    )

    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Title: {data.get('title')}")
        print(f"Price: {data.get('price')}")
    else:
        print(response.text)


def main():
    print("Amazon Product Scraper API - Test Client")
    print("=" * 50)

    try:
        test_health()
        test_single_product()
        # test_post_product()
        # test_batch_job()

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("Make sure the API is running on", BASE_URL)
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
