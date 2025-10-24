"""
Zenodo API Client

Provides functionality to fetch and parse data from Zenodo datasets.
DOI: 10.5281/zenodo.17201032
"""

import requests
from typing import Dict, List, Optional, Any
import pandas as pd
from io import StringIO


class ZenodoClient:
    """Client for interacting with Zenodo API"""
    
    def __init__(self, doi: str = "10.5281/zenodo.17201032"):
        """
        Initialize Zenodo client.
        
        Args:
            doi: The DOI of the Zenodo dataset
        """
        self.doi = doi
        self.base_url = "https://zenodo.org/api"
        
        # Extract record ID from DOI
        self.record_id = doi.split('.')[-1]
        
    def get_record_metadata(self) -> Dict[str, Any]:
        """
        Fetch metadata for the Zenodo record.
        
        Returns:
            Dictionary containing record metadata
            
        Raises:
            requests.RequestException: If the API request fails
        """
        url = f"{self.base_url}/records/{self.record_id}"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch Zenodo metadata: {str(e)}")
    
    def get_files(self) -> List[Dict[str, Any]]:
        """
        Get list of files in the Zenodo record.
        
        Returns:
            List of file metadata dictionaries
        """
        metadata = self.get_record_metadata()
        return metadata.get('files', [])
    
    def download_file(self, file_url: str) -> bytes:
        """
        Download a file from Zenodo.
        
        Args:
            file_url: Direct URL to the file
            
        Returns:
            File content as bytes
            
        Raises:
            requests.RequestException: If download fails
        """
        try:
            response = requests.get(file_url, timeout=60)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            raise Exception(f"Failed to download file: {str(e)}")
    
    def get_csv_data(self, file_key: Optional[str] = None) -> pd.DataFrame:
        """
        Download and parse CSV data from the Zenodo record.
        
        Args:
            file_key: Optional specific file key to download. 
                     If None, downloads the first CSV file found.
        
        Returns:
            DataFrame containing the CSV data
            
        Raises:
            ValueError: If no CSV file is found
            Exception: If download or parsing fails
        """
        files = self.get_files()
        
        # Find CSV file
        csv_file = None
        if file_key:
            csv_file = next((f for f in files if f.get('key') == file_key), None)
        else:
            # Find first CSV file
            csv_file = next((f for f in files if f.get('key', '').endswith('.csv')), None)
        
        if not csv_file:
            raise ValueError("No CSV file found in Zenodo record")
        
        # Download file
        file_url = csv_file.get('links', {}).get('self')
        if not file_url:
            raise ValueError("File download URL not found")
        
        content = self.download_file(file_url)
        
        # Parse CSV
        try:
            df = pd.read_csv(StringIO(content.decode('utf-8')))
            return df
        except Exception as e:
            raise Exception(f"Failed to parse CSV data: {str(e)}")
    
    def extract_text_fields(self, metadata: Dict[str, Any]) -> str:
        """
        Extract text content from Zenodo record metadata for analysis.
        
        Args:
            metadata: Record metadata dictionary
            
        Returns:
            Combined text string for analysis
        """
        text_parts = []
        
        # Extract title
        if 'title' in metadata.get('metadata', {}):
            text_parts.append(f"Title: {metadata['metadata']['title']}")
        
        # Extract description
        if 'description' in metadata.get('metadata', {}):
            text_parts.append(f"Description: {metadata['metadata']['description']}")
        
        # Extract keywords
        if 'keywords' in metadata.get('metadata', {}):
            keywords = ', '.join(metadata['metadata']['keywords'])
            text_parts.append(f"Keywords: {keywords}")
        
        # Extract notes
        if 'notes' in metadata.get('metadata', {}):
            text_parts.append(f"Notes: {metadata['metadata']['notes']}")
        
        return '\n\n'.join(text_parts)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the Zenodo record.
        
        Returns:
            Dictionary with record summary information
        """
        metadata = self.get_record_metadata()
        meta = metadata.get('metadata', {})
        
        return {
            'doi': self.doi,
            'record_id': self.record_id,
            'title': meta.get('title', 'N/A'),
            'creators': [c.get('name') for c in meta.get('creators', [])],
            'publication_date': meta.get('publication_date', 'N/A'),
            'description': meta.get('description', 'N/A')[:200] + '...' if len(meta.get('description', '')) > 200 else meta.get('description', 'N/A'),
            'keywords': meta.get('keywords', []),
            'files': [{'key': f.get('key'), 'size': f.get('size'), 'type': f.get('type')} for f in metadata.get('files', [])],
            'access_right': meta.get('access_right', 'N/A'),
            'license': meta.get('license', {}).get('id', 'N/A')
        }
