# GitHub Upload Guide for Simulation Code

## Overview

This guide helps you upload the supplementary simulation experiment code to your GitHub repository to support the paper's open science claims.

## Prerequisites

- GitHub account: zhanghongping1982
- Repository: circular-bias-detection (already exists)
- Git installed on your system

## Files to Upload

The following files should be uploaded to `simulations/` directory in your repository:

```
circular-bias-detection/
└── simulations/
    ├── README.md                           # Main documentation
    ├── requirements.txt                     # Python dependencies
    ├── iterative_learning_simulation.py    # Main simulation script
    └── GITHUB_UPLOAD_GUIDE.md              # This file
```

## Upload Steps

### Method 1: GitHub Web Interface (Easiest)

1. **Navigate to Repository**
   - Go to: https://github.com/zhanghongping1982/circular-bias-detection
   - Click on "Add file" → "Upload files"

2. **Upload Files**
   - Drag and drop all 4 files from `C:\Users\14593\CascadeProjects\circular-bias-detection\simulations\`
   - Or click "choose your files" and select them

3. **Commit Changes**
   - Scroll down to "Commit changes" section
   - Commit message: `Add supplementary simulation experiment (Section 3.2.1)`
   - Extended description:
     ```
     - Implement Iterated Learning framework based on Ren et al. (2024)
     - Quantify circular bias amplification across 5 generations
     - Results: 10% initial bias → 48.7% (4.87× amplification)
     - Supports NMI paper submission with original empirical contribution
     ```
   - Click "Commit changes"

### Method 2: Git Command Line (For Advanced Users)

```bash
# Navigate to project directory
cd C:\Users\14593\CascadeProjects\circular-bias-detection

# Initialize git (if not already done)
git init
git remote add origin https://github.com/zhanghongping1982/circular-bias-detection.git

# Add simulation files
git add simulations/

# Commit
git commit -m "Add supplementary simulation experiment (Section 3.2.1)

- Implement Iterated Learning framework based on Ren et al. (2024)
- Quantify circular bias amplification across 5 generations
- Results: 10% initial bias → 48.7% (4.87× amplification)
- Supports NMI paper submission with original empirical contribution"

# Push to GitHub
git push -u origin main
```

## Verification

After upload, verify that:

1. All 4 files appear at: https://github.com/zhanghongping1982/circular-bias-detection/tree/main/simulations
2. README.md displays correctly (GitHub auto-renders Markdown)
3. Code is viewable online
4. URL matches the citation in paper: 
   - LaTeX: `\url{https://github.com/zhanghongping1982/circular-bias-detection/tree/main/simulations}`
   - BibTeX entry: `\bibitem{zhang2025sim}`

## Running the Simulation (For Reviewers)

After upload, reviewers can reproduce results:

```bash
# Clone repository
git clone https://github.com/zhanghongping1982/circular-bias-detection.git
cd circular-bias-detection/simulations

# Install dependencies
pip install -r requirements.txt

# Run simulation
python iterative_learning_simulation.py
```

Expected output:
- Console log showing 5 generations with metrics
- `simulation_results/figure5_simulation_results.png` (4-panel visualization)
- `simulation_results/metrics.json` (raw data)

## License

Ensure repository has MIT License (or compatible open-source license) to allow:
- Free use and modification
- Citation in academic papers
- Integration into other projects

## Contact for Issues

If upload problems occur:
- Email: zhanghongping1982@gmail.com
- GitHub Issues: https://github.com/zhanghongping1982/circular-bias-detection/issues

## Timeline

**Recommended**: Upload before paper submission to NMI
- Allows citation of live GitHub URL in bibliography
- Demonstrates reproducibility commitment
- Enhances open science credentials (boosts review scores)

## Post-Upload: Paper Integration

After successful upload, verify LaTeX paper includes:

1. **Abstract** (Line ~189): Mentions "simulation experiment" and "open-sourced on GitHub"
2. **Section 1.4 Contributions** (Line ~233): Lists simulation as primary contribution
3. **Section 3.2.1** (Line ~357): Full methodology and results
4. **Figure 5** (Line ~391): Caption references simulation parameters
5. **Bibliography** (Line ~992): `\bibitem{zhang2025sim}` with correct URL

All these elements are already added! Just need to:
- Upload code to GitHub
- Compile LaTeX to verify all references resolve
- Upload figure5_simulation_results.png to Overleaf project root

---

**Status**: Ready for upload! 🚀
