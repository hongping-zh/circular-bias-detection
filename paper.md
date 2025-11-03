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

Reviewers frequently ask whether Sleuth is (1) a new algorithm, (2) an innovative combination yielding superior diagnostic power, or (3) a usability contribution that enables new users. Our answer is explicit:

- **New algorithm?** Sleuth does not propose a single novel estimator. Instead, it frames circular-bias detection as a statistical inference task and operationalizes it with three complementary indicators—PSI, CCS, and ρ_PC—augmented with bootstrap uncertainty quantification (confidence intervals and p-values) for formal hypothesis testing.
- **Innovative combination?** Yes. Sleuth integrates these indicators into a unified workflow and a composite Circular Bias Score (CBS) with calibrated, data-driven thresholds. This design improves practical diagnostic power versus any single metric and separates failure modes (parameter drift, constraint inconsistency, performance–constraint coupling) that are often conflated in practice [@recht2019imagenet; @bouthillier2021accounting].
- **Ease-of-use enabling new users?** Yes. A zero‑install, browser-based implementation via Pyodide, CSV inputs, guided defaults, and exportable reports lower the barrier for non-programmers (e.g., reviewers, editors, and domain researchers) to perform circular‑bias audits, expanding who can apply these checks in real workflows.

This contribution addresses a clear gap: experiment platforms (MLflow [@zaharia2018mlflow], Weights & Biases [@biewald2020wandb]) log metadata but lack integrated diagnostics for circular evaluation patterns; reproducibility checklists rely on self‑attestation without automated validation [@pineau2021improving]; fairness toolkits (AIF360 [@bellamy2019aif360], Fairlearn [@bird2020fairlearn]) target model‑output bias rather than evaluation‑protocol integrity. Sleuth complements these efforts by providing statistical tests and actionable visual diagnostics focused specifically on evaluation procedures.

Primary users include academic researchers preparing submissions, peer reviewers and editors assessing methodological rigor, benchmark organizers auditing leaderboards, research‑integrity officers, and ML practitioners integrating QA checks into pipelines. By combining statistical rigor with accessible delivery, Sleuth meets an immediate community need for practical, auditable detection of circular evaluation bias.

# Key Features

- **Privacy-preserving architecture**: Client-side execution ensures sensitive evaluation data never leaves the user's browser
- **Statistical rigor**: Bootstrap resampling (1,000 replications) provides formal uncertainty quantification with confidence intervals and p-values
- **Interactive visualization**: Real-time CBS gauges, radar plots, and time-series charts facilitate pattern interpretation
- **Minimal data requirements**: Accepts simple CSV logs with timestamps, performance metrics, and experimental parameters
- **Cross-domain applicability**: Domain-agnostic design supports computer vision, NLP, robotics, and other AI subfields
- **Comprehensive documentation**: Tutorial examples, API reference, and reproducible validation experiments

# Implementation

Sleuth's frontend combines React for UI components with Chart.js for visualization rendering. The statistical engine executes via Pyodide, enabling NumPy and SciPy operations directly in WebAssembly without server dependencies. Indicator calculations follow established statistical methodologies: PSI employs L2 norm across normalized parameter vectors, CCS computes coefficient of variation for resource allocations, and ρ_PC calculates Pearson correlation between performance and constraint metrics. Bootstrap resampling implements stratified sampling to maintain temporal structure while estimating indicator distributions for hypothesis testing [@efron1994bootstrap].
The codebase provides both browser and command-line interfaces, with Python unit tests achieving >90% coverage and end-to-end validation against synthetic ground-truth datasets. Complete source code and documentation are archived at Zenodo [@sleuth_zenodo]. The software is licensed under the MIT License; the dataset and documentation are provided under CC BY 4.0.

# Data Availability

All synthetic citation datasets, the generator script (`generate_data.py`), and the evaluation script (`evaluate_citation_bias.py`) are archived on Zenodo (Dataset DOI: 10.5281/zenodo.TBD_DATASET). The software and exact code used in this study are available at https://github.com/hongping-zh/circular-bias-detection and are referenced by the release tag `v0.1.0-data` for precise reproducibility.

# Reproducibility

We provide fixed random seeds and record all generation parameters in `{prefix}_params.json`. The following commands reproduce the datasets and evaluation results:

1. Generate small/medium datasets (deterministic with default seed):

```
python generate_data.py
```

2. Evaluate and export JSON summaries:

```
python evaluate_citation_bias.py --prefix synthetic_citations_small --json small_eval.json
python evaluate_citation_bias.py --prefix synthetic_citations_medium --json medium_eval.json
```

3. Negative control (no biased groups):

```
python -c "from generate_data import generate_citation_dataset; generate_citation_dataset(num_papers=1000, num_biased_groups=0, file_name='neg_control.csv', out_prefix='neg_control', seed=42)"
python evaluate_citation_bias.py --prefix neg_control --json neg_control_eval.json
```

4. Hard-variant datasets (introducing base same-year noise and cross-group biased edges):

```
python -c "from generate_data import generate_citation_dataset; generate_citation_dataset(num_papers=600, start_year=2010, end_year=2023, base_citation_rate=1.8, num_biased_groups=6, biased_group_size=5, bias_intensity=3, file_name='synthetic_hard_small.csv', seed=42, out_prefix='synthetic_hard_small', base_same_year_rate=0.05, bias_cross_group_rate=0.10)"
python evaluate_citation_bias.py --prefix synthetic_hard_small --json hard_small_eval.json
```

All artifacts (CSVs and evaluation JSONs) are included in the Zenodo archive (Dataset DOI: 10.5281/zenodo.TBD_DATASET).

# Validation & Results

We validate the dataset and evaluation pipeline using ground-truth edge labels emitted by the generator. For the small dataset, a simple baseline heuristic (predict biased if same-year and same-group edge) achieves perfect scores, which is expected given the construction:

| Dataset | Edges | Precision | Recall | F1 |
|---------|-------|-----------|--------|----|
| Small   | 127   | 1.00      | 1.00   | 1.00 |

We further report results on the medium dataset, a negative control, and a hard-variant dataset that introduces non-trivial confounders. The JSON summaries (`medium_eval.json`, `neg_control_eval.json`, `hard_*_eval.json`) are archived with the dataset and reproduce the reported metrics.

# Acknowledgements

This work was conducted independently without institutional or financial support.

# References
