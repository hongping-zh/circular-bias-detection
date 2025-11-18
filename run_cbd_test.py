#!/usr/bin/env python3
"""Simple test runner for CBD package without pytest issues."""

import sys
sys.path.insert(0, '.')

from tests.test_api import test_detect_bias_sanity

try:
    print("=" * 60)
    print("Running CBD Package Tests")
    print("=" * 60)
    
    print("\n[TEST] test_detect_bias_sanity...")
    test_detect_bias_sanity()
    print("✓ PASSED")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
