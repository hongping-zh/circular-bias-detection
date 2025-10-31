# 🎉 Sleuth v1.0 - Official Release

## AI Evaluation Bias Hunter - Now Live!

**Release Date**: October 15, 2025  
**Version**: 1.0.0  
**Status**: Stable

---

## 🚀 What is Sleuth?

Sleuth is a **free, browser-based tool** for detecting circular reasoning bias in AI algorithm evaluation. Unlike traditional bias detection tools that focus on model outputs (e.g., fairness metrics), Sleuth audits the **evaluation process itself**—detecting when the rules of the game are changed mid-evaluation to favor certain algorithms.

**Live Demo**: https://hongping-zh.github.io/circular-bias-detection/

---

## ✨ Key Features in v1.0

### 🔍 Statistical Rigor
- **Three Novel Indicators**: PSI, CCS, ρ_PC with complete mathematical foundations
- **Bootstrap Confidence Intervals**: 1000 resamples with 95% CI and p-values
- **Circular Bias Score (CBS)**: Composite metric with risk stratification
- **Adaptive Thresholds**: Strict/Standard/Lenient modes for different contexts

### 🎓 User-Friendly
- **Interactive Tutorial**: 7-step guided tour for first-time users
- **Progress Bar**: Real-time analysis feedback with 6 stages
- **Enhanced Error Messages**: Specific row/column identification (e.g., "Row 5: 'performance' must be a number")
- **Example Datasets**: Pre-loaded CV and LLM evaluation data

### 📊 Beautiful Visualizations
- **PSI Time Series**: Parameter stability over time
- **ρ_PC Scatter Plot**: Performance vs. constraints correlation
- **Indicator Comparison**: All three metrics with threshold overlays
- **Interactive Charts**: Hover tooltips, smooth animations

### 🔒 Privacy-First
- **100% Client-Side**: No data uploaded to servers
- **No Signup Required**: Start using immediately
- **Open Source**: Full transparency in implementation

### 📖 Comprehensive Documentation
- **Mathematical Formulas**: Complete CBS, PSI, CCS, ρ_PC definitions
- **Data Preparation Guide**: Required formats, quality checklist, examples
- **Parameter Guidelines**: Threshold recommendations for different scenarios
- **Common Issues**: Specific solutions for typical problems

---

## 💻 Quick Start

### Try Online (30 Seconds)

1. Visit: https://hongping-zh.github.io/circular-bias-detection/
2. Click "📊 Try Example from Zenodo"
3. Click "🔍 Scan for Bias"
4. View results with interactive charts!

### Upload Your Data

**Required CSV columns:**
- `time_period`: Sequential evaluation period (1, 2, 3...)
- `algorithm`: Algorithm name
- `performance`: Normalized score [0, 1]
- At least one constraint column (e.g., `constraint_compute`)

**Example:**
```csv
time_period,algorithm,performance,constraint_compute,constraint_memory
1,ResNet,0.72,300,8.0
1,VGG,0.68,450,12.0
2,ResNet,0.74,305,8.2
2,VGG,0.70,455,12.1
```

