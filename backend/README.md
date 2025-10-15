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
│   ├── ccs_calculator.py   # ✅ Day 2: CCS implementation
│   ├── rho_pc_calculator.py # ✅ Day 2: ρ_PC implementation
│   ├── bootstrap.py        # 🔜 Day 3: Bootstrap CI
│   └── bias_scorer.py      # 🔜 Day 3: CBS composite score
├── utils/                  # Utilities
│   ├── data_parser.py      # 🔜 CSV parsing
│   └── validator.py        # 🔜 Data validation
├── tests/                  # Unit tests
│   ├── test_psi.py         # ✅ Day 1: PSI tests
│   ├── test_ccs.py         # ✅ Day 2: CCS tests
│   └── test_rho_pc.py      # ✅ Day 2: ρ_PC tests
├── data/                   # Sample data
│   └── sample_data.csv     # ✅ Day 1: Example dataset
├── app.py                  # 🔜 Day 3: Flask API
├── requirements.txt        # ✅ Dependencies
├── run_psi_test.py         # ✅ Day 1: Quick test
└── run_day2_test.py        # ✅ Day 2: Comprehensive test
```

## Day 1 Progress ✅

- [x] Directory structure created
- [x] PSI calculator implemented
- [x] Sample data created
- [x] Unit tests written
- [x] Quick test script ready

## Day 2 Progress ✅

- [x] CCS calculator implemented
- [x] ρ_PC calculator implemented
- [x] CCS unit tests written
- [x] ρ_PC unit tests written
- [x] Mathematical correctness verified
- [x] Comprehensive test script

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

### CCS (Constraint-Consistency Score)

**Formula:**
```
CCS = 1 - (1/p) Σⱼ₌₁ᵖ CV(cⱼ)
where CV(cⱼ) = σⱼ / μⱼ
```

**Interpretation:**
- CCS ≥ 0.90: Highly consistent (low risk)
- 0.85 ≤ CCS < 0.90: Moderately consistent
- CCS < 0.85: Inconsistent (high risk)

**Usage:**
```python
from core.ccs_calculator import compute_ccs

result = compute_ccs(df)

print(f"CCS Score: {result['ccs_score']:.4f}")
print(f"CV by Constraint: {result['cv_by_constraint']}")
```

### ρ_PC (Performance-Constraint Correlation)

**Formula:**
```
ρ_PC = Pearson(P, C̄)
```

**Interpretation:**
- |ρ_PC| < 0.3: Weak correlation (low risk)
- 0.3 ≤ |ρ_PC| < 0.5: Moderate correlation
- |ρ_PC| ≥ 0.5: Strong correlation (high risk)

**Usage:**
```python
from core.rho_pc_calculator import compute_rho_pc

result = compute_rho_pc(df)

print(f"ρ_PC Score: {result['rho_pc']:.4f}")
print(f"P-value: {result['p_value']:.4f}")
print(f"Significant: {result['significant']}")
```

## Testing

### Quick Test (No pytest required)
```bash
python run_psi_test.py
```

### Day 2 Comprehensive Test
```bash
python run_day2_test.py
```

### Full Unit Tests
```bash
# Test all algorithms
pytest tests/ -v

# Test individually
pytest tests/test_psi.py -v
pytest tests/test_ccs.py -v
pytest tests/test_rho_pc.py -v
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
