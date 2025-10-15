# Changelog

All notable changes to Sleuth - AI Evaluation Bias Hunter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-10-15

### 🎉 Initial Public Release

First stable release of Sleuth, a comprehensive web-based tool for detecting circular reasoning bias in AI algorithm evaluation.

### ✨ Core Features

#### Bias Detection
- **Three Statistical Indicators**: PSI, CCS, ρ_PC with comprehensive mathematical foundations
- **Bootstrap Confidence Intervals**: 1000 resamples with 95% CI
- **P-value Testing**: Statistical significance for all indicators
- **Circular Bias Score (CBS)**: Composite metric with risk stratification (Low/Medium/High)
- **Adaptive Thresholds**: Strict/Standard/Lenient modes for different evaluation contexts

#### User Interface
- **Interactive Tutorial**: 7-step guided onboarding for first-time users
- **Progress Bar**: Real-time feedback with 6 analysis stages
- **Help System**: In-app "❓ Help" button for tutorial access anytime
- **Responsive Design**: Mobile-friendly interface

#### Data Handling
- **Enhanced Validation**: Detailed error messages with specific row/column identification
- **CSV Upload**: Drag-and-drop or click to browse
- **Example Datasets**: Pre-loaded Computer Vision and LLM evaluation examples
- **Synthetic Data Generator**: Built-in random data generation for testing
- **Data Requirements Checking**: Minimum 2 algorithms, 3 time periods, 1 constraint column

#### Visualizations
- **PSI Time Series Chart**: Line chart showing parameter stability over time with threshold overlay
- **ρ_PC Scatter Plot**: Performance vs. Constraints correlation visualization
- **Indicator Comparison**: Bar chart comparing all three indicators against thresholds
- **Interactive Charts**: Hover tooltips, smooth animations, responsive layout
- **Bootstrap Indicators**: Visual display of confidence intervals and statistical significance

#### Documentation
- **Mathematical Definitions**: Complete formulas for CBS, PSI, CCS, ρ_PC with statistical interpretations
- **Data Preparation Guide**: Required format, optional columns, LLM-specific fields, quality checklist
- **Parameter Guidelines**: Threshold recommendations with strict/standard/lenient ranges
- **Common Issues & Solutions**: Specific error resolutions and sparse data handling
- **Example CSV Formats**: Ready-to-use templates for different domains

#### Performance & Architecture
- **Web Worker Ready**: Infrastructure for background computation (mock mode in v1.0)
- **Client-Side Processing**: 100% browser-based, no data uploaded to servers
- **Privacy-First**: All data stays on user's computer
- **Fast Results**: Analysis completes in ~3.5 seconds

### 📦 Technical Stack

- **Frontend**: React 18 + Vite 7
- **Charting**: Chart.js 4.5 + react-chartjs-2 5.3
- **Language**: JavaScript ES6+
- **Styling**: CSS3 with responsive design
- **Build**: Vite with GitHub Pages deployment

### 📊 Statistics

- **Total Code**: ~2,114 lines across 20+ files
- **Components**: 11 React components
- **Utilities**: 4 utility modules
- **Documentation**: 733+ lines (USER_GUIDE_EN.md + ENHANCEMENTS.md + MVP_IMPROVEMENTS.md)

### 🎯 Use Cases

- **Academic Researchers**: Validate evaluation protocols before publication
- **Journal Reviewers**: Audit submitted algorithm comparison papers
- **Conference Organizers**: Check benchmark competition fairness
- **ML Engineers**: Verify internal A/B testing integrity
- **AI Product Managers**: Assess vendor claims during model selection

### 📖 Documentation Files

- `README.md`: Project overview and quick start
- `USER_GUIDE_EN.md`: Comprehensive user guide with mathematical foundations
- `ENHANCEMENTS.md`: Feature documentation for v1.0 enhancements
- `MVP_IMPROVEMENTS.md`: Phase 1 improvement summary
- `PERFORMANCE.md`: Performance optimization details
- `DEPLOYMENT_CHECKLIST.md`: Deployment procedures
- `AFTERNOON_TASKS.md`: Phase 2 roadmap

### 🔗 Links

- **Live Demo**: https://hongping-zh.github.io/circular-bias-detection/
- **GitHub**: https://github.com/hongping-zh/circular-bias-detection
- **Zenodo Dataset**: https://doi.org/10.5281/zenodo.17201032
- **User Guide**: [USER_GUIDE_EN.md](web-app/USER_GUIDE_EN.md)

### 🙏 Acknowledgments

- Chart.js for visualization library
- React team for the UI framework
- Pyodide for Python-in-browser capabilities (future integration)

---

## [Unreleased] - Future Features

### Planned for v1.1

#### Baseline Comparison (MVP Phase 2)
- [ ] Baseline selector with 5 modes (None, First Period, Best/Worst/Median)
- [ ] Differential analysis visualization
- [ ] Improvement percentage calculation

#### Group Analysis (MVP Phase 2)
- [ ] Algorithm grouping by performance tiers
- [ ] Subgroup bias detection
- [ ] Group comparison charts (radar, box plots)

#### Enhanced Visualizations (MVP Phase 2)
- [ ] Distribution heatmap (Algorithm × Time)
- [ ] Interest drift stacked area chart
- [ ] Filter bubble effect indicator
- [ ] Group comparison visualizations

#### Production Features
- [ ] Real Python backend integration (replace mock detection)
- [ ] Full Web Worker implementation for heavy computation
- [ ] PDF report export
- [ ] API endpoint for programmatic access

### Planned for v2.0

#### Industrial Features
- [ ] Cost-benefit analysis
- [ ] ROI calculator
- [ ] Production readiness scoring
- [ ] Deployment risk assessment
- [ ] TCO (Total Cost of Ownership) estimation

#### Platform Integrations
- [ ] Weights & Biases plugin
- [ ] MLflow integration
- [ ] Kubeflow component
- [ ] GitHub Actions workflow

#### Enterprise Features
- [ ] SSO authentication
- [ ] Custom branding
- [ ] Compliance report templates
- [ ] Multi-user collaboration
- [ ] Audit trail logging

---

## Version History

| Version | Release Date | Highlights |
|---------|--------------|------------|
| 1.0.0 | 2025-10-15 | Initial public release with core bias detection, visualizations, and tutorial |

---

## Notes

### Breaking Changes
- None (initial release)

### Known Limitations
- **Mock Detection Mode**: v1.0 uses simulated analysis for demo purposes. Real Python computation coming in v1.1
- **Browser Compatibility**: Requires modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- **Data Size**: Recommended maximum 1000 rows for optimal performance

### Bug Reports

Please report issues at: https://github.com/hongping-zh/circular-bias-detection/issues

### Contributing

We welcome contributions! See CONTRIBUTING.md (coming soon) for guidelines.

---

**Thank you for using Sleuth!** 🎉
