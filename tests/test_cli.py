import json
import pandas as pd
import pytest
from unittest.mock import Mock, patch
from circular_bias_cli.main import CircularBiasCLI
from circular_bias_cli.utils.zenodo_loader import ZenodoLoader


def _make_sample_csv(path):
    df = pd.DataFrame(
        {
            "time_period": [1, 1, 2, 2, 3, 3],
            "algorithm": ["A", "B", "A", "B", "A", "B"],
            "performance": [0.80, 0.78, 0.82, 0.79, 0.83, 0.81],
            "constraint_compute": [512, 512, 512, 512, 512, 512],
            "constraint_memory": [8.0, 8.0, 8.0, 8.0, 8.0, 8.0],
            "constraint_dataset_size": [10000, 10000, 10000, 10000, 10000, 10000],
        }
    )
    df.to_csv(path, index=False)


def test_cli_detect_json_output(tmp_path):
    csv_path = tmp_path / "sample.csv"
    out_json = tmp_path / "results.json"
    _make_sample_csv(csv_path)

    cli = CircularBiasCLI()
    exit_code = cli.run([
        "detect",
        str(csv_path),
        "--format",
        "json",
        "--output",
        str(out_json),
    ])

    # Should return 0 or 1 depending on detection
    assert exit_code in (0, 1)
    assert out_json.exists()
    data = json.loads(out_json.read_text())
    assert isinstance(data, dict)


def test_cli_info_local_file(tmp_path, capsys):
    csv_path = tmp_path / "sample.csv"
    _make_sample_csv(csv_path)

    cli = CircularBiasCLI()
    exit_code = cli.run(["info", str(csv_path)])

    assert exit_code == 0
    captured = capsys.readouterr().out
    assert "Rows:" in captured
    assert "Columns:" in captured


def test_cli_list_algorithms(capsys):
    cli = CircularBiasCLI()
    exit_code = cli.run(["list-algorithms"]) 
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Available Algorithms" in out


def test_zenodo_loader_selects_largest_csv():
    """Test that ZenodoLoader picks the largest CSV by default."""
    loader = ZenodoLoader()
    
    # Mock Zenodo API response with multiple CSV files
    mock_response = {
        'files': [
            {'key': 'small.csv', 'size': 1000, 'links': {'self': 'http://example.com/small.csv'}},
            {'key': 'large.csv', 'size': 5000, 'links': {'self': 'http://example.com/large.csv'}},
            {'key': 'medium.csv', 'size': 3000, 'links': {'self': 'http://example.com/medium.csv'}},
        ]
    }
    
    with patch('requests.get') as mock_get:
        # Mock metadata request
        mock_meta = Mock()
        mock_meta.json.return_value = mock_response
        mock_meta.raise_for_status = Mock()
        
        # Mock CSV download request
        mock_csv = Mock()
        mock_csv.raise_for_status = Mock()
        
        mock_get.side_effect = [mock_meta, mock_csv]
        
        with patch('pandas.read_csv') as mock_read_csv:
            mock_read_csv.return_value = pd.DataFrame({'col': [1, 2, 3]})
            
            # Should select 'large.csv' (5000 bytes)
            result = loader._download_zenodo('17637303', None, None)
            
            # Verify pandas.read_csv was called with the largest file URL
            mock_read_csv.assert_called_once_with('http://example.com/large.csv')


def test_zenodo_cache_mechanism(tmp_path):
    """Test that caching works: first download, second load from cache."""
    loader = ZenodoLoader(cache_dir=tmp_path)
    
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
            
            # First load: should download
            df1 = loader.load('zenodo://17637303', force_download=False)
            assert len(df1) == 2
            assert mock_read_csv.call_count == 1
            
            # Second load: should use cache (no new download)
            df2 = loader.load('zenodo://17637303', force_download=False)
            assert len(df2) == 2
            # read_csv called once more to read from cache file
            assert mock_read_csv.call_count == 2
            
            # Verify cache file exists
            cache_files = list(tmp_path.glob('*.csv'))
            assert len(cache_files) == 1


def test_cli_detect_zenodo_17637303():
    """Test CLI command: circular-bias detect zenodo://17637303"""
    cli = CircularBiasCLI()
    
    # Mock the loader to avoid actual network call
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
        exit_code = cli.run(['detect', 'zenodo://17637303'])
        
        # Should complete successfully (0 or 1 depending on detection)
        assert exit_code in (0, 1)
