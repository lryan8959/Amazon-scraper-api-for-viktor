# ✅ Deployment Checklist

Follow this checklist to deploy your Amazon Scraper API.

## Pre-Deployment

- [ ] **API Code Ready**
  - [x] app.py created
  - [x] scraper.py created
  - [x] Dockerfile created
  - [x] requirements.txt created
  - [x] Store URL feature added

- [ ] **Generate API Key**
  ```bash
  openssl rand -hex 16
  ```
  Save this key! You'll need it.

- [ ] **Test Locally (Optional but Recommended)**
  ```bash
  cd api
  docker-compose up -d
  curl http://localhost:8000/health
  ```

## GitHub Setup

- [ ] **Create GitHub Repository**
  - Go to https://github.com/new
  - Name: `amazon-scraper-api`
  - Visibility: Public or Private
  - Click "Create repository"

- [ ] **Push Code**
  ```bash
  git add .
  git commit -m "Initial commit: Amazon scraper API"
  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
  git branch -M main
  git push -u origin main
  ```

- [ ] **Verify Upload**
  - Visit your GitHub repo
  - Confirm `/api` directory exists
  - Confirm Dockerfile is present

## Deploy to Railway

- [ ] **Login to Railway**
  - Go to https://railway.app
  - Click "Login with GitHub"
  - Authorize Railway

- [ ] **Create New Project**
  - Click "New Project"
  - Select "Deploy from GitHub repo"
  - Choose your repository

- [ ] **Configure Variables**
  - Go to "Variables" tab
  - Add:
    - `API_KEYS` = your-generated-key
    - `CACHE_TTL` = 3600
    - `MAX_BATCH` = 5
    - `US_ZIP` = 10001

- [ ] **Generate Domain**
  - Go to "Settings" tab
  - Click "Generate Domain"
  - Copy your URL

- [ ] **Wait for Deployment**
  - Check "Deployments" tab
  - Wait for "Success" status (2-5 minutes)

## Testing

- [ ] **Test Health Endpoint**
  ```bash
  curl https://your-app.railway.app/health
  ```

- [ ] **Test Product Scraping**
  ```bash
  curl -H "X-API-Key: YOUR_KEY" \
    "https://your-app.railway.app/v1/product?url=B01LXJG04I"
  ```

- [ ] **Test Store URL Field**
  ```bash
  curl -H "X-API-Key: YOUR_KEY" \
    "https://your-app.railway.app/v1/product?url=B01LXJG04I" \
    | jq '.store_url'
  ```

- [ ] **View API Documentation**
  - Visit: `https://your-app.railway.app/docs`

## Post-Deployment

- [ ] **Save Credentials**
  - API URL: _________________________
  - API Key: _________________________
  - Deployment Date: _________________

- [ ] **Update Documentation**
  - Add your API URL to README
  - Share API key with team (securely)

- [ ] **Set Up Monitoring (Optional)**
  - Railway dashboard for metrics
  - Set up alerts for downtime

- [ ] **Test All Endpoints**
  - [ ] GET /health
  - [ ] GET /v1/product
  - [ ] POST /v1/product
  - [ ] POST /v1/jobs
  - [ ] GET /v1/jobs/{job_id}

## Success! 🎉

Your API is now live at: `https://your-app.railway.app`

## Troubleshooting

### Deployment Failed
- Check Railway logs in dashboard
- Verify Dockerfile syntax
- Check environment variables

### API Returns 401
- Verify API key is correct
- Check X-API-Key header format

### Scraping Fails
- Check Railway logs
- Verify Chromium installed in Docker
- May need to increase memory limits

### Need Help?
- Railway Support: https://discord.gg/railway
- API Docs: See DEPLOY_NOW.md
- GitHub Issues: (create in your repo)

---

**Deployment Time Estimate:**
- GitHub setup: 2 minutes
- Railway deployment: 5 minutes
- Testing: 2 minutes
**Total: ~10 minutes**

**Monthly Cost:**
- Railway Starter: $5/month
- Render: $7/month (or free with limitations)
- Self-hosted: Variable (server cost only)
