# Proposal: Integrate Sleuth as a Standard Integrity Check for ML Evaluation Protocols

**Submitted by**: Hongping Zhang (UESTC / Independent Researcher)  
**Contact**: yujjam@uest.edu.gr  
**Project**: [Sleuth – Circular Bias Detection](https://github.com/hongping-zh/circular-bias-detection)

## Problem Statement
Current ML evaluation practices—especially in leaderboards and SOTA claims—are vulnerable to *circular reasoning bias*: iterative tuning of prompts, hyperparameters, or datasets until performance metrics improve. This inflates reported results and undermines reproducibility. Existing tools (e.g., AIF360, Fairlearn) focus on model fairness, not *evaluation protocol integrity*.

## Proposed Solution
**Sleuth** is the first open-source framework that:
- Quantifies circular bias via three statistically grounded indicators: PSI (parameter stability), CCS (constraint consistency), and ρ_PC (performance-constraint correlation).
- Supports automated checks via Python SDK, CLI, and web app.
- Generates auditable reports with actionable fixes.

## Integration with MLCommons
We propose Sleuth as a **recommended pre-submission validation tool** for:
- **MLPerf Inference/Training**: Add Sleuth check to submission pipelines to flag unstable evaluation conditions.
- **Responsible AI Guidelines**: Include Sleuth in “Evaluation Best Practices” documentation.
- **Benchmark Metadata Schema**: Extend result records with `sleuth_verified: true/false` and bias scores.

## Why Now?
- Growing concern over “benchmark overfitting” in LLM and vision research.
- Sleuth is lightweight (<500 LOC core), language-agnostic (via CSV), and already used in academic peer review.
- Zenodo DOI and JOSS submission ensure long-term archival and academic credit.

## Next Steps Requested
- Discuss inclusion in MLCommons Working Group on Evaluation Integrity.
- Pilot integration with one MLPerf benchmark (e.g., LLM Inference).
- Co-author a white paper on “Evaluation Hygiene in ML”.
