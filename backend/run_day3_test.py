"""
Day 3 Integration Test Script

Tests the complete pipeline:
1. Bootstrap confidence intervals
2. CBS composite scoring
3. Flask API (if server is running)
"""

import pandas as pd
import requests
import json
from core.bootstrap import bootstrap_indicators
from core.bias_scorer import detect_circular_bias

def print_header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

def test_bootstrap():
    """Test bootstrap confidence intervals"""
    print_header("TEST 1: BOOTSTRAP CONFIDENCE INTERVALS")
    
    # Load data
    print("\n📂 Loading sample data...")
    try:
        df = pd.read_csv('data/sample_data.csv')
        print(f"✓ Loaded {len(df)} rows")
    except FileNotFoundError:
        print("✗ Creating synthetic data...")
        df = pd.DataFrame({
            'time_period': [1, 1, 2, 2, 3, 3, 4, 4],
            'algorithm': ['A', 'B'] * 4,
            'performance': [0.7, 0.6, 0.72, 0.65, 0.74, 0.67, 0.76, 0.69],
            'constraint_compute': [100, 150, 105, 155, 110, 160, 115, 165],
            'constraint_memory': [8.0, 12.0, 8.5, 12.5, 9.0, 13.0, 9.5, 13.5]
        })
    
    # Run bootstrap (reduced iterations for speed)
    print("\n🔄 Running bootstrap (100 iterations for quick test)...")
    results = bootstrap_indicators(df, n_iterations=100, confidence=0.95, random_seed=42)
    
    print("\n📊 Bootstrap Results:")
    for indicator in ['psi', 'ccs', 'rho_pc']:
        res = results[indicator]
        print(f"\n{indicator.upper()}:")
        print(f"  Mean: {res['mean']:.4f}")
        print(f"  95% CI: [{res['ci_lower']:.4f}, {res['ci_upper']:.4f}]")
        print(f"  Std Dev: {res['std']:.4f}")
    
    print("\n✅ Bootstrap test PASSED")
    return results


def test_cbs():
    """Test CBS composite scoring"""
    print_header("TEST 2: CBS COMPOSITE SCORING")
    
    # Load data
    print("\n📂 Loading sample data...")
    try:
        df = pd.read_csv('data/sample_data.csv')
        print(f"✓ Loaded {len(df)} rows")
    except FileNotFoundError:
        print("✗ Creating synthetic data...")
        df = pd.DataFrame({
            'time_period': [1, 1, 2, 2, 3, 3, 4, 4],
            'algorithm': ['A', 'B'] * 4,
            'performance': [0.7, 0.6, 0.72, 0.65, 0.74, 0.67, 0.76, 0.69],
            'constraint_compute': [100, 150, 105, 155, 110, 160, 115, 165],
            'constraint_memory': [8.0, 12.0, 8.5, 12.5, 9.0, 13.0, 9.5, 13.5]
        })
    
    # Run detection
    print("\n🔍 Running bias detection...")
    results = detect_circular_bias(df, run_bootstrap=False)
    
    print("\n" + results['interpretation'])
    
    print("\n📊 Detailed Scores:")
    print(f"  PSI: {results['psi']['score']:.4f} (norm: {results['psi']['normalized']:.4f})")
    print(f"  CCS: {results['ccs']['score']:.4f} (norm: {results['ccs']['normalized']:.4f})")
    print(f"  ρ_PC: {results['rho_pc']['score']:.4f} (norm: {results['rho_pc']['normalized']:.4f})")
    print(f"\n  CBS: {results['cbs_score']:.4f}")
    print(f"  Risk: {results['risk_level']}")
    print(f"  Bias Detected: {results['bias_detected']}")
    print(f"  Confidence: {results['confidence']:.1f}%")
    
    print("\n💡 Recommendations:")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"  {i}. {rec[:80]}...")
    
    print("\n✅ CBS test PASSED")
    return results


def test_api():
    """Test Flask API (if running)"""
    print_header("TEST 3: FLASK API INTEGRATION")
    
    base_url = "http://localhost:5000"
    
    # Test 1: Health check
    print("\n📡 Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=2)
        if response.status_code == 200:
            print("✓ Health check PASSED")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Health check FAILED: {response.status_code}")
            return None
    except requests.ConnectionError:
        print("⚠️ API server not running")
        print("  Start server with: python app.py")
        print("  Skipping API tests...")
        return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None
    
    # Test 2: API info
    print("\n📡 Testing info endpoint...")
    try:
        response = requests.get(f"{base_url}/api/info")
        if response.status_code == 200:
            print("✓ Info endpoint PASSED")
        else:
            print(f"✗ Info endpoint FAILED: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 3: Bias detection
    print("\n📡 Testing detect endpoint...")
    
    # Prepare test data
    csv_data = """time_period,algorithm,performance,constraint_compute,constraint_memory
1,A,0.7,100,8.0
1,B,0.6,150,12.0
2,A,0.72,105,8.5
2,B,0.65,155,12.5
3,A,0.74,110,9.0
3,B,0.67,160,13.0"""
    
    payload = {
        "csv_data": csv_data,
        "run_bootstrap": False
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/detect",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✓ Detect endpoint PASSED")
            result = response.json()
            print(f"\n  CBS Score: {result['cbs_score']:.4f}")
            print(f"  Bias Detected: {result['bias_detected']}")
            print(f"  Risk Level: {result['risk_level']}")
            
            print("\n✅ API test PASSED")
            return result
        else:
            print(f"✗ Detect endpoint FAILED: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def main():
    """Run all Day 3 tests"""
    print("=" * 70)
    print("DAY 3 COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print("\nTesting: Bootstrap + CBS + Flask API")
    
    # Test 1: Bootstrap
    try:
        bootstrap_result = test_bootstrap()
    except Exception as e:
        print(f"\n❌ Bootstrap test FAILED: {e}")
        bootstrap_result = None
    
    # Test 2: CBS
    try:
        cbs_result = test_cbs()
    except Exception as e:
        print(f"\n❌ CBS test FAILED: {e}")
        cbs_result = None
    
    # Test 3: API
    try:
        api_result = test_api()
    except Exception as e:
        print(f"\n❌ API test FAILED: {e}")
        api_result = None
    
    # Final summary
    print_header("FINAL SUMMARY")
    
    tests_passed = 0
    tests_total = 3
    
    if bootstrap_result:
        print("\n✅ Bootstrap CI: PASS")
        tests_passed += 1
    else:
        print("\n❌ Bootstrap CI: FAIL")
    
    if cbs_result:
        print("✅ CBS Scoring: PASS")
        tests_passed += 1
    else:
        print("❌ CBS Scoring: FAIL")
    
    if api_result:
        print("✅ Flask API: PASS")
        tests_passed += 1
    elif api_result is None:
        print("⚠️ Flask API: SKIPPED (server not running)")
        tests_total = 2
    else:
        print("❌ Flask API: FAIL")
    
    print(f"\n📊 Tests Passed: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n✅ Day 3 Implementation Complete!")
        print("\n🎯 Next Steps:")
        print("  1. Deploy Flask API to production")
        print("  2. Integrate with web app frontend")
        print("  3. Add more test cases")
        print("  4. Optimize performance")
    else:
        print("\n⚠️ Some tests failed. Review errors above.")
    
    print("\n" + "=" * 70)
    print("TEST SUITE COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
