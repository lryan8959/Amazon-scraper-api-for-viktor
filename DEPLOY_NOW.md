# 🚀 Deploy Your API Now - 3 Easy Methods

## Method 1: Railway Web UI (Easiest - 5 Minutes)

### Step 1: Login to Railway
1. Go to https://railway.app
2. Click "Login with GitHub" (or email)
3. Create account if needed

### Step 2: Deploy
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. If not connected, click "Connect GitHub" and authorize
4. Select your repository: `cravealicious-site`
5. Railway will auto-detect the Dockerfile in `/api`
6. Click **"Deploy"**

### Step 3: Configure
1. Click on your service
2. Go to **"Variables"** tab
3. Add these variables:
   ```
   API_KEYS=your-secret-key-here
   CACHE_TTL=3600
   MAX_BATCH=5
   US_ZIP=10001
   ```
4. Railway will automatically redeploy

### Step 4: Get Your URL
1. Go to **"Settings"** tab
2. Click **"Generate Domain"**
3. Copy your URL: `https://your-app.up.railway.app`

### Step 5: Test
```bash
curl -H "X-API-Key: your-secret-key-here" \
  "https://your-app.up.railway.app/health"
```

**Done! ✅**

---

## Method 2: Render (Also Very Easy)

### Step 1: Create Account
1. Go to https://render.com
2. Sign up with GitHub

### Step 2: Deploy
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `amazon-scraper-api`
   - **Environment**: `Docker`
   - **Region**: Choose closest to you
   - **Plan**: Free or Starter ($7/month)
   - **Dockerfile Path**: Leave blank (auto-detected)
   - **Docker Build Context Directory**: `./api`

### Step 3: Add Environment Variables
```
API_KEYS=your-secret-key-here
CACHE_TTL=3600
MAX_BATCH=5
US_ZIP=10001
MAX_RETRIES=2
```

### Step 4: Deploy
Click **"Create Web Service"**

You'll get a URL like: `https://amazon-scraper-api.onrender.com`

**Done! ✅**

---

## Method 3: Docker on Your Own Server (Full Control)

If you have a VPS (DigitalOcean, AWS, etc.):

### Quick Deploy:
```bash
# 1. SSH into your server
ssh user@your-server.com

# 2. Clone your repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO/api

# 3. Create .env file
cat > .env << EOF
API_KEYS=$(openssl rand -hex 16)
CACHE_TTL=3600
MAX_BATCH=5
US_ZIP=10001
MAX_RETRIES=2
EOF

# 4. Run with Docker
docker-compose up -d

# 5. Get your API key
grep API_KEYS .env

# Your API is now at: http://your-server-ip:8000
```

**Done! ✅**

---

## Method 4: Railway CLI (Once You Login)

Since Railway requires browser login, here's the manual process:

```bash
# 1. Install Railway CLI
brew install railway

# 2. Login (opens browser)
railway login

# 3. Go to project
cd api

# 4. Create project on Railway
railway init

# 5. Add variables
railway variables --set "API_KEYS=$(openssl rand -hex 16)"
railway variables --set "CACHE_TTL=3600"
railway variables --set "MAX_BATCH=5"

# 6. Deploy
railway up

# 7. Get domain
railway domain
```

---

## 🎯 Recommendation

**For fastest deployment: Use Method 1 (Railway Web UI)**

1. Push code to GitHub
2. Connect to Railway via web
3. Deploy in 1 click
4. Add environment variables
5. Done!

**Total time: 5 minutes**

---

## 📋 Before You Deploy

### Push to GitHub First:
```bash
# In your project root
git add .
git commit -m "Add Amazon scraper API"
git branch -M main

# Create new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Generate API Key:
```bash
openssl rand -hex 16
# Save this key!
```

---

## ✅ After Deployment Checklist

- [ ] API is accessible
- [ ] Health endpoint works: `/health`
- [ ] Can scrape products: `/v1/product?url=B01LXJG04I`
- [ ] API key authentication works
- [ ] API documentation accessible: `/docs`
- [ ] Saved API key securely
- [ ] Added domain to documentation
- [ ] Set up monitoring (optional)

---

## 🆘 Need Help?

**Railway Support:**
- Dashboard: https://railway.app
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

**Render Support:**
- Dashboard: https://dashboard.render.com
- Docs: https://render.com/docs
- Support: support@render.com

**General API Issues:**
- Check logs in platform dashboard
- Verify environment variables are set
- Ensure Docker build succeeded
- Test locally first: `docker-compose up`

---

**Next Step:** Choose Method 1 or 2 and deploy in 5 minutes! 🚀
