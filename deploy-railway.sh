#!/bin/bash

echo "🚂 Deploying Amazon Scraper API to Railway"
echo "==========================================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Railway CLI not found. Installing..."

    # Detect OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo "Installing via Homebrew..."
            brew install railway
        else
            echo "Installing via curl..."
            curl -fsSL https://railway.app/install.sh | sh
        fi
    else
        # Linux/WSL
        echo "Installing via curl..."
        curl -fsSL https://railway.app/install.sh | sh
    fi

    echo "✅ Railway CLI installed!"
    echo ""
fi

# Verify installation
echo "Railway CLI version: $(railway --version)"
echo ""

# Check if already logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Logging in to Railway..."
    railway login
    echo ""
else
    echo "✅ Already logged in as: $(railway whoami)"
    echo ""
fi

# Check if project is already linked
if railway status &> /dev/null; then
    echo "✅ Project already linked to Railway"
    echo ""
else
    echo "🎯 Initializing Railway project..."
    railway init
    echo ""
fi

# Generate API key
echo "🔑 Generating secure API key..."
API_KEY=$(openssl rand -hex 16)
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚠️  IMPORTANT - SAVE THIS API KEY!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "API_KEY: $API_KEY"
echo ""
echo "You will need this key to access your API!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Ask user to confirm
read -p "Press Enter to continue deployment..."

# Set environment variables
echo "⚙️  Setting environment variables..."
railway variables set API_KEYS="$API_KEY" > /dev/null
railway variables set CACHE_TTL=3600 > /dev/null
railway variables set MAX_BATCH=5 > /dev/null
railway variables set US_ZIP=10001 > /dev/null
railway variables set MAX_RETRIES=2 > /dev/null
railway variables set REQUIRE_US_ZIP=0 > /dev/null
echo "✅ Environment variables set"
echo ""

# Deploy
echo "🚀 Deploying to Railway..."
echo "(This may take 2-5 minutes...)"
echo ""
railway up

# Check deployment status
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment successful!"
    echo ""

    # Get domain
    echo "🌐 Getting deployment URL..."
    DOMAIN=$(railway domain 2>/dev/null)

    if [ -z "$DOMAIN" ]; then
        echo "⚠️  Domain not ready yet. Generating one..."
        railway domain create > /dev/null 2>&1
        sleep 2
        DOMAIN=$(railway domain 2>/dev/null)
    fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎉 DEPLOYMENT COMPLETE!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📍 API URL: https://$DOMAIN"
    echo "🔑 API Key: $API_KEY"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 TEST YOUR API:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1. Health Check:"
    echo "   curl https://$DOMAIN/health"
    echo ""
    echo "2. Test Product Scraping:"
    echo "   curl -H 'X-API-Key: $API_KEY' \\"
    echo "     'https://$DOMAIN/v1/product?url=B01LXJG04I'"
    echo ""
    echo "3. API Documentation:"
    echo "   https://$DOMAIN/docs"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 USEFUL COMMANDS:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "View logs:         railway logs -f"
    echo "Open dashboard:    railway open"
    echo "Project status:    railway status"
    echo "View variables:    railway variables"
    echo "Redeploy:          railway up"
    echo ""

    # Save credentials to file
    cat > .railway-credentials.txt << EOF
Railway Deployment Credentials
===============================

API URL: https://$DOMAIN
API Key: $API_KEY

Deployed: $(date)

Test Commands:
--------------
curl https://$DOMAIN/health
curl -H 'X-API-Key: $API_KEY' 'https://$DOMAIN/v1/product?url=B01LXJG04I'

Dashboard: https://railway.app
Docs: https://$DOMAIN/docs
EOF

    echo "💾 Credentials saved to: .railway-credentials.txt"
    echo ""
    echo "⚠️  Keep this file secure and do not commit to git!"
    echo ""

else
    echo ""
    echo "❌ Deployment failed!"
    echo ""
    echo "Check logs with: railway logs"
    echo "Try again with: railway up"
    echo ""
    exit 1
fi
