---
title: 'Sleuth: A Browser-Based Tool for Detecting Circular Bias in AI Evaluation'
tags:
  - Python
  - JavaScript
  - artificial intelligence
  - machine learning
  - evaluation
  - reproducibility
  - bias detection
  - benchmark integrity
authors:
  - name: Hongping Zhang
    orcid: 0009-0000-2529-4613
    affiliation: 1
affiliations:
 - name: Independent Researcher
   index: 1
date: 16 October 2025
bibliography: paper.bib
---

# Summary

Evaluation integrity in artificial intelligence (AI) systems faces a critical challenge when assessment protocols undergo iterative modifications influenced by observed outcomes. This phenomenon, known as *circular bias*, generates self-reinforcing patterns that artificially enhance reported metrics while undermining reproducibility. `Sleuth` is an open-source, browser-based tool that provides the first statistical framework specifically designed to detect circular bias in AI evaluation workflows through quantitative analysis of experimental logs.

The tool implements three complementary diagnostic indicators: **PSI** (Performance-Structure Independence) quantifies parameter consistency using L2 distance metrics, **CCS** (Constraint-Consistency Score) assesses resource allocation stability via coefficient of variation, and **ρ_PC** (Performance-Constraint Correlation) detects systematic performance-resource coupling through correlation analysis. These indicators combine into a unified **Circular Bias Score (CBS)** ranging from 0 (no bias) to 1 (severe bias), complemented by bootstrap uncertainty estimation providing 95% confidence intervals and p-values for hypothesis testing.

Operating entirely in the browser through Pyodide for client-side Python execution, Sleuth preserves data confidentiality while generating interactive visualizations including CBS gauge charts, multi-dimensional radar plots, and temporal trend analyses. Empirical validation demonstrates 94% detection accuracy on controlled synthetic datasets and successfully identifies circular patterns in published ImageNet benchmark scenarios.

# Statement of Need

Contemporary AI research workflows commonly employ adaptive evaluation strategies where experimental parameters undergo refinement based on interim performance observations [@recht2019imagenet; @bouthillier2021accounting]. While methodologically legitimate when transparently documented, circular bias emerges when modifications remain undisclosed or retrospectively applied, producing inflated capability claims and diminished reproducibility [@kapoor2023leakage; @dwork2015reusable]. This problem pervades competitive leaderboard environments, proprietary development pipelines, and benchmark curation practices [@blodgett2020language; @dehghani2021benchmark].

Existing experiment management platforms (MLflow [@zaharia2018mlflow], Weights & Biases [@biewald2020wandb]) provide metadata logging but lack integrated diagnostics for circular evaluation patterns. Reproducibility frameworks rely on author self-attestation without automated validation [@pineau2021improving], while algorithmic fairness tools (AIF360 [@bellamy2019aif360], Fairlearn [@bird2020fairlearn]) address model output biases but not evaluation procedure integrity.

**Sleuth fills this gap** by transforming circular bias detection into a quantifiable statistical inference problem. Its target audience includes:

- **Academic researchers** validating their own evaluation protocols before publication
- **Peer reviewers and editors** assessing methodological rigor in submitted manuscripts  
- **Benchmark organizers** auditing leaderboard competitions for integrity violations
- **Research integrity officers** investigating reproducibility concerns
- **ML practitioners** implementing quality assurance in production pipelines

The tool's browser-based architecture eliminates installation barriers and data transmission risks, making statistical diagnostics accessible to researchers without specialized computational infrastructure or statistical expertise. By providing formal hypothesis testing alongside intuitive visualizations, Sleuth enables evidence-based assessment of evaluation integrity across diverse AI application domains.

# Key Features

- **Privacy-preserving architecture**: Client-side execution ensures sensitive evaluation data never leaves the user's browser
- **Statistical rigor**: Bootstrap resampling (1,000 replications) provides formal uncertainty quantification with confidence intervals and p-values
- **Interactive visualization**: Real-time CBS gauges, radar plots, and time-series charts facilitate pattern interpretation
- **Minimal data requirements**: Accepts simple CSV logs with timestamps, performance metrics, and experimental parameters
- **Cross-domain applicability**: Domain-agnostic design supports computer vision, NLP, robotics, and other AI subfields
- **Comprehensive documentation**: Tutorial examples, API reference, and reproducible validation experiments

# Implementation

Sleuth's frontend combines React for UI components with Chart.js for visualization rendering. The statistical engine executes via Pyodide, enabling NumPy and SciPy operations directly in WebAssembly without server dependencies. Indicator calculations follow established statistical methodologies: PSI employs L2 norm across normalized parameter vectors, CCS computes coefficient of variation for resource allocations, and ρ_PC calculates Pearson correlation between performance and constraint metrics. Bootstrap resampling implements stratified sampling to maintain temporal structure while estimating indicator distributions for hypothesis testing [@efron1994bootstrap].

The codebase provides both browser and command-line interfaces, with Python unit tests achieving >90% coverage and end-to-end validation against synthetic ground-truth datasets. Complete source code, documentation, and reproducibility materials are permanently archived at Zenodo (DOI: 10.5281/zenodo.17201032) under Creative Commons Attribution 4.0 International license.

# Acknowledgements

This work was conducted independently without institutional or financial support.

# References
