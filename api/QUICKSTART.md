# Quick Start Guide

## 1. Local Testing (5 minutes)

### Using Docker (Easiest)
```bash
cd api
chmod +x deploy.sh
./deploy.sh
```

Your API will be running at: `http://localhost:8000`

### Using Python
```bash
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
uvicorn app:app --reload
```

## 2. Test It

```bash
# Replace with your API key from .env
API_KEY="demo-key-12345"

# Test health
curl http://localhost:8000/health

# Test scraping
curl -H "X-API-Key: $API_KEY" \
  "http://localhost:8000/v1/product?url=B07B3NJDNB"
```

## 3. Deploy to Cloud (10 minutes)

### Railway (Recommended)
1. Push code to GitHub
2. Go to https://railway.app
3. Click "New Project" → "Deploy from GitHub"
4. Select your repo
5. Add environment variable: `API_KEYS=your-secret-key`
6. Done! You'll get a URL like: `https://your-app.railway.app`

### Render
1. Push code to GitHub
2. Go to https://render.com
3. New → Web Service
4. Connect repo → Select `api` directory
5. Add env vars
6. Deploy!

### Fly.io
```bash
cd api
fly launch
fly secrets set API_KEYS=your-secret-key
fly deploy
```

## 4. Use Your API

```python
import requests

API_URL = "https://your-app.railway.app"
API_KEY = "your-api-key"

headers = {"X-API-Key": API_KEY}

# Single product
response = requests.get(
    f"{API_URL}/v1/product",
    params={"url": "B07B3NJDNB"},
    headers=headers
)
product = response.json()
print(f"{product['title']}: {product['price']}")

# Batch job
job = requests.post(
    f"{API_URL}/v1/jobs",
    json={"urls": ["B07B3NJDNB", "B08N5WRWNW"]},
    headers=headers
).json()

# Check job status
import time
while True:
    status = requests.get(
        f"{API_URL}/v1/jobs/{job['job_id']}",
        headers=headers
    ).json()
    print(f"Status: {status['status']}")
    if status['status'] == 'done':
        break
    time.sleep(10)

for product in status['products']:
    print(f"{product['title']}: {product['price']}")
```

## Troubleshooting

**Port already in use?**
```bash
# Change port
uvicorn app:app --port 8001
```

**Docker issues?**
```bash
# Check logs
docker-compose logs -f

# Restart
docker-compose restart

# Clean rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up
```

**Scraping fails?**
- Amazon might be blocking your IP
- Try setting `US_ZIP=10001` and `REQUIRE_US_ZIP=1` in .env
- Check if the ASIN is valid
- Look at API logs for details

## Next Steps

- Read [README.md](README.md) for full API documentation
- Read [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Check [/docs](http://localhost:8000/docs) for interactive API docs
- Run `python test_client.py` for comprehensive tests

## Support

- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- GitHub Issues: (your repo)/issues
