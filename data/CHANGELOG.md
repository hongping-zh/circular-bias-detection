# Changelog - Algorithm Benchmark Suite

All notable changes to the Algorithm Benchmark Suite dataset will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-10-13

### Added
- **9 new scenario files** with controlled experimental conditions:
  - `scenario_no_bias_low_noise.csv` - Baseline with minimal noise
  - `scenario_no_bias_high_noise.csv` - High measurement noise scenario
  - `scenario_mild_bias.csv` - Bias intensity 0.3
  - `scenario_moderate_bias.csv` - Bias intensity 0.6
  - `scenario_high_bias.csv` - Bias intensity 0.9
  - `scenario_few_periods.csv` - Limited temporal data (8 periods)
  - `scenario_many_algorithms.csv` - Extended algorithm set (6 algorithms)
  - `scenario_mixed_conditions.csv` - Complex multi-variate scenario
  - `scenario_edge_case.csv` - Edge case testing scenario

- **JSON Schema validation** (`schema.json`)
  - Formal data structure specification
  - Field type and constraint definitions
  - Validation examples

- **Comprehensive data dictionary** (`DATA_DICTIONARY.md`)
  - Detailed field specifications with examples
  - Value ranges and units
  - Usage guidelines and best practices
  - Data quality indicators

- **Data generation script** (`generate_benchmark_data.py`)
  - Fully reproducible data generation
  - Configurable bias and noise parameters
  - Command-line interface with validation
  - Fixed random seeds for reproducibility

- **Enhanced documentation**
  - Updated README with file inventory
  - Schema validation examples
  - Reproduction instructions
  - GitHub repository links

### Changed
- Expanded total dataset from 20 to 500+ records
- Improved Zenodo metadata with keywords and detailed description
- Standardized versioning to 2.0.0 across all artifacts

### Fixed
- Version inconsistency between dataset title and Zenodo metadata
- Missing author ORCID display on Zenodo page
- Lack of machine-readable schema

## [1.0.0] - 2024-09-25

### Added
- Initial release of Algorithm Benchmark Suite
- `algorithm_benchmark_suite.csv` with 20 evaluation records
- 4 algorithms (ResNet, VGG, DenseNet, EfficientNet)
- 5 time periods representing evaluation evolution
- 7 fields: time_period, algorithm, performance, constraint_compute, constraint_memory, constraint_dataset_size, evaluation_protocol

- Basic README with:
  - Field descriptions
  - Usage examples
  - Zenodo DOI link

### Metadata
- Published on Zenodo with DOI: 10.5281/zenodo.17196639
- License: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Author: Hongping Zhang (ORCID: 0009-0000-2529-4613)

---

## Version Comparison

| Version | Files | Records | Features |
|---------|-------|---------|----------|
| 1.0.0 | 1 CSV | 20 | Basic benchmark |
| 2.0.0 | 10 CSV | 500+ | Multiple scenarios, schema, generation script |

---

## Planned for Future Versions

### [2.1.0] - Planned
- [ ] Real-world case study data (anonymized)
- [ ] Additional domain-specific scenarios (NLP, recommender systems)
- [ ] Extended temporal ranges (30+ periods)
- [ ] Multi-objective performance metrics

### [3.0.0] - Planned
- [ ] Integration with automated validation pipeline
- [ ] Interactive data explorer web interface
- [ ] Community-contributed scenarios
- [ ] Extended metadata (publication links, benchmark leaderboards)

---

## How to Report Issues

If you find data quality issues or have suggestions:

1. **GitHub Issues**: https://github.com/hongping-zh/circular-bias-detection/issues
2. **Email**: yujjam@uest.edu.gr
3. **Zenodo Comments**: https://zenodo.org/records/17196639

Please include:
- Dataset version
- File name
- Row number (if applicable)
- Description of the issue
- Expected vs. actual values

---

## Citation

When citing specific versions:

**Version 2.0.0:**
```bibtex
@dataset{zhang2024_benchmark_v2,
  author = {Zhang, Hongping},
  title = {Algorithm Benchmark Suite v2.0},
  year = {2024},
  publisher = {Zenodo},
  version = {2.0.0},
  doi = {10.5281/zenodo.17196639}
}
```

**Version 1.0.0:**
```bibtex
@dataset{zhang2024_benchmark_v1,
  author = {Zhang, Hongping},
  title = {Algorithm Benchmark Suite v1.0},
  year = {2024},
  publisher = {Zenodo},
  version = {1.0.0},
  doi = {10.5281/zenodo.17196639}
}
```

---

## Links

- **Zenodo Repository**: https://doi.org/10.5281/zenodo.17196639
- **GitHub Repository**: https://github.com/hongping-zh/circular-bias-detection
- **Software Framework**: See main repository README
- **License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
