# Deploy to Railway Using CLI

## Step-by-Step Guide

### 1. Install Railway CLI

**macOS/Linux:**
```bash
# Using Homebrew (recommended for macOS)
brew install railway

# OR using npm
npm i -g @railway/cli

# OR using curl
curl -fsSL https://railway.app/install.sh | sh
```

**Windows:**
```bash
# Using npm
npm i -g @railway/cli

# OR using Scoop
scoop install railway
```

Verify installation:
```bash
railway --version
```

### 2. Login to Railway

```bash
railway login
```

This will open your browser for authentication. Login with your Railway account.

### 3. Navigate to Your Project

```bash
cd /Users/mac/Downloads/cravealicious-site/api
```

### 4. Initialize Railway Project

```bash
# Create new Railway project
railway init
```

You'll be asked:
- **Project name**: `amazon-scraper-api` (or your preferred name)
- **Environment**: Choose "production" or "development"

### 5. Set Environment Variables

**Generate a secure API key:**
```bash
# Generate random API key
export API_KEY=$(openssl rand -hex 16)
echo "Your API Key: $API_KEY"
```

**Set the environment variables:**
```bash
# Set API key
railway variables set API_KEYS=$API_KEY

# Optional: Set other variables
railway variables set CACHE_TTL=3600
railway variables set MAX_BATCH=5
railway variables set US_ZIP=10001
railway variables set MAX_RETRIES=2
```

**View all variables:**
```bash
railway variables
```

### 6. Deploy Your API

```bash
# Deploy to Railway
railway up
```

This will:
- ✅ Build your Docker image
- ✅ Deploy to Railway
- ✅ Assign a public URL
- ✅ Start your service

**Monitor the deployment:**
```bash
# Watch logs in real-time
railway logs -f
```

### 7. Get Your API URL

```bash
# Get your deployment URL
railway domain
```

You'll get a URL like: `https://amazon-scraper-api-production.up.railway.app`

**Or generate a custom domain:**
```bash
railway domain create
```

### 8. Test Your Deployment

```bash
# Replace with your actual URL and API key
export API_URL="https://amazon-scraper-api-production.up.railway.app"
export API_KEY="your-api-key-from-step-5"

# Test health endpoint
curl "$API_URL/health"

# Test product scraping
curl -H "X-API-Key: $API_KEY" \
  "$API_URL/v1/product?url=B01LXJG04I"
```

## Complete Deployment Script

Save this as `deploy-railway.sh`:

```bash
#!/bin/bash

echo "🚂 Deploying to Railway"
echo "======================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    curl -fsSL https://railway.app/install.sh | sh
fi

# Login
echo "📝 Logging in to Railway..."
railway login

# Initialize project
echo "🎯 Initializing Railway project..."
railway init

# Generate and set API key
echo "🔑 Generating API key..."
API_KEY=$(openssl rand -hex 16)
echo "Your API Key: $API_KEY"
echo "SAVE THIS KEY - YOU'LL NEED IT TO ACCESS THE API!"
echo ""

# Set environment variables
echo "⚙️ Setting environment variables..."
railway variables set API_KEYS=$API_KEY
railway variables set CACHE_TTL=3600
railway variables set MAX_BATCH=5
railway variables set US_ZIP=10001
railway variables set MAX_RETRIES=2

# Deploy
echo "🚀 Deploying to Railway..."
railway up

# Get domain
echo ""
echo "🌐 Getting deployment URL..."
DOMAIN=$(railway domain)

echo ""
echo "✅ Deployment Complete!"
echo "======================="
echo "API URL: $DOMAIN"
echo "API Key: $API_KEY"
echo ""
echo "📊 Test your API:"
echo "curl -H 'X-API-Key: $API_KEY' '$DOMAIN/health'"
echo ""
echo "📖 View logs:"
echo "railway logs -f"
```

Make it executable and run:
```bash
chmod +x deploy-railway.sh
./deploy-railway.sh
```

## Useful Railway CLI Commands

### Project Management
```bash
# List all projects
railway list

# Link to existing project
railway link

# Open project in browser
railway open

# Delete project
railway delete
```

### Environment Variables
```bash
# List all variables
railway variables

# Set a variable
railway variables set KEY=VALUE

# Delete a variable
railway variables delete KEY
```

### Deployment
```bash
# Deploy current directory
railway up

# Deploy specific directory
railway up --directory ./api

# Deploy and watch logs
railway up && railway logs -f
```

### Logs & Monitoring
```bash
# View recent logs
railway logs

# Follow logs in real-time
railway logs -f

# View logs from specific service
railway logs -s amazon-scraper-api
```

### Domain Management
```bash
# Show current domain
railway domain

# Generate new domain
railway domain create

# Remove domain
railway domain delete
```

### Status & Info
```bash
# Show project status
railway status

# Show project info
railway whoami

# Show service details
railway service
```

## Update Deployment

After making code changes:

```bash
# 1. Commit your changes
git add .
git commit -m "Update API"

# 2. Deploy to Railway
railway up

# 3. Watch logs
railway logs -f
```

Or use automatic deployments (see below).

## Enable Automatic Deployments (GitHub)

1. **Push code to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

2. **Connect to Railway:**
```bash
# Open Railway dashboard
railway open

# In the Railway dashboard:
# Settings → Connect GitHub → Select your repository
```

Now every push to `main` branch will automatically deploy!

## Environment-Specific Deployments

### Production
```bash
railway environment production
railway variables set API_KEYS=prod-key-here
railway up
```

### Staging
```bash
railway environment staging
railway variables set API_KEYS=staging-key-here
railway up
```

## Troubleshooting

### Deployment fails
```bash
# Check logs
railway logs

# Check build logs
railway logs --build

# Try redeploying
railway up --force
```

### Port issues
Railway automatically sets `PORT` environment variable. Your app should use:
```python
port = int(os.getenv("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

This is already configured in your `Dockerfile`.

### Memory issues
```bash
# Open Railway dashboard
railway open

# Settings → Adjust memory/CPU limits
```

### Environment variable not working
```bash
# Verify variables are set
railway variables

# Restart the service
railway restart
```

## Cost Estimation

Railway pricing (as of 2024):
- **Starter Plan**: $5/month
- **Includes**: 500 hours execution time
- **Memory**: Up to 8GB RAM
- **Storage**: Up to 100GB

Your API typically uses:
- ~500MB-1GB RAM
- ~24/7 uptime = 720 hours/month

**Cost**: ~$5-10/month

## Monitoring

### View metrics in CLI
```bash
# Show recent activity
railway logs --tail 100

# Show service status
railway status
```

### View metrics in dashboard
```bash
# Open dashboard
railway open

# Navigate to: Metrics → View CPU, Memory, Network usage
```

## Backup API Key

**Save your API key securely:**
```bash
# View current API key
railway variables | grep API_KEYS

# Save to local file (DO NOT commit to git!)
echo "API_KEYS=$(railway variables | grep API_KEYS | cut -d'=' -f2)" > .env.production
```

## Next Steps

1. ✅ Deploy to Railway
2. ✅ Test all endpoints
3. ✅ Set up monitoring
4. ✅ Enable automatic deployments (GitHub)
5. ✅ Configure custom domain (optional)
6. ✅ Set up alerts for downtime
7. ✅ Implement rate limiting (production)

---

**Need Help?**
- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- CLI Help: `railway --help`
