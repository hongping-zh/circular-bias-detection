"""
Test script for Zenodo Integration

Demonstrates how to use the Zenodo-Sleuth integration API.
"""

import requests
import json
import time


# Configuration
BASE_URL = "http://localhost:5000"


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_health_check():
    """Test 1: Health check"""
    print_section("TEST 1: Health Check")
    
    response = requests.get(f"{BASE_URL}/health")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {data['status']}")
        print(f"✅ Service: {data['service']}")
        print(f"✅ Version: {data['version']}")
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        return False


def test_zenodo_summary():
    """Test 2: Get Zenodo summary"""
    print_section("TEST 2: Zenodo Dataset Summary")
    
    try:
        response = requests.get(f"{BASE_URL}/api/zenodo/summary", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ DOI: {data['doi']}")
            print(f"✅ Title: {data['title']}")
            print(f"✅ Creators: {', '.join(data['creators'])}")
            print(f"✅ Publication Date: {data['publication_date']}")
            print(f"✅ License: {data['license']}")
            print(f"✅ Files:")
            for file in data['files']:
                size_mb = file['size'] / (1024 * 1024)
                print(f"   - {file['key']} ({size_mb:.2f} MB)")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {str(e)}")
        print("   Tip: Make sure the server is running and Zenodo is accessible")
        return False


def test_analyze_zenodo_simple():
    """Test 3: Simple Zenodo analysis (no bootstrap)"""
    print_section("TEST 3: Analyze Zenodo Dataset (Simple)")
    
    try:
        # Simple request with default parameters
        start_time = time.time()
        
        response = requests.post(
            f"{BASE_URL}/api/analyze_zenodo",
            json={},  # Empty - use defaults
            timeout=60
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Analysis completed in {elapsed:.2f}s")
            print(f"\n📊 Dataset Info:")
            print(f"   - Rows: {data['dataset_info']['rows']}")
            print(f"   - Columns: {data['dataset_info']['columns']}")
            print(f"   - Algorithms: {', '.join(data['dataset_info']['algorithms'])}")
            print(f"   - Time Periods: {data['dataset_info']['time_periods']}")
            
            print(f"\n🔍 Sleuth Analysis:")
            analysis = data['sleuth_analysis']
            print(f"   - CBS Score: {analysis['cbs_score']:.4f}")
            print(f"   - Bias Detected: {analysis['bias_detected']}")
            print(f"   - Interpretation: {analysis['interpretation']}")
            
            if 'metrics' in analysis:
                print(f"\n📈 Detailed Metrics:")
                print(f"   - PSI: {analysis['metrics']['psi']:.4f}")
                print(f"   - CCS: {analysis['metrics']['ccs']:.4f}")
                print(f"   - ρ_PC: {analysis['metrics']['rho_pc']:.4f}")
            
            print(f"\n⏱️  Processing Time: {data['processing_info']['elapsed_time_seconds']}s")
            print(f"   From Cache: {data['processing_info']['from_cache']}")
            
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_analyze_zenodo_with_params():
    """Test 4: Zenodo analysis with custom parameters"""
    print_section("TEST 4: Analyze with Custom Parameters")
    
    try:
        params = {
            "run_bootstrap": False,
            "weights": [0.4, 0.3, 0.3],
            "use_cache": False  # Force fresh analysis
        }
        
        print(f"Parameters: {json.dumps(params, indent=2)}")
        
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/api/analyze_zenodo",
            json=params,
            timeout=60
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Analysis completed in {elapsed:.2f}s")
            print(f"   CBS Score: {data['sleuth_analysis']['cbs_score']:.4f}")
            print(f"   Bias Detected: {data['sleuth_analysis']['bias_detected']}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_cache_functionality():
    """Test 5: Cache functionality"""
    print_section("TEST 5: Cache Functionality")
    
    try:
        # First call - should not be from cache
        print("First call (should compute)...")
        start1 = time.time()
        response1 = requests.post(
            f"{BASE_URL}/api/analyze_zenodo",
            json={"use_cache": True},
            timeout=60
        )
        time1 = time.time() - start1
        
        if response1.status_code == 200:
            data1 = response1.json()
            from_cache1 = data1['processing_info'].get('from_cache', False)
            print(f"   Time: {time1:.2f}s, From cache: {from_cache1}")
        
        # Second call - should be from cache
        print("\nSecond call (should use cache)...")
        start2 = time.time()
        response2 = requests.post(
            f"{BASE_URL}/api/analyze_zenodo",
            json={"use_cache": True},
            timeout=60
        )
        time2 = time.time() - start2
        
        if response2.status_code == 200:
            data2 = response2.json()
            from_cache2 = data2['processing_info'].get('from_cache', False)
            print(f"   Time: {time2:.2f}s, From cache: {from_cache2}")
            
            if from_cache2 and time2 < time1:
                print(f"\n✅ Cache working! Speedup: {time1/time2:.1f}x")
                return True
            else:
                print(f"\n⚠️  Cache may not be working as expected")
                return False
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_clear_cache():
    """Test 6: Clear cache"""
    print_section("TEST 6: Clear Cache")
    
    try:
        response = requests.post(f"{BASE_URL}/api/cache/clear", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['message']}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_api_info():
    """Test 7: API information"""
    print_section("TEST 7: API Information")
    
    try:
        response = requests.get(f"{BASE_URL}/api/info", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Name: {data['name']}")
            print(f"✅ Version: {data['version']}")
            print(f"\n📋 Available Endpoints:")
            for endpoint, info in data['endpoints'].items():
                print(f"   {info['method']:6} {endpoint:30} - {info['description']}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  ZENODO-SLEUTH INTEGRATION TEST SUITE")
    print("=" * 70)
    print(f"\nBase URL: {BASE_URL}")
    print(f"DOI: 10.5281/zenodo.17201032")
    
    results = []
    
    # Run tests
    tests = [
        ("Health Check", test_health_check),
        ("API Info", test_api_info),
        ("Zenodo Summary", test_zenodo_summary),
        ("Simple Analysis", test_analyze_zenodo_simple),
        ("Custom Parameters", test_analyze_zenodo_with_params),
        ("Cache Functionality", test_cache_functionality),
        ("Clear Cache", test_clear_cache),
    ]
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
            time.sleep(0.5)  # Brief pause between tests
        except KeyboardInterrupt:
            print("\n\n⚠️  Tests interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {str(e)}")
            results.append((name, False))
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} {name}")
    
    print(f"\n{'=' * 70}")
    print(f"Total: {passed}/{total} tests passed ({100*passed/total:.0f}%)")
    print(f"{'=' * 70}\n")
    
    return passed == total


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted")
        exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        exit(1)
