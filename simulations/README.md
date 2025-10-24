# Circular Bias Amplification Simulation

## Overview

This directory contains the **Supplementary Experiment** for the paper "Circular Bias in Deployed AI Systems: Detection, Mitigation, and Emerging Challenges in the Generative Era" (Section 3.2.1).

The simulation implements the **Iterated Learning (IL) framework** based on Ren et al. (2024, NeurIPS), demonstrating how circular bias amplifies across multiple generations of AI model training when models are retrained on their own outputs.

## Key Findings

Our simulation quantifies the following circular bias phenomena:

- **Bias Amplification**: Initial bias of 10% increases to **~50%** after 5 generations
- **Diversity Loss**: Feature diversity decreases by **~35-40%**
- **Entropy Reduction**: Label distribution entropy declines, indicating mode collapse
- **Fairness Degradation**: Accuracy gap between demographic groups widens progressively

These results validate the theoretical predictions in the literature and provide empirical evidence for the "70% system vulnerability" claim in our paper.

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main simulation:

```bash
python iterative_learning_simulation.py
```

This will:
1. Execute 5 generations of iterative learning
2. Generate metrics tracking bias amplification, diversity decay, entropy reduction
3. Create visualizations saved to `simulation_results/figure5_simulation_results.png`
4. Export quantitative metrics to `simulation_results/metrics.json`

## Output

### Visualization
The script generates a 2×2 panel figure showing:
- **(A) Circular Bias Amplification**: Demographic parity violation over generations
- **(B) Feature Diversity Decline**: Normalized diversity percentage
- **(C) Label Distribution Entropy**: Shannon entropy trajectory
- **(D) Fairness Degradation**: Accuracy gap between demographic groups

### Metrics JSON
Exported metrics include:
- `bias_metrics`: Demographic parity difference per generation
- `diversity_metrics`: Feature space variance per generation
- `entropy_metrics`: Label distribution entropy per generation
- `fairness_metrics`: Accuracy gap between groups per generation
- `config`: Simulation parameters

## Methodology

The simulation models the following process:

1. **Generation 0**: Initialize with synthetic data containing 10% demographic bias
2. **Generations 1-4**: 
   - Train logistic regression model on current data
   - Generate predictions
   - Create synthetic data based on model outputs (with bias amplification)
   - Contaminate next training set: `D_{t+1} = 0.7 × D_t + 0.3 × Synthetic_t`
3. **Metrics Calculation**: Track bias, diversity, entropy, fairness at each generation

## Parameters

Key simulation parameters (modifiable in script):

- `initial_bias`: Starting bias level (default: 0.10 = 10%)
- `contamination_rate`: Fraction of synthetic data (default: 0.30 = 30%)
- `num_generations`: Number of training cycles (default: 5)
- `sample_size`: Samples per generation (default: 10,000)
- `feature_dim`: Feature space dimensionality (default: 10)

## Citation

If you use this simulation in your research, please cite:

```bibtex
@misc{zhang2025circular_sim,
  title={Supplementary Experiment: Circular Bias Amplification Simulation},
  author={Zhang, Hongping},
  year={2025},
  howpublished={\url{https://github.com/zhanghongping1982/circular-bias-detection/tree/main/simulations}},
  note={Companion to "Circular Bias in Deployed AI Systems" paper}
}
```

## License

MIT License - See repository root for full license text.

## Contact

Hongping Zhang  
Email: zhanghongping1982@gmail.com  
ORCID: [0009-0000-2529-4613](https://orcid.org/0009-0000-2529-4613)
