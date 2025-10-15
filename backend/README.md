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
│   ├── bootstrap.py        # ✅ Day 3: Bootstrap CI
│   └── bias_scorer.py      # ✅ Day 3: CBS composite score
├── tests/                  # Unit tests
│   ├── test_psi.py         # ✅ Day 1: PSI tests
│   ├── test_ccs.py         # ✅ Day 2: CCS tests
│   └── test_rho_pc.py      # ✅ Day 2: ρ_PC tests
├── data/                   # Sample data
│   └── sample_data.csv     # ✅ Example dataset
├── app.py                  # ✅ Day 3: Flask REST API
├── requirements.txt        # ✅ Dependencies
├── run_psi_test.py         # ✅ Day 1: PSI test
├── run_day2_test.py        # ✅ Day 2: CCS + ρ_PC test
└── run_day3_test.py        # ✅ Day 3: Full integration test
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

## Day 3 Progress ✅

- [x] Bootstrap confidence intervals (1000 iterations)
- [x] CBS composite bias score
- [x] Flask REST API
- [x] Integration tests
- [x] API documentation
- [x] Complete pipeline working

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

### CBS (Circular Bias Score) - Composite

**Formula:**
```
CBS = w₁·ψ(PSI) + w₂·ψ(CCS) + w₃·ψ(ρ_PC)
```

**Risk Levels:**
- CBS < 0.3: Low Risk
- 0.3 ≤ CBS < 0.6: Medium Risk
- CBS ≥ 0.6: High Risk

**Usage:**
```python
from core.bias_scorer import detect_circular_bias

# Complete detection pipeline
results = detect_circular_bias(df, run_bootstrap=True, n_bootstrap=1000)

print(f"CBS Score: {results['cbs_score']:.3f}")
print(f"Risk Level: {results['risk_level']}")
print(f"Bias Detected: {results['bias_detected']}")
print(f"Confidence: {results['confidence']:.1f}%")

# With bootstrap CI
if 'bootstrap' in results:
    print(f"PSI CI: [{results['bootstrap']['psi']['ci_lower']:.3f}, {results['bootstrap']['psi']['ci_upper']:.3f}]")
```

### Bootstrap Confidence Intervals

**Usage:**
```python
from core.bootstrap import bootstrap_indicators

bootstrap_results = bootstrap_indicators(df, n_iterations=1000, confidence=0.95)

print(f"PSI Mean: {bootstrap_results['psi']['mean']:.4f}")
print(f"PSI 95% CI: [{bootstrap_results['psi']['ci_lower']:.4f}, {bootstrap_results['psi']['ci_upper']:.4f}]")
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

### Day 3 Integration Test
```bash
python run_day3_test.py
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

### Flask API Server
```bash
# Start API server
python app.py

# Server will run on http://localhost:5000
# Endpoints:
#   GET  /health       - Health check
#   GET  /api/info     - API documentation
#   POST /api/detect   - Bias detection
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
