"""
Zenodo Dataset Loader with caching support.

Supports URI formats:
- zenodo://17201032                          # Latest version, all CSV files
- zenodo://17637303                          # CBD Dataset v3/v3.1 (default: largest CSV)
- zenodo://17201032/v2.0.0                   # Specific version
- zenodo://17201032/scenario_high_bias.csv   # Specific file
- file://path/to/data.csv                    # Local file
- https://example.com/data.csv               # Remote URL
"""

import requests
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
import hashlib
import json
from urllib.parse import urlparse


class ZenodoLoader:
    """
    Load datasets from Zenodo with automatic caching.
    
    Features:
    - Automatic download and caching
    - Version management
    - Multiple file support
    - Progress tracking
    - Metadata extraction
    """
    
    CACHE_DIR = Path.home() / ".circular-bias" / "cache"
    METADATA_FILE = CACHE_DIR / "metadata.json"
    BASE_URL = "https://zenodo.org/api/records"
    
    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize Zenodo loader.
        
        Args:
            cache_dir: Custom cache directory (default: ~/.circular-bias/cache)
        """
        if cache_dir:
            self.CACHE_DIR = Path(cache_dir)
        
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self._metadata_cache = self._load_metadata()
    
    def load(self, uri: str, force_download: bool = False) -> pd.DataFrame:
        """
        Load data from URI.
        
        Args:
            uri: Data source URI (zenodo://, file://, https://)
            force_download: Force re-download even if cached
        
        Returns:
            DataFrame with evaluation data
        
        Raises:
            ValueError: If URI format is invalid
            requests.HTTPError: If Zenodo download fails
            FileNotFoundError: If local file not found
        
        Examples:
            >>> loader = ZenodoLoader()
            >>> df = loader.load("zenodo://17201032")
            >>> df = loader.load("zenodo://17201032/scenario_high_bias.csv")
            >>> df = loader.load("file://data/my_data.csv")
        """
        self.logger.info(f"Loading data from: {uri}")
        
        if uri.startswith("zenodo://"):
            return self._load_zenodo(uri, force_download)
        elif uri.startswith("file://"):
            return self._load_local(uri.replace("file://", ""))
        elif uri.startswith("http://") or uri.startswith("https://"):
            return self._load_url(uri)
        else:
            # Assume local path
            return self._load_local(uri)
    
    def _load_zenodo(self, uri: str, force_download: bool = False) -> pd.DataFrame:
        """Load data from Zenodo."""
        # Parse URI: zenodo://record_id[/version][/filename]
        parts = uri.replace("zenodo://", "").split("/")
        record_id = parts[0]
        
        # Determine version and filename
        version = None
        filename = None
        
        if len(parts) > 1:
            if parts[1].startswith('v'):
                version = parts[1]
                filename = parts[2] if len(parts) > 2 else None
            else:
                filename = parts[1]
        
        # Check cache
        cache_key = self._generate_cache_key(record_id, version, filename)
        cached_file = self.CACHE_DIR / f"{cache_key}.csv"
        
        if cached_file.exists() and not force_download:
            self.logger.info(f"Using cached data: {cached_file.name}")
            return pd.read_csv(cached_file)
        
        # Download from Zenodo
        self.logger.info(f"Downloading from Zenodo: {record_id}")
        data = self._download_zenodo(record_id, version, filename)
        
        # Cache the result
        data.to_csv(cached_file, index=False)
        self._update_metadata(cache_key, {
            'record_id': record_id,
            'version': version,
            'filename': filename,
            'uri': uri,
            'rows': len(data),
            'columns': list(data.columns)
        })
        
        self.logger.info(f"Data cached: {cached_file.name} ({len(data)} rows)")
        return data
    
    def _download_zenodo(self, record_id: str, version: Optional[str], 
                        filename: Optional[str]) -> pd.DataFrame:
        """Download data from Zenodo API."""
        # Get record metadata
        url = f"{self.BASE_URL}/{record_id}"
        
        self.logger.debug(f"Fetching metadata from: {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        record = response.json()
        
        # Extract files
        files = record.get('files', [])
        if not files:
            raise ValueError(f"No files found in Zenodo record {record_id}")
        
        # Filter CSV files
        csv_files = [f for f in files if f['key'].endswith('.csv')]
        if not csv_files:
            raise ValueError(f"No CSV files found in Zenodo record {record_id}")
        
        # Select target file
        if filename:
            target_file = next((f for f in csv_files if f['key'] == filename), None)
            if not target_file:
                available = [f['key'] for f in csv_files]
                raise ValueError(f"File '{filename}' not found. Available: {available}")
        else:
            # Default to the largest CSV file for generic records (e.g., 17637303)
            target_file = max(csv_files, key=lambda f: f.get('size', 0))
            self.logger.info(f"No filename specified, using largest CSV: {target_file['key']} ({target_file.get('size', 0)} bytes)")
        
        # Download file
        file_url = target_file['links']['self']
        file_size = target_file.get('size', 0)
        
        self.logger.info(f"Downloading {target_file['key']} ({file_size} bytes)...")
        
        # Stream download for progress tracking
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        
        # Load directly into pandas
        return pd.read_csv(file_url)
    
    def _load_local(self, filepath: str) -> pd.DataFrame:
        """Load data from local file."""
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        self.logger.info(f"Loading local file: {path.name}")
        return pd.read_csv(path)
    
    def _load_url(self, url: str) -> pd.DataFrame:
        """Load data from HTTP(S) URL."""
        self.logger.info(f"Downloading from URL: {url}")
        return pd.read_csv(url)
    
    def _generate_cache_key(self, record_id: str, version: Optional[str], 
                           filename: Optional[str]) -> str:
        """Generate unique cache key."""
        key_parts = [record_id, version or 'latest', filename or 'all']
        key_string = "_".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()[:16]
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load cached metadata."""
        if self.METADATA_FILE.exists():
            with open(self.METADATA_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    def _update_metadata(self, cache_key: str, metadata: Dict[str, Any]) -> None:
        """Update metadata cache."""
        self._metadata_cache[cache_key] = metadata
        with open(self.METADATA_FILE, 'w') as f:
            json.dump(self._metadata_cache, f, indent=2)
    
    def list_cached(self) -> List[Dict[str, Any]]:
        """List all cached datasets."""
        cached = []
        for key, meta in self._metadata_cache.items():
            cache_file = self.CACHE_DIR / f"{key}.csv"
            if cache_file.exists():
                meta['cache_file'] = str(cache_file)
                meta['cache_size'] = cache_file.stat().st_size
                cached.append(meta)
        return cached
    
    def clear_cache(self, record_id: Optional[str] = None) -> int:
        """
        Clear cache.
        
        Args:
            record_id: Clear specific record (None = clear all)
        
        Returns:
            Number of files deleted
        """
        deleted = 0
        
        if record_id:
            # Clear specific record
            keys_to_delete = [k for k, v in self._metadata_cache.items() 
                            if v.get('record_id') == record_id]
        else:
            # Clear all
            keys_to_delete = list(self._metadata_cache.keys())
        
        for key in keys_to_delete:
            cache_file = self.CACHE_DIR / f"{key}.csv"
            if cache_file.exists():
                cache_file.unlink()
                deleted += 1
            del self._metadata_cache[key]
        
        # Update metadata file
        with open(self.METADATA_FILE, 'w') as f:
            json.dump(self._metadata_cache, f, indent=2)
        
        self.logger.info(f"Cleared {deleted} cached files")
        return deleted
    
    def get_zenodo_info(self, record_id: str) -> Dict[str, Any]:
        """
        Get metadata about a Zenodo record.
        
        Args:
            record_id: Zenodo record ID
        
        Returns:
            Dictionary with record metadata
        """
        url = f"{self.BASE_URL}/{record_id}"
        response = requests.get(url)
        response.raise_for_status()
        
        record = response.json()
        
        # Extract useful metadata
        metadata = record.get('metadata', {})
        files = record.get('files', [])
        
        return {
            'record_id': record_id,
            'title': metadata.get('title'),
            'doi': metadata.get('doi'),
            'version': metadata.get('version'),
            'publication_date': metadata.get('publication_date'),
            'creators': metadata.get('creators', []),
            'description': metadata.get('description'),
            'files': [{
                'filename': f['key'],
                'size': f['size'],
                'checksum': f.get('checksum')
            } for f in files],
            'csv_files': [f['key'] for f in files if f['key'].endswith('.csv')]
        }
