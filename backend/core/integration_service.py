"""
Integration Service for Sleuth API and Zenodo Dataset

Combines Zenodo data retrieval with Sleuth bias detection analysis.
"""

import pandas as pd
from typing import Dict, Any, Optional, List
import time
from io import StringIO

from utils.zenodo_client import ZenodoClient
from core.bias_scorer import detect_circular_bias


class IntegrationService:
    """Service to integrate Zenodo data with Sleuth bias detection"""
    
    def __init__(self, doi: str = "10.5281/zenodo.17201032"):
        """
        Initialize integration service.
        
        Args:
            doi: DOI of the Zenodo dataset
        """
        self.zenodo_client = ZenodoClient(doi=doi)
        self.cache = {}  # Simple in-memory cache
    
    def analyze_zenodo_dataset(
        self,
        file_key: Optional[str] = None,
        weights: List[float] = [0.33, 0.33, 0.34],
        run_bootstrap: bool = False,
        n_bootstrap: int = 1000,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Fetch data from Zenodo and run Sleuth bias detection.
        
        Args:
            file_key: Specific file to analyze (None = first CSV file)
            weights: Weights for PSI/CCS/ρ_PC metrics
            run_bootstrap: Whether to run bootstrap confidence intervals
            n_bootstrap: Number of bootstrap iterations
            use_cache: Whether to use cached results
            
        Returns:
            Dictionary with integrated results:
            {
                'source_data': {...},  # Zenodo metadata
                'dataset_info': {...},  # Dataset information
                'sleuth_analysis': {...}  # Bias detection results
            }
        """
        
        cache_key = f"{file_key}_{weights}_{run_bootstrap}_{n_bootstrap}"
        
        # Check cache
        if use_cache and cache_key in self.cache:
            cached_result = self.cache[cache_key]
            cached_result['from_cache'] = True
            return cached_result
        
        start_time = time.time()
        
        # Step 1: Fetch Zenodo metadata
        print(f"📥 Fetching Zenodo record metadata...")
        metadata = self.zenodo_client.get_record_metadata()
        
        # Step 2: Download and parse CSV data
        print(f"📂 Downloading dataset file...")
        df = self.zenodo_client.get_csv_data(file_key=file_key)
        print(f"✅ Downloaded {len(df)} rows, {len(df.columns)} columns")
        
        # Step 3: Validate data format
        validation_error = self._validate_data_for_sleuth(df)
        if validation_error:
            raise ValueError(f"Data validation failed: {validation_error}")
        
        # Step 4: Run Sleuth bias detection
        print(f"🔍 Running Sleuth bias detection (bootstrap={run_bootstrap})...")
        analysis_results = detect_circular_bias(
            df,
            weights=weights,
            run_bootstrap=run_bootstrap,
            n_bootstrap=n_bootstrap
        )
        
        # Step 5: Combine results
        elapsed_time = time.time() - start_time
        
        combined_result = {
            'source_data': {
                'doi': self.zenodo_client.doi,
                'record_id': self.zenodo_client.record_id,
                'title': metadata.get('metadata', {}).get('title', 'N/A'),
                'creators': [c.get('name') for c in metadata.get('metadata', {}).get('creators', [])],
                'publication_date': metadata.get('metadata', {}).get('publication_date', 'N/A'),
                'description': metadata.get('metadata', {}).get('description', 'N/A')[:300] + '...' if len(metadata.get('metadata', {}).get('description', '')) > 300 else metadata.get('metadata', {}).get('description', 'N/A'),
                'license': metadata.get('metadata', {}).get('license', {}).get('id', 'N/A'),
                'access_right': metadata.get('metadata', {}).get('access_right', 'N/A')
            },
            'dataset_info': {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist(),
                'algorithms': df['algorithm'].unique().tolist() if 'algorithm' in df.columns else [],
                'time_periods': sorted(df['time_period'].unique().tolist()) if 'time_period' in df.columns else [],
                'performance_range': {
                    'min': float(df['performance'].min()) if 'performance' in df.columns else None,
                    'max': float(df['performance'].max()) if 'performance' in df.columns else None,
                    'mean': float(df['performance'].mean()) if 'performance' in df.columns else None
                }
            },
            'sleuth_analysis': analysis_results,
            'processing_info': {
                'elapsed_time_seconds': round(elapsed_time, 2),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'from_cache': False
            }
        }
        
        # Cache result
        if use_cache:
            self.cache[cache_key] = combined_result
        
        print(f"✅ Analysis complete in {elapsed_time:.2f}s: CBS={analysis_results['cbs_score']:.3f}, Bias={analysis_results['bias_detected']}")
        
        return combined_result
    
    def get_zenodo_summary(self) -> Dict[str, Any]:
        """
        Get summary information about the Zenodo dataset.
        
        Returns:
            Dictionary with dataset summary
        """
        return self.zenodo_client.get_summary()
    
    def analyze_custom_data_with_zenodo_context(
        self,
        custom_csv: str,
        weights: List[float] = [0.33, 0.33, 0.34],
        run_bootstrap: bool = False,
        n_bootstrap: int = 1000
    ) -> Dict[str, Any]:
        """
        Analyze custom CSV data while providing Zenodo dataset context.
        
        Args:
            custom_csv: CSV string with custom data
            weights: Weights for PSI/CCS/ρ_PC metrics
            run_bootstrap: Whether to run bootstrap confidence intervals
            n_bootstrap: Number of bootstrap iterations
            
        Returns:
            Dictionary with analysis results and Zenodo context
        """
        
        # Get Zenodo context
        zenodo_summary = self.get_zenodo_summary()
        
        # Parse custom data
        df = pd.read_csv(StringIO(custom_csv))
        
        # Validate
        validation_error = self._validate_data_for_sleuth(df)
        if validation_error:
            raise ValueError(f"Data validation failed: {validation_error}")
        
        # Run analysis
        analysis_results = detect_circular_bias(
            df,
            weights=weights,
            run_bootstrap=run_bootstrap,
            n_bootstrap=n_bootstrap
        )
        
        return {
            'zenodo_context': {
                'reference_dataset': zenodo_summary,
                'note': 'This analysis uses custom data. Zenodo dataset provided as reference context.'
            },
            'custom_data_info': {
                'rows': len(df),
                'columns': len(df.columns),
                'algorithms': df['algorithm'].unique().tolist() if 'algorithm' in df.columns else []
            },
            'sleuth_analysis': analysis_results
        }
    
    def clear_cache(self):
        """Clear the results cache"""
        self.cache.clear()
        print("🗑️  Cache cleared")
    
    def _validate_data_for_sleuth(self, df: pd.DataFrame) -> Optional[str]:
        """
        Validate that data is suitable for Sleuth bias detection.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Error message if invalid, None if valid
        """
        # Check required columns
        required_cols = ['time_period', 'algorithm', 'performance']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            return f"Missing required columns: {', '.join(missing_cols)}"
        
        # Check for constraint columns
        constraint_cols = [col for col in df.columns if col.startswith('constraint_')]
        if not constraint_cols:
            return "No constraint columns found. At least one 'constraint_*' column is required."
        
        # Check data types
        if not pd.api.types.is_numeric_dtype(df['time_period']):
            return "'time_period' must be numeric"
        
        if not pd.api.types.is_numeric_dtype(df['performance']):
            return "'performance' must be numeric"
        
        # Check performance range
        if (df['performance'] < 0).any() or (df['performance'] > 1).any():
            return "'performance' values must be in range [0, 1]"
        
        # Check minimum data requirements
        if len(df) < 4:
            return f"Insufficient data: need at least 4 rows, got {len(df)}"
        
        if len(df['algorithm'].unique()) < 2:
            return "At least 2 different algorithms required"
        
        if len(df['time_period'].unique()) < 2:
            return "At least 2 different time periods required"
        
        return None
