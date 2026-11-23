#!/bin/bash

# Test script for your deployed Amazon Scraper API
# Your API: https://amazon-scraper-api-for-viktor-production.up.railway.app

API_URL="https://amazon-scraper-api-for-viktor-production.up.railway.app"
API_KEY="715bbbcda6fae35385f88bc58001c535"

echo "🧪 Testing Your Deployed API"
echo "=============================="
echo ""
echo "API URL: $API_URL"
echo "API Key: $API_KEY"
echo ""

# Test 1: Health Check
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  Testing Health Endpoint"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
curl -s "$API_URL/health" | jq . || curl -s "$API_URL/health"
echo ""
echo ""

# Test 2: Product Scraping
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  Testing Product Scraping (ASIN: B01LXJG04I)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⏳ This may take 10-15 seconds for first request..."
echo ""

RESPONSE=$(curl -s -H "X-API-Key: $API_KEY" \
  "$API_URL/v1/product?url=B01LXJG04I")

# Check if jq is available
if command -v jq &> /dev/null; then
    echo "Full Response:"
    echo "$RESPONSE" | jq .
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 Key Fields:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Status:      $(echo "$RESPONSE" | jq -r '.status')"
    echo "ASIN:        $(echo "$RESPONSE" | jq -r '.asin')"
    echo "Title:       $(echo "$RESPONSE" | jq -r '.title')"
    echo "Price:       $(echo "$RESPONSE" | jq -r '.price')"
    echo "Rating:      $(echo "$RESPONSE" | jq -r '.rating')"
    echo "Reviews:     $(echo "$RESPONSE" | jq -r '.reviews_count')"
    echo "Brand:       $(echo "$RESPONSE" | jq -r '.brand')"
    echo "Store URL:   $(echo "$RESPONSE" | jq -r '.store_url')"
    echo "Cached:      $(echo "$RESPONSE" | jq -r '.cached')"
else
    echo "$RESPONSE"
    echo ""
    echo "💡 Tip: Install jq for pretty output: brew install jq"
fi

echo ""
echo ""

# Test 3: Check specific features
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  Verifying New Features"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

STORE_URL=$(echo "$RESPONSE" | jq -r '.store_url' 2>/dev/null || echo "")
if [ -n "$STORE_URL" ] && [ "$STORE_URL" != "null" ]; then
    echo "✅ Store URL extraction: WORKING"
    echo "   $STORE_URL"
else
    echo "❌ Store URL extraction: NOT FOUND"
fi
echo ""

IMAGES_COUNT=$(echo "$RESPONSE" | jq -r '.images | length' 2>/dev/null || echo "0")
if [ "$IMAGES_COUNT" -gt 0 ]; then
    echo "✅ Images extraction: WORKING ($IMAGES_COUNT images)"
else
    echo "❌ Images extraction: NOT FOUND"
fi
echo ""

FEATURES_COUNT=$(echo "$RESPONSE" | jq -r '.features | length' 2>/dev/null || echo "0")
if [ "$FEATURES_COUNT" -gt 0 ]; then
    echo "✅ Features extraction: WORKING ($FEATURES_COUNT features)"
else
    echo "❌ Features extraction: NOT FOUND"
fi
echo ""

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Testing Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📖 API Documentation:"
echo "   $API_URL/docs"
echo ""
echo "🔍 View Logs:"
echo "   railway logs -f"
echo ""
