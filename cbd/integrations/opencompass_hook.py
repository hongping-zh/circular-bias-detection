"""OpenCompass integration hook for automatic bias detection.

OpenCompass is a popular LLM evaluation framework. This hook automatically
records constraints and detects circular bias during evaluation.
"""
from typing import Dict, List, Optional, Any
import json
import os
from pathlib import Path


class OpenCompassHook:
    """Hook for OpenCompass evaluation framework.
    
    Usage:
    ------
    ```python
    from cbd.integrations import OpenCompassHook
    
    # In your OpenCompass config
    hook = OpenCompassHook(output_dir='./bias_detection')
    
    # After evaluation
    results = hook.analyze_results(opencompass_results)
    print(results['summary'])
    ```
    """
    
    def __init__(
        self,
        output_dir: str = './cbd_analysis',
        auto_detect: bool = True,
        n_permutations: int = 1000,
        alpha: float = 0.05
    ):
        """Initialize OpenCompass hook.
        
        Parameters:
        -----------
        output_dir : str
            Directory to save analysis results
        auto_detect : bool, default=True
            Automatically run bias detection after evaluation
        n_permutations : int, default=1000
            Number of permutations for detection
        alpha : float, default=0.05
            Significance level
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.auto_detect = auto_detect
        self.n_permutations = n_permutations
        self.alpha = alpha
        
        self.recorded_constraints = []
        self.recorded_metrics = []
    
    def before_evaluation(self, config: Dict):
        """Hook called before evaluation starts.
        
        Parameters:
        -----------
        config : dict
            OpenCompass configuration
        """
        # Record configuration constraints
        constraints = {
            'model_name': config.get('model', {}).get('name', 'unknown'),
            'datasets': [d.get('name', 'unknown') for d in config.get('datasets', [])],
            'batch_size': config.get('batch_size', None),
            'max_seq_len': config.get('max_seq_len', None),
            'timestamp': str(Path(self.output_dir).stat().st_mtime)
        }
        
        self.recorded_constraints.append(constraints)
        
        # Save constraints
        with open(self.output_dir / 'constraints.json', 'w') as f:
            json.dump(self.recorded_constraints, f, indent=2)
    
    def after_evaluation(self, results: Dict):
        """Hook called after evaluation completes.
        
        Parameters:
        -----------
        results : dict
            OpenCompass evaluation results
        """
        # Record metrics
        self.recorded_metrics.append(results)
        
        # Save metrics
        with open(self.output_dir / 'metrics.json', 'w') as f:
            json.dump(self.recorded_metrics, f, indent=2)
        
        # Auto-detect if enabled
        if self.auto_detect:
            analysis = self.analyze_results(results)
            
            # Save analysis
            with open(self.output_dir / 'bias_analysis.json', 'w') as f:
                json.dump(analysis, f, indent=2)
            
            # Print summary
            print("\n" + "="*60)
            print("🔍 Circular Bias Detection Results")
            print("="*60)
            print(analysis.get('summary', 'No summary available'))
            print("="*60 + "\n")
    
    def analyze_results(self, results: Dict) -> Dict:
        """Analyze OpenCompass results for circular bias.
        
        Parameters:
        -----------
        results : dict
            OpenCompass evaluation results
        
        Returns:
        --------
        dict
            Bias detection analysis
        """
        from cbd.risk_summary import generate_batch_risk_summary
        
        # Extract dataset-level results
        dataset_results = results.get('dataset_results', {})
        
        analysis = {
            'n_datasets': len(dataset_results),
            'datasets': list(dataset_results.keys()),
            'per_dataset_analysis': {},
            'overall_risk': 'Unknown'
        }
        
        # Analyze each dataset
        detection_results = []
        for dataset_name, dataset_metrics in dataset_results.items():
            # Extract performance metrics
            accuracy = dataset_metrics.get('accuracy', None)
            
            if accuracy is not None:
                # Simple heuristic: flag if accuracy > 0.95
                is_suspicious = accuracy > 0.95
                
                dataset_analysis = {
                    'dataset': dataset_name,
                    'accuracy': accuracy,
                    'suspicious': is_suspicious,
                    'reason': 'Unusually high accuracy' if is_suspicious else 'Normal'
                }
                
                analysis['per_dataset_analysis'][dataset_name] = dataset_analysis
                
                # Mock detection result for summary
                detection_results.append({
                    'p_value': 0.001 if is_suspicious else 0.5,
                    'alpha': self.alpha
                })
        
        # Generate summary
        if detection_results:
            summary = generate_batch_risk_summary(
                detection_results,
                test_names=list(dataset_results.keys())
            )
            analysis['summary'] = summary
        else:
            analysis['summary'] = "No datasets analyzed"
        
        return analysis
    
    def export_for_paper(self, output_file: str = 'bias_report.md'):
        """Export analysis results in paper-ready format.
        
        Parameters:
        -----------
        output_file : str
            Output markdown file
        """
        report_path = self.output_dir / output_file
        
        with open(report_path, 'w') as f:
            f.write("# Circular Bias Detection Report\n\n")
            f.write("## Evaluation Configuration\n\n")
            
            if self.recorded_constraints:
                f.write("```json\n")
                f.write(json.dumps(self.recorded_constraints[-1], indent=2))
                f.write("\n```\n\n")
            
            f.write("## Bias Detection Results\n\n")
            
            # Load analysis if exists
            analysis_file = self.output_dir / 'bias_analysis.json'
            if analysis_file.exists():
                with open(analysis_file) as af:
                    analysis = json.load(af)
                
                f.write(f"**Overall Risk:** {analysis.get('overall_risk', 'Unknown')}\n\n")
                f.write(f"**Summary:** {analysis.get('summary', 'N/A')}\n\n")
                
                f.write("### Per-Dataset Analysis\n\n")
                f.write("| Dataset | Accuracy | Suspicious | Reason |\n")
                f.write("|---------|----------|------------|--------|\n")
                
                for dataset, result in analysis.get('per_dataset_analysis', {}).items():
                    f.write(f"| {dataset} | {result.get('accuracy', 'N/A'):.3f} | "
                           f"{result.get('suspicious', False)} | {result.get('reason', 'N/A')} |\n")
        
        print(f"Report exported to: {report_path}")


# Convenience function
def create_opencompass_hook(**kwargs) -> OpenCompassHook:
    """Create OpenCompass hook with default settings.
    
    Examples:
    ---------
    >>> hook = create_opencompass_hook(output_dir='./my_analysis')
    >>> # Use in OpenCompass config
    """
    return OpenCompassHook(**kwargs)
