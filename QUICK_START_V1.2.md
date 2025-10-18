# 🚀 Sleuth v1.2 Quick Start Guide

**Get the API running in 5 minutes!**

---

## ⚡ 1-Minute Setup

### Step 1: Install Dependencies (1 min)

```bash
cd C:\Users\14593\CascadeProjects\circular-bias-detection\backend
pip install -r requirements.txt
```

### Step 2: Run Server (10 seconds)

```bash
python main.py
```

**Expected Output:**
```
🚀 Sleuth API v1.2 starting...
📖 API docs: http://localhost:8000/api/docs
🔑 Demo API key: demo_free_key_12345
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 3: Test It! (30 seconds)

**Open browser:**
```
http://localhost:8000/api/docs
```

**You should see Swagger UI with interactive API documentation!** 🎉

---

## 🧪 Test the API

### Test 1: Health Check

```bash
curl http://localhost:8000/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "1.2.0",
  "timestamp": "2024-10-18T10:30:00"
}
```

---

### Test 2: Bias Detection (Full Example)

```bash
curl -X POST "http://localhost:8000/api/v1/detect" \
  -H "X-API-Key: demo_free_key_12345" \
  -H "Content-Type: application/json" \
  -d "{
    \"performance_matrix\": [[0.85, 0.78], [0.87, 0.80], [0.91, 0.84]],
    \"constraint_matrix\": [[512, 0.7], [550, 0.75], [600, 0.8]],
    \"algorithm_names\": [\"ModelA\", \"ModelB\"]
  }"
```

**Expected Response:**
```json
{
  "has_bias": true,
  "risk_level": "medium",
  "confidence": "medium",
  "recommendation": "Lock hyperparameters and re-evaluate with fixed settings",
  "details": {
    "psi": {
      "value": 0.18,
      "threshold": 0.15,
      "status": "fail",
      "meaning": "Parameters changed during evaluation"
    },
    "ccs": {
      "value": 0.82,
      "threshold": 0.85,
      "status": "fail",
      "meaning": "Constraints inconsistent"
    },
    "rho_pc": {
      "value": 0.65,
      "threshold": 0.5,
      "status": "fail",
      "meaning": "Performance depends on constraints"
    }
  },
  "timestamp": "2024-10-18T10:30:00",
  "processing_time_ms": 45.23
}
```

✅ **Success!** Your API is detecting bias!

---

### Test 3: Check Usage

```bash
curl -X GET "http://localhost:8000/api/v1/usage" \
  -H "X-API-Key: demo_free_key_12345"
```

**Expected Response:**
```json
{
  "tier": "free",
  "usage_count": 1,
  "usage_limit": 5,
  "remaining": 4,
  "reset_date": "2024-12-01"
}
```

---

## 🐍 Python Client Example

```python
import requests

# API configuration
API_URL = "http://localhost:8000/api/v1/detect"
API_KEY = "demo_free_key_12345"

# Your evaluation data
data = {
    "performance_matrix": [
        [0.85, 0.78],
        [0.87, 0.80],
        [0.91, 0.84]
    ],
    "constraint_matrix": [
        [512, 0.7],
        [550, 0.75],
        [600, 0.8]
    ],
    "algorithm_names": ["ModelA", "ModelB"]
}

# Make request
response = requests.post(
    API_URL,
    json=data,
    headers={"X-API-Key": API_KEY}
)

# Check result
result = response.json()

if result["has_bias"]:
    print(f"⚠️  BIAS DETECTED - {result['risk_level'].upper()}")
    print(f"Recommendation: {result['recommendation']}")
else:
    print("✅ No bias detected")

print(f"\nProcessing time: {result['processing_time_ms']}ms")
```

**Save as:** `test_api.py` and run:
```bash
python test_api.py
```

---

## 🌐 JavaScript Client Example

```javascript
// test_api.js
const axios = require('axios');

const API_URL = 'http://localhost:8000/api/v1/detect';
const API_KEY = 'demo_free_key_12345';

const data = {
  performance_matrix: [
    [0.85, 0.78],
    [0.87, 0.80],
    [0.91, 0.84]
  ],
  constraint_matrix: [
    [512, 0.7],
    [550, 0.75],
    [600, 0.8]
  ],
  algorithm_names: ['ModelA', 'ModelB']
};

