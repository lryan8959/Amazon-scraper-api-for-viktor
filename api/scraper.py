import os
import re
import asyncio
from typing import Optional

# Configuration
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
PROXY = os.getenv("PROXY_URL")  # Format: {"server": "http://proxy:port", "username": "user", "password": "pass"}
US_ZIP = os.getenv("US_ZIP", "10001")
REQUIRE_US_ZIP = os.getenv("REQUIRE_US_ZIP", "0") == "1"
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))


def find_asin(text: str) -> Optional[str]:
    """Extract ASIN from URL or plain text."""
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


async def ensure_us_location(page, zipcode: str) -> bool:
    """Set delivery location to US ZIP code."""
    try:
        await page.goto("https://www.amazon.com", wait_until="domcontentloaded", timeout=15000)
        await asyncio.sleep(1)

        # Click location selector
        try:
            await page.click("#nav-global-location-popover-link", timeout=3000)
            await asyncio.sleep(1)
        except:
            return False

        # Enter ZIP code
        try:
            await page.fill("#GLUXZipUpdateInput", zipcode, timeout=3000)
            await asyncio.sleep(0.5)
            await page.click("input[aria-labelledby='GLUXZipUpdate-announce']", timeout=3000)
            await asyncio.sleep(2)
            return True
        except:
            return False
    except Exception as e:
        print(f"Location setup failed: {e}")
        return False


