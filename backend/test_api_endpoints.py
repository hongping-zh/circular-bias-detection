"""
Complete API endpoint testing script
Tests all backend functionality after integration
"""

import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 70)
print("API Endpoint Testing Suite")
print("=" * 70)

# Test 1: Health Check
print("\n[TEST 1] Health Check")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("[PASS] Health check successful")
except Exception as e:
    print(f"[FAIL] Health check failed: {e}")

# Test 2: API Info
print("\n[TEST 2] API Information")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/api/info", timeout=5)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Endpoints available: {len(data.get('endpoints', []))}")
    assert response.status_code == 200
    print("[PASS] API info retrieved successfully")
except Exception as e:
    print(f"[FAIL] API info failed: {e}")

# Test 3: Bias Detection (CSV)
print("\n[TEST 3] Bias Detection Endpoint")
print("-" * 70)

# Sample CSV data
csv_data = """time_period,algorithm,performance,constraint_compute,constraint_memory
1,A,0.70,100,8.0
1,B,0.60,150,12.0
2,A,0.72,105,8.5
2,B,0.65,155,12.5
3,A,0.74,110,9.0
3,B,0.67,160,13.0
4,A,0.76,115,9.5
4,B,0.69,165,13.5"""

try:
    response = requests.post(
        f"{BASE_URL}/api/detect",
        data=csv_data,
        headers={'Content-Type': 'text/csv'},
        timeout=30
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"CBS Score: {data.get('cbs_score', 'N/A'):.4f}")
        print(f"Risk Level: {data.get('risk_level', 'N/A')}")
        print(f"Bias Detected: {data.get('bias_detected', 'N/A')}")
        print(f"Confidence: {data.get('confidence', 'N/A'):.1f}%")
        print("\nIndicators:")
        print(f"  PSI: {data.get('psi', {}).get('score', 'N/A'):.4f}")
        print(f"  CCS: {data.get('ccs', {}).get('score', 'N/A'):.4f}")
        print(f"  rho_PC: {data.get('rho_pc', {}).get('score', 'N/A'):.4f}")
        print("[PASS] Bias detection successful")
    else:
        print(f"[FAIL] Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"[FAIL] Bias detection failed: {e}")

# Test 4: CSV Analysis (Gemini)
print("\n[TEST 4] CSV Analysis Endpoint (Gemini AI)")
print("-" * 70)

simple_csv = """name,age,salary
Alice,25,50000
Bob,30,60000
Charlie,35,70000"""

try:
    response = requests.post(
        f"{BASE_URL}/api/analyze-csv",
        data=simple_csv,
        headers={'Content-Type': 'text/plain'},
        timeout=30
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Summary: {data.get('summary', 'N/A')[:100]}...")
        print(f"Mock Mode: {data.get('isMock', False)}")
        print(f"Data Quality Insights: {len(data.get('dataQualityInsights', []))} items")
        print(f"Bias Insights: {len(data.get('biasDetectionInsights', []))} items")
        print("[PASS] CSV analysis successful")
    else:
        print(f"[FAIL] Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"[FAIL] CSV analysis failed: {e}")

# Summary
print("\n" + "=" * 70)
print("Test Suite Complete")
print("=" * 70)
print("\nNext Steps:")
print("1. Check that all tests passed")
print("2. If any failed, check backend logs")
print("3. Test frontend integration")
print("=" * 70)