See full [Data Preparation Guide](web-app/USER_GUIDE_EN.md#data-preparation)

---

## 🎯 Use Cases

### Academic Researchers
- Validate evaluation protocols before paper submission
- Ensure reproducibility and statistical rigor
- Avoid p-hacking and HARKing (Hypothesizing After Results are Known)

### Journal Reviewers & Conference Organizers
- Audit submitted algorithm comparison papers
- Check benchmark competition fairness
- Detect data leakage and overfitting to test sets

### ML Engineers & Data Scientists
- Verify internal A/B testing integrity
- Detect evaluation manipulation in team KPIs
- Ensure model selection is unbiased

### AI Product Managers
- Assess vendor claims during model procurement
- Validate third-party benchmarks
- Due diligence for AI supplier selection

---

## 📊 What Makes Sleuth Different?

| Feature | Traditional Bias Tools | Sleuth |
|---------|------------------------|--------|
| **Focus** | Model outputs (predictions) | Evaluation process integrity |
| **Detects** | Demographic bias, fairness violations | Protocol manipulation, circular reasoning |
| **Target** | Deployed models | Algorithm comparison studies |
| **Method** | Group fairness metrics | Temporal consistency analysis |
| **Users** | ML practitioners deploying models | Researchers, reviewers, auditors |

**Complementary, not competitive**: Use traditional bias tools for deployed models, use Sleuth for evaluation protocol auditing.

---

## 🔢 Technical Details

### Circular Bias Score (CBS)

```
CBS = w₁ · ψ(PSI) + w₂ · ψ(CCS) + w₃ · ψ(ρ_PC)
```

Where:
- **PSI**: Performance-Structure Independence (parameter drift detection)
- **CCS**: Constraint-Consistency Score (specification stability)
- **ρ_PC**: Performance-Constraint Correlation (dependency quantification)

**Risk Stratification:**
- CBS < 0.3: **Low Risk** - Evaluation likely sound
- 0.3 ≤ CBS < 0.6: **Medium Risk** - Review methodology
- CBS ≥ 0.6: **High Risk** - Strong evidence of circular bias

See full [Mathematical Documentation](web-app/USER_GUIDE_EN.md#circular-bias-score-mathematical-definition)

---

## 📈 Statistics

### Project Scale
- **Total Code**: ~2,114 lines across 20+ files
- **React Components**: 11
- **Utility Modules**: 4
- **Documentation**: 733+ lines

### Development Timeline
- **Concept**: Q3 2025
- **Development**: Q4 2025
- **Beta Testing**: October 2025
- **Public Release**: October 15, 2025

---

## 🌟 What's Next?

### Coming in v1.1 (MVP Phase 2)

- **Baseline Comparison**: Compare against reference periods or algorithms
- **Group Analysis**: Detect bias differences across user groups
- **Enhanced Visualizations**: Heatmaps, stacked area charts, filter bubble indicators
- **Real Python Backend**: Replace mock detection with actual computation

See full [Roadmap](CHANGELOG.md#unreleased---future-features)

### Long-Term Vision (v2.0)

- **Industrial Features**: ROI calculator, TCO estimation, deployment risk scoring
- **Platform Integrations**: WandB, MLflow, Kubeflow, GitHub Actions
- **Enterprise Edition**: SSO, custom branding, compliance templates

---

## 📚 Resources

### Documentation
- **[User Guide](web-app/USER_GUIDE_EN.md)**: Complete guide with formulas and examples
- **[Data Preparation](web-app/USER_GUIDE_EN.md#data-preparation)**: Format requirements and quality checklist
- **[CHANGELOG](CHANGELOG.md)**: Detailed version history
- **[FAQ](web-app/USER_GUIDE_EN.md#faqs)**: Common questions

### Sample Data
- **Computer Vision**: `data/sample_data.csv`
- **LLM Evaluation**: `data/llm_eval_sample.csv`
- **Synthetic Generator**: Built-in tool

### Links
- **Live Demo**: https://hongping-zh.github.io/circular-bias-detection/
- **GitHub Repository**: https://github.com/hongping-zh/circular-bias-detection
- **Zenodo Dataset**: https://doi.org/10.5281/zenodo.17201032
- **Issue Tracker**: https://github.com/hongping-zh/circular-bias-detection/issues

---

## 👥 Target Audience

| User Type | Use Case | Benefit |
|-----------|----------|---------|
| **Academic Researchers** | Pre-publication validation | Ensure methodological rigor |
| **Journal Reviewers** | Paper auditing | Detect evaluation flaws |
| **ML Engineers** | A/B test verification | Prevent manipulation |
| **Product Managers** | Vendor assessment | Validate claims |
| **Compliance Officers** | Audit reporting | Generate compliance docs |

---

## 🤝 Contributing

We welcome contributions from the community!

**How to contribute:**
1. Report bugs via [GitHub Issues](https://github.com/hongping-zh/circular-bias-detection/issues)
2. Suggest features via [Discussions](https://github.com/hongping-zh/circular-bias-detection/discussions)
3. Submit pull requests (CONTRIBUTING.md coming soon)
4. Share your use cases and feedback

---

## 📄 License

This project is licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

You are free to:
- **Share**: Copy and redistribute the material
- **Adapt**: Remix, transform, and build upon the material

Under the following terms:
- **Attribution**: You must give appropriate credit

See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

### Technology
- **React**: UI framework
- **Vite**: Build tool
- **Chart.js**: Visualization library
- **Pyodide**: Python-in-browser (future)

### Inspiration
- Research integrity community
- MLOps best practices
- Statistical testing literature

### Community
- Early beta testers
- Academic reviewers
- Open source contributors

---

## 📧 Contact

- **Issues**: https://github.com/hongping-zh/circular-bias-detection/issues
- **Discussions**: https://github.com/hongping-zh/circular-bias-detection/discussions
- **Email**: yujjam@uest.edu.gr

---

## 🎉 Try It Now!

**Don't wait! Detect bias in 30 seconds:**

👉 **[Launch Sleuth](https://hongping-zh.github.io/circular-bias-detection/)** 👈

---

**Thank you for your interest in research integrity!**

*Sleuth Team*  
*October 15, 2025*
