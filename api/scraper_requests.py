"""
Alternative scraper using requests library (faster, sometimes bypasses detection better)
"""
import requests
import re
import random
from typing import Optional
from bs4 import BeautifulSoup

# Rotate between multiple user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
]

# Try multiple Amazon domains (some have weaker bot detection)
AMAZON_DOMAINS = [
    "amazon.com",
    "amazon.co.uk",
    "amazon.de",
    "amazon.ca",
]


def get_headers():
    """Generate realistic browser headers"""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Cache-Control": "max-age=0",
        "TE": "trailers",
    }


def find_asin(text: str) -> Optional[str]:
    """Extract ASIN from URL or plain text"""
    patterns = [
        r'/dp/([A-Z0-9]{10})',
        r'/gp/product/([A-Z0-9]{10})',
        r'asin[=/]([A-Z0-9]{10})',
        r'\b([A-Z0-9]{10})\b'
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            asin = m.group(1).upper()
            if re.match(r'^[A-Z0-9]{10}$', asin):
                return asin
    return None


def scrape_with_requests(asin: str) -> dict:
    """
    Scrape using requests library (no browser, faster, sometimes works better)
    """
    session = requests.Session()

    # Try multiple domains
    for domain in AMAZON_DOMAINS:
        url = f"https://www.{domain}/dp/{asin}"

        try:
            print(f"[{asin}] Trying {domain} with requests...")

            response = session.get(
                url,
                headers=get_headers(),
                timeout=15,
                allow_redirects=True
            )

            print(f"[{asin}] Status code: {response.status_code}")

            if response.status_code != 200:
                continue

            html = response.text

            # Check for blocking
            if "captcha" in html.lower() or "robot" in html.lower():
                print(f"[{asin}] ⚠️  Bot detection on {domain}")
                continue

            # Parse with BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Check if product page loaded
            title_elem = soup.select_one("#productTitle")
            if not title_elem:
                print(f"[{asin}] ✗ No product title on {domain}")
                continue

            print(f"[{asin}] ✓ Success on {domain}!")

            # Extract data
            result = {
                "status": "ok",
                "asin": asin,
                "url": url,
                "domain": domain,
            }

            # Title
            if title_elem:
                result["title"] = title_elem.get_text(strip=True)

            # Price
            price_elem = soup.select_one(".a-price .a-offscreen")
            if price_elem:
                result["price"] = price_elem.get_text(strip=True)

            # Rating
            rating_elem = soup.select_one("span[data-hook='rating-out-of-text']")
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                match = re.search(r'([\d.]+)', rating_text)
                if match:
                    result["rating"] = float(match.group(1))

            # Reviews count
            reviews_elem = soup.select_one("#acrCustomerReviewText")
            if reviews_elem:
                reviews_text = reviews_elem.get_text(strip=True)
                match = re.search(r'([\d,]+)', reviews_text)
                if match:
                    result["reviews_count"] = int(match.group(1).replace(',', ''))

            # Main image
            img_elem = soup.select_one("#landingImage, #imgBlkFront")
            if img_elem:
                result["main_image"] = img_elem.get('src')

            # Images
            images = []
            img_thumbnails = soup.select(".imageThumbnail img")
            for thumb in img_thumbnails[:10]:
                src = thumb.get('src')
                if src:
                    # Convert thumbnail to full size
                    full_src = re.sub(r'\._[^.]+_\.', '.', src)
                    images.append(full_src)
            if images:
                result["images"] = images

            # Brand
            brand_elem = soup.select_one("#bylineInfo")
            if brand_elem:
                brand_text = brand_elem.get_text(strip=True)
                result["brand"] = brand_text.replace("Visit the ", "").replace(" Store", "").replace("Brand: ", "")

            # Store URL
            store_link = soup.select_one("#bylineInfo")
            if store_link and store_link.get('href'):
                href = store_link.get('href')
                if href.startswith("/"):
                    result["store_url"] = f"https://www.{domain}{href}"
                else:
                    result["store_url"] = href

            # Availability
            avail_elem = soup.select_one("#availability span")
            if avail_elem:
                result["availability"] = avail_elem.get_text(strip=True)

            # Features
            features = []
            feature_elems = soup.select("#feature-bullets li:not(.aok-hidden) span.a-list-item")
            for feat in feature_elems[:10]:
                text = feat.get_text(strip=True)
                if text and len(text) > 5:
                    features.append(text)
            if features:
                result["features"] = features

            # Description
            desc_elem = soup.select_one("#productDescription p")
            if desc_elem:
                result["description"] = desc_elem.get_text(strip=True)

            # Categories
            categories = []
            cat_elems = soup.select("#wayfinding-breadcrumbs_feature_div ul li a")
            for cat in cat_elems:
                cat_text = cat.get_text(strip=True)
                if cat_text:
                    categories.append(cat_text)
            if categories:
                result["categories"] = categories

            return result

        except Exception as e:
            print(f"[{asin}] Error on {domain}: {e}")
            continue

    # All domains failed
    return {
        "status": "error",
        "message": "Failed to scrape from all domains. Amazon may be blocking requests.",
        "asin": asin
    }
