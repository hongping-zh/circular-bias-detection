# Circular Bias Scanner - Web App

🔍 Single-page web application for detecting circular reasoning bias in algorithm evaluation.

## Features

- **Upload CSV** - Analyze your own evaluation data
- **Example Data** - Try with sample data from Zenodo
- **Synthetic Data** - Generate test scenarios
- **Instant Analysis** - Results in under 1 minute
- **Privacy-First** - All computation in your browser (no server uploads)
- **Open Source** - Free and transparent

## Tech Stack

- **React** - UI framework
- **PyOdide** - Python in the browser
- **NumPy, Pandas, SciPy** - Scientific computing
- **GitHub Pages** - Free hosting

## Quick Start

### Development

```bash
# Install dependencies
npm install

# Start development server
npm start

# Open http://localhost:3000
```

### Build

```bash
# Create production build
npm run build

# Deploy to GitHub Pages
npm run deploy
```

## How It Works

1. **Load Data** - Upload CSV, use example, or generate synthetic data
2. **Scan** - Click the scan button to run detection
3. **Results** - View PSI, CCS, and ρ_PC indicators
4. **Download** - Export results as JSON

## Data Format

CSV file should contain:
- `time_period` - Evaluation period (integer)
- `algorithm` - Algorithm name (string)
- `performance` - Performance metric 0-1 (float)
- `constraint_compute` - Computational constraint (float)
- `constraint_memory` - Memory constraint GB (float)
- `constraint_dataset_size` - Dataset size (integer)
- `evaluation_protocol` - Protocol version (string)

## Links

- **Framework**: https://github.com/hongping-zh/circular-bias-detection
- **Dataset**: https://doi.org/10.5281/zenodo.17201032
- **Paper**: [Submitted to JASA]

## License

CC-BY-4.0

## Citation

```bibtex
@software{zhang2024biasscanner,
  author = {Zhang, Hongping},
  title = {Circular Bias Scanner: Web Tool for Evaluation Bias Detection},
  year = {2024},
  url = {https://github.com/hongping-zh/circular-bias-detection}
}
```
