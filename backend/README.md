# Sleuth Backend - Circular Bias Detection

Python backend for computing PSI, CCS, and ρ_PC indicators.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Quick test (Day 1)
python run_psi_test.py

# Unit tests (Day 2)
pytest tests/test_psi.py -v
```

## Project Structure

```
backend/
├── core/                   # Core algorithms
│   ├── psi_calculator.py   # ✅ Day 1: PSI implementation
│   ├── ccs_calculator.py   # 🔜 Day 2: CCS implementation
│   ├── rho_pc_calculator.py # 🔜 Day 2: ρ_PC implementation
│   ├── bootstrap.py        # 🔜 Day 3: Bootstrap CI
│   └── bias_scorer.py      # 🔜 Day 3: CBS composite score
├── utils/                  # Utilities
│   ├── data_parser.py      # 🔜 CSV parsing
│   └── validator.py        # 🔜 Data validation
├── tests/                  # Unit tests
│   └── test_psi.py         # ✅ Day 1: PSI tests
├── data/                   # Sample data
│   └── sample_data.csv     # ✅ Day 1: Example dataset
├── app.py                  # 🔜 Day 3: Flask API
├── requirements.txt        # ✅ Dependencies
└── run_psi_test.py         # ✅ Day 1: Quick test
```

## Day 1 Progress ✅

- [x] Directory structure created
- [x] PSI calculator implemented
- [x] Sample data created
- [x] Unit tests written
- [x] Quick test script ready

## Algorithms

### PSI (Performance-Structure Independence)

**Formula:**
```
PSI = (1/T) Σᵢ₌₁ᵀ ||θᵢ - θᵢ₋₁||₂
```

**Interpretation:**
- PSI < 0.10: Stable (low risk)
- 0.10 ≤ PSI < 0.15: Moderate
- PSI ≥ 0.15: Unstable (high risk)

**Usage:**
```python
from core.psi_calculator import compute_psi
import pandas as pd

df = pd.read_csv('data/sample_data.csv')
result = compute_psi(df)

print(f"PSI Score: {result['psi_score']:.4f}")
print(f"Exceeds Threshold: {result['exceeds_threshold']}")
```

## Testing

### Quick Test (No pytest required)
```bash
python run_psi_test.py
```

### Full Unit Tests
```bash
pytest tests/test_psi.py -v
```

### Expected Output
```
PSI Score: 0.0XXX
Threshold: 0.15
Status: ✓ Below threshold

Interpretation:
PSI = 0.0XXX indicates very stable parameters (low risk). 
Parameters show excellent stability across time periods. 
Analyzed 5 time periods.
```

## Next Steps

**Day 2 (Tomorrow):**
- [ ] Implement CCS calculator
- [ ] Implement ρ_PC calculator
- [ ] Write unit tests for both
- [ ] Verify mathematical correctness

**Day 3 (After tomorrow):**
- [ ] Bootstrap confidence intervals
- [ ] CBS composite score
- [ ] Flask API
- [ ] Integration test

## Dependencies

- numpy >= 1.24.0
- pandas >= 2.0.0
- scipy >= 1.10.0
- flask >= 3.0.0
- flask-cors >= 4.0.0
- pytest >= 7.4.0

## License

CC BY 4.0
