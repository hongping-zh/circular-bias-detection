# 🚀 Web App Setup Guide

## Step 1: Wait for React Project Creation

The `create-react-app` command is running. Wait for it to complete (2-3 minutes).

---

## Step 2: Copy Files to React Project

Once `create-react-app` finishes, copy the prepared files:

```bash
# Copy source files
xcopy /E /I web-app-files\src web-app\src
xcopy /E /I web-app-files\public web-app\public
copy web-app-files\README.md web-app\README.md

# Or manually:
# 1. Copy web-app-files/src/* to web-app/src/
# 2. Copy web-app-files/public/index.html to web-app/public/
# 3. Copy web-app-files/README.md to web-app/
```

---

## Step 3: Install Dependencies

```bash
cd web-app
npm install
```

---

## Step 4: Test Locally

```bash
npm start
```

This will open http://localhost:3000

**Test checklist:**
- [ ] Page loads without errors
- [ ] "Loading Python engine..." appears (30 sec first time)
- [ ] Upload CSV works
- [ ] "Try Example" button works
- [ ] "Generate Synthetic" button works
- [ ] Scan button becomes enabled after loading data
- [ ] Clicking Scan shows results
- [ ] Download button works

---

## Step 5: Build for Production

```bash
npm run build
```

This creates an optimized build in `build/` folder.

---

## Step 6: Deploy to GitHub Pages

### Option A: Manual Deployment

1. **Install gh-pages package:**
```bash
npm install --save-dev gh-pages
```

2. **Add to package.json:**
```json
{
  "homepage": "https://hongping-zh.github.io/circular-bias-detection",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  }
}
```

3. **Deploy:**
```bash
npm run deploy
```

### Option B: GitHub Actions (Automated)

Create `.github/workflows/deploy-web-app.yml`:

```yaml
name: Deploy Web App

on:
  push:
    branches: [main]
    paths:
      - 'web-app/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 18
      
      - name: Install and Build
        run: |
          cd web-app
          npm install
          npm run build
      
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./web-app/build
```

---

## Step 7: Configure GitHub Pages

1. Go to: https://github.com/hongping-zh/circular-bias-detection/settings/pages
2. Source: Select `gh-pages` branch
3. Root: Select `/ (root)`
4. Click Save

Wait 1-2 minutes, then visit:
```
https://hongping-zh.github.io/circular-bias-detection/
```

---

## Troubleshooting

### Issue: Pyodide loading timeout

**Solution:** Check browser console, try refreshing page

### Issue: CSV parsing error

**Solution:** Ensure CSV has required columns:
- time_period
- algorithm
- performance
- constraint_compute
- constraint_memory
- constraint_dataset_size
- evaluation_protocol

### Issue: GitHub Pages 404

**Solution:** 
1. Check Settings > Pages enabled
2. Ensure `homepage` in package.json is correct
3. Wait 2-3 minutes for deployment

---

## Custom Domain (Optional)

1. Buy domain (e.g., bias-scanner.app)
2. Add CNAME record pointing to: `hongping-zh.github.io`
3. Create `public/CNAME` file with your domain
4. Redeploy

---

## Next Steps

After deployment:
1. Test on mobile devices
2. Share link on Twitter/LinkedIn
3. Submit to Product Hunt
4. Post on HackerNews

---

## Support

- **Issues**: https://github.com/hongping-zh/circular-bias-detection/issues
- **Dataset**: https://doi.org/10.5281/zenodo.17201032