async function detectBias() {
  try {
    const response = await axios.post(API_URL, data, {
      headers: { 'X-API-Key': API_KEY }
    });

    const result = response.data;

    if (result.has_bias) {
      console.log(`⚠️  BIAS DETECTED - ${result.risk_level.toUpperCase()}`);
      console.log(`Recommendation: ${result.recommendation}`);
    } else {
      console.log('✅ No bias detected');
    }

    console.log(`\nProcessing time: ${result.processing_time_ms}ms`);
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

detectBias();
```

**Run:**
```bash
npm install axios
node test_api.js
```

---

## 📚 Interactive API Documentation

### Swagger UI (Recommended)

**Open in browser:**
```
http://localhost:8000/api/docs
```

**Features:**
- ✅ Try API calls directly in browser
- ✅ See all endpoints and parameters
- ✅ Example request/response
- ✅ Authentication testing

### ReDoc (Alternative)

```
http://localhost:8000/api/redoc
```

---

## 🔑 Get Your Own API Key

### Generate Free API Key

```bash
curl -X POST "http://localhost:8000/api/v1/keys/generate?email=your@email.com&tier=free"
```

**Response:**
```json
{
  "api_key": "sk_free_abc123...",
  "tier": "free",
  "usage_limit": 5,
  "created_at": "2024-10-18T10:30:00"
}
```

**Save your API key!** You'll need it for all requests.

---

## 🎯 Common Use Cases

### Use Case 1: CI/CD Integration

```bash
# Add to your CI pipeline
python test_bias.py || exit 1
```

### Use Case 2: Jupyter Notebook

```python
import requests
import pandas as pd

# Load your evaluation data
df = pd.read_csv('evaluation_results.csv')

# Prepare matrices
performance = df.pivot('time', 'algorithm', 'score').values
constraints = df.groupby('time')[['gpu_hours', 'dataset_size']].first().values

# Detect bias
result = requests.post(
    "http://localhost:8000/api/v1/detect",
    json={
        "performance_matrix": performance.tolist(),
        "constraint_matrix": constraints.tolist()
    },
    headers={"X-API-Key": "your-api-key"}
).json()

# Display
print(f"Bias: {result['has_bias']}")
print(f"Risk: {result['risk_level']}")
```

### Use Case 3: Pre-Deployment Check

```bash
#!/bin/bash
# check_bias.sh

RESULT=$(curl -s -X POST "http://localhost:8000/api/v1/detect" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d @evaluation_data.json)

HAS_BIAS=$(echo $RESULT | jq -r '.has_bias')

if [ "$HAS_BIAS" = "true" ]; then
  echo "❌ Bias detected - deployment blocked"
  exit 1
else
  echo "✅ No bias - safe to deploy"
  exit 0
fi
```

---

## 🐛 Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'circular_bias_detector'`

**Solution:**
```bash
# Install the package in editable mode
cd C:\Users\14593\CascadeProjects\circular-bias-detection
pip install -e .
```

---

### Problem: `ImportError: cannot import name 'SimpleBiasDetector'`

**Solution:**
Check if `SimpleBiasDetector` exists:
```bash
python -c "from circular_bias_detector import SimpleBiasDetector; print('OK')"
```

If not, use `BiasDetector` instead:
```python
# In backend/main.py, line 137:
from circular_bias_detector import BiasDetector  # instead of SimpleBiasDetector
```

---

### Problem: Port 8000 already in use

**Solution:**
```bash
# Use different port
uvicorn main:app --port 8080
```

---

### Problem: CORS errors in browser

**Solution:**
Check `allow_origins` in `main.py`:
```python
allow_origins=[
    "https://hongping-zh.github.io",
    "http://localhost:5173",
    "http://localhost:3000",
    # Add your frontend URL here
]
```

---

## 📊 Next Steps

### ✅ Completed:
- Backend API running
- Authentication working
- Bias detection functional

### 🚧 Next Up:
1. Add LLM quick scan implementation
2. PDF report generation
3. Connect frontend to backend
4. Deploy to production

### 📖 Learn More:
- [Full API Documentation](http://localhost:8000/api/docs)
- [Implementation Plan](V1.2_PHASE1_IMPLEMENTATION.md)
- [GitHub Repository](https://github.com/hongping-zh/circular-bias-detection)

---

## 🎉 Success Checklist

- [ ] Server starts without errors
- [ ] Health check returns 200
- [ ] Swagger docs load
- [ ] Bias detection endpoint works
- [ ] Python client works
- [ ] Usage tracking works

**If all checked → You're ready to build!** 🚀

---

**Questions?** Open an issue on GitHub or email yujjam@uest.edu.gr

**Happy coding!** 💻
