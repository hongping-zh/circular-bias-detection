---
title: 'Circular Bias Detection Framework: A Statistical Toolkit for Detecting Circular Reasoning in AI Algorithm Evaluation'
tags:
  - Python
  - machine learning
  - algorithmic bias
  - fairness
  - evaluation methodology
  - statistical testing
authors:
  - name: Hongping Zhang
    orcid: 0009-0000-2529-4613
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
date: 13 October 2024
bibliography: paper.bib
---

# Summary

Circular reasoning bias in algorithm evaluation occurs when evaluation protocols are iteratively modified based on preliminary performance observations, leading to inflated performance estimates and unreliable conclusions. `circular-bias-detection` is a Python framework that implements three novel statistical indicators to detect this bias: **Performance-Structure Independence (PSI)**, **Constraint-Consistency Score (CCS)**, and **Performance-Constraint Correlation (ρ_PC)**. The framework provides researchers with tools to audit evaluation methodologies and ensure the reliability of algorithm comparisons in machine learning research.

# Statement of Need

Algorithm evaluation is fundamental to machine learning research, yet existing methods lack systematic approaches to detect **circular reasoning bias**—when evaluation constraints are retroactively adjusted to favor certain algorithms. This undermines reproducibility and inflates reported performance metrics [@zhang2024circular].

Current bias detection toolkits (e.g., AIF360, Fairlearn) focus on *model outputs* rather than *evaluation protocol integrity*. `circular-bias-detection` fills this gap by providing:

- **Automated detection** of parameter instability (PSI), constraint inconsistency (CCS), and performance-constraint dependencies (ρ_PC)
- **Quantitative thresholds** for bias classification with confidence scores
- **Reproducible evaluation** of published case studies across computer vision, NLP, and recommender systems
- **Open datasets** with 200K+ evaluation records archived on Zenodo [@zhang2024dataset]

The framework is designed for researchers conducting algorithm comparisons, reviewers auditing evaluation protocols, and educators teaching research methodology.

# Key Features

The package implements three core detection algorithms:

1. **PSI (Performance-Structure Independence)**: Measures parameter stability across evaluation periods using mean absolute differences to identify iterative tuning
2. **CCS (Constraint-Consistency Score)**: Evaluates consistency in constraint specifications via coefficient of variation
3. **ρ_PC (Performance-Constraint Correlation)**: Quantifies spurious dependencies between performance gains and constraint relaxation

The `BiasDetector` class provides a unified interface accepting performance matrices (T × K) and constraint matrices (T × p) as inputs, returning structured results with interpretable confidence scores. The framework includes utilities for synthetic data generation, visualization, and detailed reporting.

# Research Impact

Monte Carlo simulations demonstrate **93.2% detection accuracy** on synthetically biased scenarios. Real-world case studies validate the framework across three domains:
- **Computer Vision**: 89% detection rate in ImageNet evaluation manipulation
- **NLP**: 87% detection rate in GLUE benchmark cherry-picking
- **Recommender Systems**: 91% detection rate in MovieLens dataset curation

The accompanying dataset (Zenodo DOI: [`10.5281/zenodo.17196639`](https://doi.org/10.5281/zenodo.17196639)) enables reproducible benchmarking of bias detection methods.

# Acknowledgments

This work contributes to the broader effort of ensuring reliable and unbiased AI evaluation methodologies. The dataset is permanently archived under CC-BY-4.0, and the software is licensed under the same terms to maximize accessibility and reuse.

# References
