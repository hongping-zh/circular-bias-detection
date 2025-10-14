# 🔍 Sleuth - AI Evaluation Bias Hunter

Single-page web application for detecting circular reasoning bias in algorithm evaluation.

**🌐 Live Demo:** https://hongping-zh.github.io/circular-bias-detection/

---

## 📚 Documentation

- **[Quick Start Guide](./QUICK_START.md)** - Get started in 2 minutes
- **[Full User Guide](./USER_GUIDE_EN.md)** - Complete documentation
- **[中文用户指南](./USER_GUIDE_CN.md)** - Chinese documentation

---

## ✨ Features

- ✅ **Upload CSV** - Analyze your own evaluation data
- ✅ **Example Data** - Try with sample data from Zenodo
- ✅ **Synthetic Data** - Generate test scenarios
- ✅ **Instant Analysis** - Results in under 1 minute
- ✅ **Privacy-First** - All computation in your browser (no server uploads)
- ✅ **Open Source** - Free and transparent (CC BY 4.0)

---

## 🚀 Tech Stack

- **React** - UI framework
- **Vite** - Build tool
- **PyOdide** - Python in the browser (planned)
- **GitHub Pages** - Free hosting

---

## 💻 Development

### Install dependencies
```bash
npm install
```

### Start dev server
```bash
npm run dev
```

Visit: http://localhost:5173/

### Build for production
```bash
npm run build
```

### Deploy to GitHub Pages
```bash
npm run deploy
```

---

## 📊 Data Format

CSV file must contain these columns:

| Column | Type | Description |
|--------|------|-------------|
| `time_period` | int | Evaluation period (1, 2, 3, ...) |
| `algorithm` | str | Algorithm name |
| `performance` | float | Performance metric [0-1] |
| `constraint_compute` | float | Computational constraint |
| `constraint_memory` | float | Memory constraint (GB) |
| `constraint_dataset_size` | int | Dataset size |
| `evaluation_protocol` | str | Protocol version |

**Example:**
```csv
time_period,algorithm,performance,constraint_compute,constraint_memory,constraint_dataset_size,evaluation_protocol
1,ResNet,0.72,300,8.0,50000,ImageNet-v1.0
1,VGG,0.68,450,12.0,50000,ImageNet-v1.0
```

---

## 🔗 Links

- **GitHub Repository:** https://github.com/hongping-zh/circular-bias-detection
- **Dataset:** https://doi.org/10.5281/zenodo.17201032
- **Paper:** (Submitted to JASA)

---

## 📝 License

CC BY 4.0 - Free to use, share, and adapt with attribution.

---

**Version:** 1.0.0 (MVP - Test Mode)  
**Updated:** October 2024
