# 🚀 Deployment Checklist

## Pre-Deployment Steps

### 1. Install Chart.js (REQUIRED)

```bash
cd C:\Users\14593\CascadeProjects\circular-bias-detection\web-app
npm install chart.js react-chartjs-2
```

**Verify installation:**
```bash
npm list chart.js react-chartjs-2
```

Should show:
```
├── chart.js@4.x.x
└── react-chartjs-2@5.x.x
```

---

### 2. Test Locally

```bash
npm run dev
```

Visit: http://localhost:5173

**Test checklist:**
- [ ] Tutorial opens automatically
- [ ] Upload invalid CSV → see error message
- [ ] Upload valid CSV → see success message
- [ ] Click "Scan for Bias" → see progress bar
- [ ] View results → see 3 interactive charts
- [ ] Click "❓ Help" → tutorial reopens

---

### 3. Git Commit (When Ready)

```bash
git add -A
git commit -m "feat: Add error handling, visualizations, and interactive tutorial

Enhancements:
- Enhanced error handling with detailed validation messages
- Interactive Chart.js visualizations (PSI, rho_PC, indicators)
- 7-step interactive tutorial for onboarding
- LLM evaluation example integration

New files: ~1200 lines
Dependencies: chart.js, react-chartjs-2"

git push origin main
```

---

### 4. Deploy to GitHub Pages

**Option A: When network is stable**
```bash
cd C:\Users\14593\CascadeProjects\circular-bias-detection\web-app
npm run deploy
```

**Option B: Manual Git deployment**
```bash
npm run build
cd dist
git init
git add -A
git commit -m "Deploy: Error handling + Visualizations + Tutorial"
git branch -M gh-pages
git push -f https://github.com/hongping-zh/circular-bias-detection.git gh-pages
cd ..
```

---

## Post-Deployment Verification

Visit: https://hongping-zh.github.io/circular-bias-detection/

### Check:
- [ ] Tutorial auto-opens on first visit
- [ ] "❓ Help" button visible in header
- [ ] Upload CSV → validation feedback
- [ ] Scan → progress bar with 6 steps
- [ ] Results → 3 charts visible
- [ ] Charts are interactive (hover tooltips)
- [ ] Mobile responsive

---

## Troubleshooting

### Issue: Charts don't render

**Solution:** Chart.js not installed
```bash
npm install chart.js react-chartjs-2
npm run build
npm run deploy
```

### Issue: Tutorial doesn't show

**Solution:** Clear localStorage
```javascript
// In browser console:
localStorage.removeItem('sleuth_tutorial_completed');
// Refresh page
```

### Issue: Network timeout during deploy

**Solution:** Use manual Git deployment (Option B above)

---

## File Checklist

### Committed Files:
- [ ] `src/utils/dataValidator.js`
- [ ] `src/components/ValidationMessage.jsx`
- [ ] `src/components/ValidationMessage.css`
- [ ] `src/components/VisualizationCharts.jsx`
- [ ] `src/components/VisualizationCharts.css`
- [ ] `src/components/InteractiveTutorial.jsx`
- [ ] `src/components/InteractiveTutorial.css`
- [ ] `src/App.jsx` (modified)
- [ ] `src/App.css` (modified)
- [ ] `src/components/DataInput.jsx` (modified)
- [ ] `src/components/Dashboard.jsx` (modified)
- [ ] `ENHANCEMENTS.md`
- [ ] `INSTALL_CHARTJS.md`
- [ ] `DEPLOYMENT_CHECKLIST.md`

### package.json Should Include:
```json
"dependencies": {
  "chart.js": "^4.x.x",
  "react-chartjs-2": "^5.x.x"
}
```

---

## Quick Commands Reference

```bash
# Install dependencies
npm install chart.js react-chartjs-2

# Test locally
npm run dev

# Build for production
npm run build

# Deploy (automated)
npm run deploy

# Deploy (manual)
cd dist && git init && git add -A && git commit -m "Deploy" && git branch -M gh-pages && git push -f https://github.com/hongping-zh/circular-bias-detection.git gh-pages && cd ..
```

---

## Done! ✅

When all checks pass:
1. ✅ Chart.js installed
2. ✅ Local testing complete
3. ✅ Git committed
4. ✅ Deployed to GitHub Pages
5. ✅ Live site verified

**Sleuth is now enhanced with professional error handling, visualizations, and onboarding!** 🎉
