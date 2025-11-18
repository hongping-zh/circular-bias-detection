# Branding & Naming Strategy

## 🎯 Brand Identity

**Primary Brand Name**: **Sleuth**  
**Tagline**: AI Bias Detector

## 📋 Naming Convention

This project uses different identifiers at different levels:

| Context | Name | Rationale | Change Status |
|---------|------|-----------|---------------|
| **Brand/Marketing** | **Sleuth** | Memorable, easy to say, implies detective work | ✅ Active |
| **GitHub Repository** | `circular-bias-detection` | Technical descriptor, SEO-friendly | 🔒 Fixed (URLs exist) |
| **PyPI Package** | `circular-bias-detector` | Python naming convention | 🔒 Fixed (published) |
| **Website Domain** | `biasdetector.vercel.app` | Descriptive, established | 🔒 Fixed (deployed) |
| **CLI Command** | `circular-bias` | Matches package name | 🔒 Fixed (installed base) |

## 💡 Why This Strategy?

### 1. **Brand Name: "Sleuth"**
- **Short & Memorable**: One word vs. 3-4 words
- **Metaphor**: Detective finding hidden biases
- **Differentiation**: Stands out in search results
- **Professional**: Sounds like a product, not just a script

### 2. **Technical Identifiers: "circular-bias-detection"**
- **Descriptive**: Clear what it does for technical users
- **SEO**: Keywords for search engines
- **Stability**: URLs and package names should not change
- **Consistency**: Follows Python/GitHub conventions

## 📝 Usage Guidelines

### ✅ DO Use "Sleuth" When:
- Writing marketing copy
- Creating presentations
- Talking to non-technical users
- Social media posts
- Blog articles
- README introduction/hero section
- Website content

### ✅ DO Use "circular-bias-detection" When:
- Installing via pip: `pip install circular-bias-detector`
- Importing in code: `from circular_bias_detector import ...`
- Linking to GitHub repo
- CLI commands: `circular-bias detect`
- Technical documentation
- DOI citations (can mention both)

### ✅ Best Practice: Combine Both
**Recommended format**: "Sleuth (`circular-bias-detector`)"

**Examples**:
- "Install Sleuth: `pip install circular-bias-detector`"
- "Sleuth is available on GitHub at hongping-zh/circular-bias-detection"
- "The Sleuth framework (`circular-bias-detector`) provides..."

## 🌐 External References

### Academic Citations
Use official software citation with both names:

```bibtex
@software{zhang2024sleuth,
  author       = {Zhang, Hongping},
  title        = {Sleuth: Circular Bias Detection for AI Evaluations},
  year         = {2024},
  publisher    = {Zenodo},
  version      = {v1.0.0},
  doi          = {10.5281/zenodo.17201032},
  url          = {https://github.com/hongping-zh/circular-bias-detection}
}
```

### URLs
- **Live Demo**: https://is.gd/check_sleuth (short URL)
- **GitHub**: https://github.com/hongping-zh/circular-bias-detection
- **PyPI**: https://pypi.org/project/circular-bias-detector/
- **Web App**: https://biasdetector.vercel.app/

## 🔄 Current Status

**Completed**:
- ✅ README updated with brand note at top
- ✅ All "Try Live Demo" → "Try Sleuth" buttons
- ✅ setup.py description includes "Sleuth"
- ✅ pyproject.toml description includes "Sleuth"
- ✅ CITATION.cff uses "Sleuth"
- ✅ README consistently uses "Sleuth" in user-facing text

**No Changes Needed**:
- 🔒 GitHub repository name (URLs already exist)
- 🔒 PyPI package name (already published)
- 🔒 Web app domain (user decision to keep as-is)
- 🔒 CLI command name (installed base exists)

## 🎨 Brand Assets

### Logo/Icon
Currently using 🔍 (magnifying glass) emoji consistently

### Color Scheme
- **Primary**: Green (#28a745) - for success/safe results
- **Warning**: Yellow (#ffc107) - for moderate risk
- **Danger**: Red (#dc3545) - for detected bias

### Voice & Tone
- **Professional but approachable**
- **Technically accurate**
- **Action-oriented** (Fix, Detect, Prevent)

## 📞 Questions?

If you're unsure which name to use, ask:
1. **Is this user-facing?** → Use "Sleuth"
2. **Is this technical/code?** → Use "circular-bias-detection/detector"
3. **Academic paper?** → Use both in citation

---

**Last Updated**: 2025-11-08  
**Version**: 1.0  
**Maintainer**: Hongping Zhang
