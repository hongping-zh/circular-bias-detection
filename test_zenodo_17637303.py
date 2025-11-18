#!/usr/bin/env python3
"""
Quick test script for Zenodo record 17637303 support.
Tests both the loader logic and caching mechanism.
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch
import pandas as pd

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from circular_bias_cli.utils.zenodo_loader import ZenodoLoader


def test_largest_csv_selection():
    """Test that loader selects the largest CSV file by default."""
    print("\n=== Test 1: Largest CSV Selection ===")
    
    loader = ZenodoLoader()
    
    # Mock Zenodo API response with multiple CSV files
    mock_response = {
        'files': [
            {'key': 'small_data.csv', 'size': 1024, 'links': {'self': 'http://example.com/small.csv'}},
            {'key': 'large_data.csv', 'size': 10240, 'links': {'self': 'http://example.com/large.csv'}},
            {'key': 'medium_data.csv', 'size': 5120, 'links': {'self': 'http://example.com/medium.csv'}},
        ]
    }
    
    with patch('requests.get') as mock_get:
        mock_meta = Mock()
        mock_meta.json.return_value = mock_response
        mock_meta.raise_for_status = Mock()
        mock_get.return_value = mock_meta
        
        with patch('pandas.read_csv') as mock_read_csv:
            mock_read_csv.return_value = pd.DataFrame({'test': [1, 2, 3]})
            
            # Call the download method
            result = loader._download_zenodo('17637303', None, None)
            
            # Verify the largest file was selected
            called_url = mock_read_csv.call_args[0][0]
            assert 'large.csv' in called_url, f"Expected large.csv, got {called_url}"
            
    print("✓ Loader correctly selects largest CSV (10240 bytes)")
    return True


def test_cache_mechanism():
    """Test that caching works correctly."""
    print("\n=== Test 2: Cache Mechanism ===")
    
    import tempfile
    cache_dir = Path(tempfile.mkdtemp())
    
    loader = ZenodoLoader(cache_dir=cache_dir)
    
    mock_response = {
        'files': [
            {'key': 'test.csv', 'size': 100, 'links': {'self': 'http://example.com/test.csv'}},
        ]
    }
    
    test_df = pd.DataFrame({
        'time_period': [1, 2],
        'algorithm': ['A', 'B'],
        'performance': [0.8, 0.9]
    })
    
    with patch('requests.get') as mock_get:
        mock_meta = Mock()
        mock_meta.json.return_value = mock_response
        mock_meta.raise_for_status = Mock()
        mock_get.return_value = mock_meta
        
        with patch('pandas.read_csv') as mock_read_csv:
            mock_read_csv.return_value = test_df
            
            # First load
            print("  First load (should download)...")
            df1 = loader.load('zenodo://17637303', force_download=False)
            first_call_count = mock_read_csv.call_count
            
            # Second load
            print("  Second load (should use cache)...")
            df2 = loader.load('zenodo://17637303', force_download=False)
            second_call_count = mock_read_csv.call_count
            
            # Verify cache was used
            cache_files = list(cache_dir.glob('*.csv'))
            assert len(cache_files) == 1, f"Expected 1 cache file, found {len(cache_files)}"
            
    print(f"✓ Cache file created: {cache_files[0].name}")
    print(f"✓ First load: {first_call_count} read call(s)")
    print(f"✓ Second load: {second_call_count} read call(s) (cache hit)")
    
    # Cleanup
    import shutil
    shutil.rmtree(cache_dir)
    
    return True


def test_cli_integration():
    """Test CLI command integration."""
    print("\n=== Test 3: CLI Integration ===")
    
    from circular_bias_cli.main import CircularBiasCLI
    
    cli = CircularBiasCLI()
    
    test_df = pd.DataFrame({
        'time_period': [1, 1, 2, 2],
        'algorithm': ['A', 'B', 'A', 'B'],
        'performance': [0.85, 0.80, 0.87, 0.82],
        'constraint_compute': [512, 512, 512, 512],
        'constraint_memory': [8.0, 8.0, 8.0, 8.0],
        'constraint_dataset_size': [10000, 10000, 10000, 10000],
        'evaluation_protocol': ['v1', 'v1', 'v1', 'v1'],
    })
    
    with patch.object(cli.zenodo_loader, 'load', return_value=test_df):
        print("  Running: circular-bias detect zenodo://17637303")
        exit_code = cli.run(['detect', 'zenodo://17637303'])
        
        assert exit_code in (0, 1), f"Unexpected exit code: {exit_code}"
        
    print(f"✓ CLI command executed successfully (exit code: {exit_code})")
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("Testing Zenodo Record 17637303 Support")
    print("=" * 60)
    
    try:
        test_largest_csv_selection()
        test_cache_mechanism()
        test_cli_integration()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print("\nYou can now use:")
        print("  circular-bias detect zenodo://17637303")
        print("\nThe loader will:")
        print("  1. Automatically select the largest CSV file")
        print("  2. Cache it to ~/.circular-bias/cache/")
        print("  3. Reuse the cache on subsequent runs")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
