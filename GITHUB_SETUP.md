# 📦 Push Your Code to GitHub

Before deploying to Railway or Render, you need to push your code to GitHub.

## Quick Setup (5 Minutes)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `amazon-scraper-api` (or your preferred name)
3. Description: "Amazon Product Scraper API with 21+ data fields"
4. Choose **Public** or **Private**
5. **DON'T** initialize with README, .gitignore, or license
6. Click **"Create repository"**

### Step 2: Initialize Git (if not already)

```bash
cd /Users/mac/Downloads/cravealicious-site

# Check if git is initialized
git status

# If not initialized:
git init
```

### Step 3: Add and Commit Files

```bash
# Add all files
git add .

# Check what will be committed
git status

# Commit
git commit -m "Initial commit: Amazon scraper API v1.1.0

- FastAPI application with 21+ data fields
- Product scraping with Playwright
- Store URL extraction
- Docker support
- Railway/Render deployment ready"
```

### Step 4: Connect to GitHub

```bash
# Replace YOUR_USERNAME and YOUR_REPO with your actual values
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Example:
# git remote add origin https://github.com/johndoe/amazon-scraper-api.git
```

### Step 5: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

**Done! ✅** Your code is now on GitHub.

---

## Verify Upload

Go to your GitHub repository URL:
```
https://github.com/YOUR_USERNAME/YOUR_REPO
```

You should see:
- `/api` directory with all your code
- `README.md`
- `Dockerfile`
- All documentation files

---

## Update .gitignore (Important!)

Make sure sensitive files aren't committed:

```bash
# Check if .gitignore exists
cat .gitignore

# If needed, create/update it
cat >> .gitignore << 'EOF'

# Environment variables
.env
.env.local
.env.production
.railway-credentials.txt

# Python
__pycache__/
*.pyc
*.pyo
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
EOF
```

If you accidentally committed sensitive files:

```bash
# Remove from git but keep locally
git rm --cached .env
git rm --cached .railway-credentials.txt

# Commit the removal
git commit -m "Remove sensitive files"
git push
```

---

## Now Deploy!

Once your code is on GitHub, choose a deployment method:

### Option 1: Railway (Recommended)
1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-deploy!

### Option 2: Render
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub
4. Select your repository
5. Configure and deploy!

See [DEPLOY_NOW.md](DEPLOY_NOW.md) for detailed instructions.

---

## Common Issues

### Authentication Required

If GitHub asks for authentication:

```bash
# Use GitHub Personal Access Token
# Generate at: https://github.com/settings/tokens

# When pushing, use:
git push https://YOUR_TOKEN@github.com/YOUR_USERNAME/YOUR_REPO.git main
```

Or set up SSH:
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: Settings → SSH Keys → New SSH key
cat ~/.ssh/id_ed25519.pub

# Use SSH URL
git remote set-url origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
git push
```

### Large Files

If you have large files (>100MB):

```bash
# Check file sizes
du -sh * | sort -h

# Remove large files from git
git rm --cached path/to/large/file
echo "path/to/large/file" >> .gitignore
git commit -m "Remove large files"
```

### Permission Denied

```bash
# Check remote URL
git remote -v

# Fix URL if needed
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

---

## Update Your Repository Later

After making changes:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with descriptive message
git commit -m "Add store URL extraction feature"

# Push to GitHub
git push
```

If using Railway/Render with auto-deploy enabled, your app will automatically update!

---

**Next:** Deploy using [DEPLOY_NOW.md](DEPLOY_NOW.md) 🚀