async def scrape_one(page, asin: str) -> dict:
    """Scrape product data from Amazon product page."""
    url = f"https://www.amazon.com/dp/{asin}"

    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)  # Give more time for page to fully load

        # Check if product exists
        not_found = await page.query_selector('text="Sorry, we couldn\'t find that page"')
        if not_found:
            return {"status": "not_found", "asin": asin}

        # Debug: Save screenshot to see what page we got
        try:
            import base64
            screenshot = await page.screenshot()
            screenshot_b64 = base64.b64encode(screenshot).decode()
            print(f"[{asin}] Screenshot saved (first 100 chars): {screenshot_b64[:100]}")
        except Exception as e:
            print(f"[{asin}] Screenshot failed: {e}")

        # Check for CAPTCHA
        page_content = await page.content()
        if "captcha" in page_content.lower() or "robot" in page_content.lower():
            print(f"[{asin}] ⚠️  CAPTCHA or bot detection page detected!")
            print(f"[{asin}] Page title: {await page.title()}")
            # Save HTML for debugging
            print(f"[{asin}] Page HTML (first 500 chars): {page_content[:500]}")

        # Debug: Log what we're trying to scrape
        print(f"[{asin}] Page loaded, starting extraction...")
        print(f"[{asin}] Page URL: {page.url}")
        print(f"[{asin}] Page title: {await page.title()}")

        # Extract product data
        result = {
            "status": "ok",
            "asin": asin,
            "url": url,
        }

        # Title
        try:
            title_el = await page.query_selector("#productTitle")
            if title_el:
                result["title"] = (await title_el.inner_text()).strip()
                print(f"[{asin}] ✓ Title found")
            else:
                print(f"[{asin}] ✗ Title not found")
        except Exception as e:
            print(f"[{asin}] ✗ Title error: {e}")

        # Price
        try:
            price_el = await page.query_selector(".a-price .a-offscreen")
            if price_el:
                result["price"] = (await price_el.inner_text()).strip()
        except:
            pass

        # Rating
        try:
            rating_el = await page.query_selector("span[data-hook='rating-out-of-text']")
            if rating_el:
                rating_text = (await rating_el.inner_text()).strip()
                match = re.search(r'([\d.]+)', rating_text)
                if match:
                    result["rating"] = float(match.group(1))
        except:
            pass

        # Reviews count
        try:
            reviews_el = await page.query_selector("#acrCustomerReviewText")
            if reviews_el:
                reviews_text = (await reviews_el.inner_text()).strip()
                match = re.search(r'([\d,]+)', reviews_text)
                if match:
                    result["reviews_count"] = int(match.group(1).replace(',', ''))
        except:
            pass

        # Main image
        try:
            img_el = await page.query_selector("#landingImage, #imgBlkFront")
            if img_el:
                result["main_image"] = await img_el.get_attribute("src")
        except:
            pass

        # All images
        try:
            images = []
            img_thumbnails = await page.query_selector_all(".imageThumbnail img")
            for thumb in img_thumbnails[:10]:
                src = await thumb.get_attribute("src")
                if src:
                    # Convert thumbnail to full size
                    full_src = re.sub(r'\._[^.]+_\.', '.', src)
                    images.append(full_src)
            if images:
                result["images"] = images
        except:
            pass

        # Brand
        try:
            brand_el = await page.query_selector("#bylineInfo")
            if brand_el:
                brand_text = (await brand_el.inner_text()).strip()
                result["brand"] = brand_text.replace("Visit the ", "").replace(" Store", "").replace("Brand: ", "")
        except:
            pass

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

        # Availability
        try:
            availability_el = await page.query_selector("#availability span")
            if availability_el:
                result["availability"] = (await availability_el.inner_text()).strip()
        except:
            pass

        # Features/Bullet points
        try:
            features = []
            feature_els = await page.query_selector_all("#feature-bullets li:not(.aok-hidden) span.a-list-item")
            for feat in feature_els[:10]:
                text = (await feat.inner_text()).strip()
                if text and len(text) > 5:
                    features.append(text)
            if features:
                result["features"] = features
        except:
            pass

        # Description
        try:
            desc_el = await page.query_selector("#productDescription p")
            if desc_el:
                result["description"] = (await desc_el.inner_text()).strip()
        except:
            pass

        # Product details
        try:
            details = {}
            detail_rows = await page.query_selector_all("#productDetails_detailBullets_sections1 tr")
            for row in detail_rows:
                try:
                    th = await row.query_selector("th")
                    td = await row.query_selector("td")
                    if th and td:
                        key = (await th.inner_text()).strip().rstrip(':')
                        value = (await td.inner_text()).strip()
                        details[key] = value
                except:
                    pass
            if details:
                result["product_details"] = details
        except:
            pass

        # Dimensions (alternative location)
        try:
            if "product_details" not in result:
                details = {}
                tech_detail_els = await page.query_selector_all("#prodDetails th, #prodDetails td")
                for i in range(0, len(tech_detail_els) - 1, 2):
                    try:
                        key = (await tech_detail_els[i].inner_text()).strip().rstrip(':')
                        value = (await tech_detail_els[i + 1].inner_text()).strip()
                        details[key] = value
                    except:
                        pass
                if details:
                    result["product_details"] = details
        except:
            pass

        # Category/Best Sellers Rank
        try:
            categories = []
            category_els = await page.query_selector_all("#wayfinding-breadcrumbs_feature_div ul li a")
            for cat in category_els:
                cat_text = (await cat.inner_text()).strip()
                if cat_text:
                    categories.append(cat_text)
            if categories:
                result["categories"] = categories
        except:
            pass

        # Variants (color, size, etc.)
        try:
            variants = {}

            # Color variants
            color_swatches = await page.query_selector_all("#variation_color_name li")
            if color_swatches:
                colors = []
                for swatch in color_swatches[:20]:
                    try:
                        title = await swatch.get_attribute("title")
                        if title:
                            colors.append(title)
                    except:
                        pass
                if colors:
                    variants["colors"] = colors

            # Size variants
            size_select = await page.query_selector("#native_dropdown_selected_size_name")
            if size_select:
                sizes = []
                size_options = await size_select.query_selector_all("option")
                for opt in size_options:
                    size_text = (await opt.inner_text()).strip()
                    if size_text and "Select" not in size_text:
                        sizes.append(size_text)
                if sizes:
                    variants["sizes"] = sizes

            if variants:
                result["variants"] = variants
        except:
            pass

        # Seller information
        try:
            seller_el = await page.query_selector("#sellerProfileTriggerId")
            if seller_el:
                result["seller"] = (await seller_el.inner_text()).strip()
            else:
                # Check for "Ships from and sold by Amazon"
                merchant_el = await page.query_selector("#merchant-info")
                if merchant_el:
                    result["seller"] = (await merchant_el.inner_text()).strip()
        except:
            pass

        return result

    except Exception as e:
        raise RuntimeError(f"Scraping failed: {str(e)}")
