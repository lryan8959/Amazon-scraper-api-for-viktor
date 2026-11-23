# ⚡ Quick Deploy Guide

## Deploy to Railway in 3 Steps

### 1️⃣ Install Railway CLI

**macOS:**
```bash
brew install railway
```

**Linux/WSL:**
```bash
curl -fsSL https://railway.app/install.sh | sh
```

**Windows:**
```bash
npm i -g @railway/cli
```

### 2️⃣ Run Deployment Script

```bash
cd /Users/mac/Downloads/cravealicious-site/api
./deploy-railway.sh
```

This will:
- ✅ Login to Railway
- ✅ Create project
- ✅ Generate API key
- ✅ Set environment variables
- ✅ Deploy your API
- ✅ Give you the URL

### 3️⃣ Test Your API

You'll get:
- **API URL**: `https://your-app.railway.app`
- **API Key**: `xxxxxxxxxxxxxxxx` (auto-generated)

```bash
# Test it
curl -H "X-API-Key: YOUR_KEY" \
  "https://your-app.railway.app/v1/product?url=B01LXJG04I"
```

---

## Manual Deployment (Step-by-Step)

If you prefer manual control:

```bash
# 1. Install CLI
brew install railway

# 2. Login
railway login

# 3. Navigate to project
cd api

# 4. Initialize
railway init

# 5. Set API key
railway variables set API_KEYS=$(openssl rand -hex 16)

# 6. Deploy
railway up

# 7. Get URL
railway domain
```

---

## Need Help?

See [DEPLOY_RAILWAY_CLI.md](DEPLOY_RAILWAY_CLI.md) for detailed instructions.

---

**Time**: ~5 minutes  
**Cost**: $5/month (Railway Starter)  
**Difficulty**: ⭐ Easy
