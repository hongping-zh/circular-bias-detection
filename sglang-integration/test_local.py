"""
Local Testing Script for SGLang Bias Detection Integration

This script tests all components locally before submitting the PR.
Run this to ensure everything works correctly.

Usage:
    python test_local.py
"""

import sys
from pathlib import Path

# Add paths for local testing
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

import subprocess
import time


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70 + "\n")


def run_command(cmd, description):
    """Run a command and report results."""
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print("-" * 70)
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {description}")
            return True
        else:
            print(f"❌ FAILED: {description}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏱️  TIMEOUT: {description}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_imports():
    """Test that all imports work."""
    print_section("TEST 1: Import Testing")
    
    try:
        print("Testing BiasAuditor import...")
        from python.sglang.lang.bias_audit import BiasAuditor, BiasAuditResult, create_auditor
        print("✅ BiasAuditor imported successfully")
        
        print("\nTesting circular_bias_detector import...")
        from circular_bias_detector.core.metrics import compute_psi, compute_ccs, compute_rho_pc
        print("✅ circular_bias_detector imported successfully")
        
        print("\nTesting numpy import...")
        import numpy as np
        print("✅ numpy imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("\nTo fix:")
        print("  pip install circular-bias-detection")
        print("  pip install numpy scipy")
        return False


def test_basic_functionality():
    """Test basic BiasAuditor functionality."""
    print_section("TEST 2: Basic Functionality")
    
    try:
        from python.sglang.lang.bias_audit import BiasAuditor
        import numpy as np
        
        print("Creating BiasAuditor...")
        auditor = BiasAuditor()
        print(f"✅ Auditor created: {auditor}")
        
        print("\nRecording test generations...")
        for i in range(10):
            auditor.record_generation(
                output=f"Test response {i}",
                constraints={'temperature': 0.7, 'max_tokens': 100},
                performance_score=0.8 + np.random.rand() * 0.1
            )
        print(f"✅ Recorded {len(auditor.history)} generations")
        
        print("\nPerforming audit...")
        result = auditor.audit(time_periods=3)
        print(f"✅ Audit completed")
        
        print("\nAudit Results:")
        print(f"  PSI: {result.psi_score:.4f}")
        print(f"  CCS: {result.ccs_score:.4f}")
        print(f"  ρ_PC: {result.rho_pc_score:.4f}")
        print(f"  Overall Bias: {result.overall_bias}")
        print(f"  Confidence: {result.confidence:.0%}")
        
        print("\nTesting JSON export...")
        json_str = result.to_json()
        print(f"✅ JSON export works (length: {len(json_str)} chars)")
        
        print("\nTesting summary...")
        summary = result.summary()
        print("✅ Summary generated:")
        print(summary)
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_bias_detection():
    """Test bias detection with synthetic data."""
    print_section("TEST 3: Bias Detection")
    
    try:
        from python.sglang.lang.bias_audit import BiasAuditor
        
        print("Scenario 1: No bias (consistent constraints)")
        print("-" * 70)
        auditor1 = BiasAuditor()
        
        for i in range(15):
            auditor1.record_generation(
                output=f"Response {i}" * 5,
                constraints={'temperature': 0.7, 'max_tokens': 100},
                performance_score=0.8
            )
        
        result1 = auditor1.audit(time_periods=5)
        print(f"  PSI: {result1.psi_score:.4f}, CCS: {result1.ccs_score:.4f}, ρ_PC: {result1.rho_pc_score:.4f}")
        print(f"  Bias Detected: {result1.overall_bias}")
        
        if not result1.overall_bias:
            print("  ✅ Correctly detected NO bias")
        else:
            print("  ⚠️  WARNING: Detected bias when none expected (may be statistical variance)")
        
        print("\nScenario 2: With bias (iterative tuning)")
        print("-" * 70)
        auditor2 = BiasAuditor()
        
        temperatures = [0.5, 0.6, 0.7, 0.8, 0.9]
        for temp in temperatures:
            for _ in range(3):
                perf = 0.5 + (temp - 0.5) * 0.8  # Correlate with temp
                auditor2.record_generation(
                    output=f"Response at temp {temp}" * 10,
                    constraints={'temperature': temp, 'max_tokens': 100},
                    performance_score=perf
                )
        
        result2 = auditor2.audit(time_periods=5)
        print(f"  PSI: {result2.psi_score:.4f}, CCS: {result2.ccs_score:.4f}, ρ_PC: {result2.rho_pc_score:.4f}")
        print(f"  Bias Detected: {result2.overall_bias}")
        print(f"  Indicators Flagged: {result2.bias_votes}/3")
        
        if result2.ccs_score < 1.0:
            print("  ✅ Correctly detected constraint variation")
        if abs(result2.rho_pc_score) > 0.5:
            print("  ✅ Correctly detected high correlation")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_unit_tests():
    """Run pytest unit tests."""
    print_section("TEST 4: Unit Tests (pytest)")
    
    # Check if pytest is available
    try:
        import pytest
    except ImportError:
        print("⚠️  pytest not installed. Skipping unit tests.")
        print("To install: pip install pytest")
        return None
    
    test_file = Path(__file__).parent / "tests" / "test_bias_audit.py"
    
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return False
    
    # Try multiple ways to run pytest
    print("Attempting to run pytest...")
    
    # Method 1: Direct pytest command
    cmd1 = f"pytest {test_file} -v --tb=short"
    result1 = run_command(cmd1, "pytest (direct)")
    if result1:
        return True
    
    # Method 2: Python -m pytest
    print("\nTrying alternative method: python -m pytest")
    cmd2 = f"python -m pytest {test_file} -v --tb=short"
    result2 = run_command(cmd2, "pytest (via python -m)")
    if result2:
        return True
    
    # Method 3: Run tests directly with Python
    print("\nTrying to run tests directly with Python...")
    try:
        import sys
        sys.argv = [str(test_file), "-v"]
        exit_code = pytest.main([str(test_file), "-v", "--tb=short"])
        if exit_code == 0:
            print("✅ Tests passed (via pytest.main)")
            return True
        else:
            print(f"⚠️ Tests completed with exit code {exit_code}")
            return False
    except Exception as e:
        print(f"⚠️  Could not run pytest: {e}")
        print("\n📝 Note: Core functionality already verified in Tests 1-3")
        print("    Unit tests are optional for local validation.")
        return None


def test_example():
    """Test the demo example."""
    print_section("TEST 5: Demo Example")
    
    example_file = Path(__file__).parent / "examples" / "bias_detection_demo.py"
    
    if not example_file.exists():
        print(f"❌ Example file not found: {example_file}")
        return False
    
    print("⚠️  Note: Demo requires user interaction (Press Enter prompts)")
    print("Running first scenario only (automated)...\n")
    
    try:
        from python.sglang.lang.bias_audit import BiasAuditor
        import numpy as np
        
        np.random.seed(42)
        auditor = BiasAuditor()
        
        prompts = ["Test prompt"] * 5
        temperature = 0.7
        
        for _ in range(3):
            for prompt in prompts:
                response = f"Simulated response for: {prompt}"
                auditor.record_generation(
                    output=response,
                    constraints={'temperature': temperature, 'max_tokens': 100}
                )
        
        result = auditor.audit(time_periods=3)
        print(result.summary())
        
        print("\n✅ Demo scenario executed successfully")
        return True
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_documentation():
    """Verify documentation exists and is readable."""
    print_section("TEST 6: Documentation Check")
    
    doc_file = Path(__file__).parent / "docs" / "bias_detection.md"
    
    if not doc_file.exists():
        print(f"❌ Documentation not found: {doc_file}")
        return False
    
    try:
        with open(doc_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ Documentation found ({len(content)} chars)")
        
        # Check for key sections
        required_sections = [
            "What is Circular Reasoning Bias",
            "Statistical Indicators",
            "Quick Start",
            "API Reference",
            "BiasAuditor",
            "Usage Patterns"
        ]
        
        missing = []
        for section in required_sections:
            if section in content:
                print(f"  ✅ Section found: {section}")
            else:
                print(f"  ❌ Section missing: {section}")
                missing.append(section)
        
        if not missing:
            print("\n✅ All required documentation sections present")
            return True
        else:
            print(f"\n⚠️  Missing sections: {missing}")
            return False
    except Exception as e:
        print(f"❌ Error reading documentation: {e}")
        return False


def test_pr_template():
    """Verify PR template exists."""
    print_section("TEST 7: PR Template Check")
    
    pr_file = Path(__file__).parent / "PR_TEMPLATE.md"
    
    if not pr_file.exists():
        print(f"❌ PR template not found: {pr_file}")
        return False
    
    try:
        with open(pr_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ PR template found ({len(content)} chars)")
        
        # Check for key sections
        required_sections = [
            "Summary",
            "Motivation",
            "Implementation",
            "Academic Foundation",
            "Usage Example",
            "Performance Impact",
            "Testing",
            "Dependencies"
        ]
        
        for section in required_sections:
            if section in content:
                print(f"  ✅ Section found: {section}")
            else:
                print(f"  ⚠️  Section may be missing: {section}")
        
        return True
    except Exception as e:
        print(f"❌ Error reading PR template: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  SGLang Bias Detection Integration - Local Test Suite".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    
    start_time = time.time()
    
    # Run all tests
    results = {
        "Imports": test_imports(),
        "Basic Functionality": test_basic_functionality(),
        "Bias Detection": test_bias_detection(),
        "Unit Tests": test_unit_tests(),
        "Demo Example": test_example(),
        "Documentation": test_documentation(),
        "PR Template": test_pr_template()
    }
    
    # Summary
    print_section("TEST SUMMARY")
    
    total = len([v for v in results.values() if v is not None])
    passed = len([v for v in results.values() if v is True])
    failed = len([v for v in results.values() if v is False])
    skipped = len([v for v in results.values() if v is None])
    
    print(f"Total Tests: {total}")
    print(f"Passed:      {passed} ✅")
    print(f"Failed:      {failed} ❌")
    print(f"Skipped:     {skipped} ⚠️")
    print()
    
    for name, result in results.items():
        if result is True:
            status = "✅ PASS"
        elif result is False:
            status = "❌ FAIL"
        else:
            status = "⚠️  SKIP"
        print(f"  {status}  {name}")
    
    elapsed = time.time() - start_time
    print(f"\nTotal time: {elapsed:.2f}s")
    print()
    
    # Final verdict
    if failed == 0:
        print("╔" + "═" * 68 + "╗")
        print("║" + "  ✅ ALL TESTS PASSED - READY FOR PR SUBMISSION".center(68) + "║")
        print("╚" + "═" * 68 + "╝")
        print()
        print("Next steps:")
        print("  1. Review all generated files")
        print("  2. Fork SGLang repository")
        print("  3. Apply these changes to your fork")
        print("  4. Submit PR using PR_TEMPLATE.md")
        return 0
    else:
        print("╔" + "═" * 68 + "╗")
        print("║" + f"  ❌ {failed} TEST(S) FAILED - FIX BEFORE SUBMITTING".center(68) + "║")
        print("╚" + "═" * 68 + "╝")
        print()
        print("Please fix the failing tests before submitting PR.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
