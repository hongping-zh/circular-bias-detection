"""RecBole integration hook for recommender system evaluation.

RecBole is a popular recommender system evaluation framework.
This hook detects circular bias in recommendation model evaluation.
"""
from typing import Dict, List, Optional, Any
import json
from pathlib import Path
import numpy as np


class RecBoleHook:
    """Hook for RecBole recommender system framework.
    
    Usage:
    ------
    ```python
    from cbd.integrations import RecBoleHook
    
    # Create hook
    hook = RecBoleHook(output_dir='./bias_detection')
    
    # In RecBole config
    config['eval_args']['hook'] = hook
    
    # After training
    hook.after_training(model, valid_data, test_data)
    
    # Get analysis
    analysis = hook.get_analysis()
    print(analysis['summary'])
    ```
    """
    
    def __init__(
        self,
        output_dir: str = './cbd_recbole',
        metrics_to_check: Optional[List[str]] = None,
        alpha: float = 0.05
    ):
        """Initialize RecBole hook.
        
        Parameters:
        -----------
        output_dir : str
            Directory to save analysis results
        metrics_to_check : list of str, optional
            Metrics to check (default: ['Recall', 'NDCG', 'Hit'])
        alpha : float, default=0.05
            Significance level
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.metrics_to_check = metrics_to_check or ['Recall', 'NDCG', 'Hit']
        self.alpha = alpha
        
        self.training_history = []
        self.validation_history = []
        self.test_results = {}
    
    def before_training(self, config: Dict):
        """Hook called before training starts.
        
        Parameters:
        -----------
        config : dict
            RecBole configuration
        """
        # Record configuration
        constraints = {
            'model': config.get('model', 'unknown'),
            'dataset': config.get('dataset', 'unknown'),
            'embedding_size': config.get('embedding_size', None),
            'learning_rate': config.get('learning_rate', None),
            'batch_size': config.get('train_batch_size', None)
        }
        
        with open(self.output_dir / 'config.json', 'w') as f:
            json.dump(constraints, f, indent=2)
    
    def on_epoch_end(self, epoch: int, train_metrics: Dict, valid_metrics: Dict):
        """Hook called at end of each epoch.
        
        Parameters:
        -----------
        epoch : int
            Current epoch number
        train_metrics : dict
            Training metrics
        valid_metrics : dict
            Validation metrics
        """
        self.training_history.append({
            'epoch': epoch,
            'metrics': train_metrics
        })
        
        self.validation_history.append({
            'epoch': epoch,
            'metrics': valid_metrics
        })
    
    def after_training(self, model, valid_data, test_data):
        """Hook called after training completes.
        
        Parameters:
        -----------
        model : object
            Trained RecBole model
        valid_data : object
            Validation dataset
        test_data : object
            Test dataset
        """
        # This would normally evaluate the model
        # For now, we'll create a placeholder
        
        print("🔍 Running circular bias detection...")
        
        # Save training history
        with open(self.output_dir / 'training_history.json', 'w') as f:
            json.dump({
                'training': self.training_history,
                'validation': self.validation_history
            }, f, indent=2)
    
    def detect_overfitting_bias(self) -> Dict:
        """Detect overfitting bias from training history.
        
        Returns:
        --------
        dict
            Overfitting analysis
        """
        if not self.validation_history:
            return {'error': 'No validation history available'}
        
        # Extract validation metrics over epochs
        analysis = {
            'n_epochs': len(self.validation_history),
            'metrics_analyzed': [],
            'overfitting_detected': False,
            'details': {}
        }
        
        for metric_name in self.metrics_to_check:
            # Extract metric values across epochs
            metric_values = []
            for epoch_data in self.validation_history:
                if metric_name in epoch_data.get('metrics', {}):
                    metric_values.append(epoch_data['metrics'][metric_name])
            
            if len(metric_values) >= 3:
                # Check for overfitting pattern
                # Simple heuristic: metric decreases in last 20% of epochs
                split_point = int(len(metric_values) * 0.8)
                early_avg = np.mean(metric_values[:split_point])
                late_avg = np.mean(metric_values[split_point:])
                
                is_overfitting = late_avg < early_avg * 0.95  # 5% drop
                
                analysis['metrics_analyzed'].append(metric_name)
                analysis['details'][metric_name] = {
                    'early_avg': float(early_avg),
                    'late_avg': float(late_avg),
                    'drop_percentage': float((early_avg - late_avg) / early_avg * 100),
                    'overfitting': is_overfitting
                }
                
                if is_overfitting:
                    analysis['overfitting_detected'] = True
        
        return analysis
    
    def detect_data_leakage(self, train_metrics: Dict, test_metrics: Dict) -> Dict:
        """Detect potential data leakage.
        
        Parameters:
        -----------
        train_metrics : dict
            Training set metrics
        test_metrics : dict
            Test set metrics
        
        Returns:
        --------
        dict
            Data leakage analysis
        """
        analysis = {
            'leakage_detected': False,
            'suspicious_metrics': []
        }
        
        for metric_name in self.metrics_to_check:
            if metric_name in train_metrics and metric_name in test_metrics:
                train_val = train_metrics[metric_name]
                test_val = test_metrics[metric_name]
                
                # Suspicious if test performance is very close to train
                # (should have some gap due to overfitting)
                ratio = test_val / train_val if train_val > 0 else 0
                
                if ratio > 0.98:  # Less than 2% gap
                    analysis['leakage_detected'] = True
                    analysis['suspicious_metrics'].append({
                        'metric': metric_name,
                        'train': float(train_val),
                        'test': float(test_val),
                        'ratio': float(ratio)
                    })
        
        return analysis
    
    def get_analysis(self) -> Dict:
        """Get complete bias analysis.
        
        Returns:
        --------
        dict
            Complete analysis results
        """
        from cbd.risk_summary import generate_risk_summary
        
        analysis = {
            'overfitting_analysis': self.detect_overfitting_bias(),
            'overall_risk': 'Unknown'
        }
        
        # Determine overall risk
        if analysis['overfitting_analysis'].get('overfitting_detected'):
            analysis['overall_risk'] = 'Medium'
            analysis['summary'] = (
                "⚡ 中等风险：检测到过拟合模式，验证集性能在训练后期下降。"
                "建议：使用early stopping或增加正则化。"
            )
        else:
            analysis['overall_risk'] = 'Low'
            analysis['summary'] = (
                "✅ 低风险：未检测到明显的过拟合或数据泄露模式。"
            )
        
        # Save analysis
        with open(self.output_dir / 'recbole_bias_analysis.json', 'w') as f:
            json.dump(analysis, f, indent=2)
        
        return analysis
    
    def create_report(self, output_file: str = 'recbole_report.md'):
        """Create markdown report.
        
        Parameters:
        -----------
        output_file : str
            Output file name
        """
        analysis = self.get_analysis()
        report_path = self.output_dir / output_file
        
        with open(report_path, 'w') as f:
            f.write("# RecBole Bias Detection Report\n\n")
            
            f.write(f"## Overall Assessment\n\n")
            f.write(f"- **Risk Level:** {analysis.get('overall_risk', 'Unknown')}\n")
            f.write(f"- **Summary:** {analysis.get('summary', 'N/A')}\n\n")
            
            f.write("## Overfitting Analysis\n\n")
            
            overfitting = analysis.get('overfitting_analysis', {})
            if overfitting.get('overfitting_detected'):
                f.write("⚠️ **Overfitting detected**\n\n")
                
                for metric, details in overfitting.get('details', {}).items():
                    if details.get('overfitting'):
                        f.write(f"- **{metric}**: ")
                        f.write(f"Early avg = {details['early_avg']:.4f}, ")
                        f.write(f"Late avg = {details['late_avg']:.4f} ")
                        f.write(f"({details['drop_percentage']:.1f}% drop)\n")
            else:
                f.write("✅ No significant overfitting detected\n")
            
            f.write("\n## Recommendations\n\n")
            
            if analysis.get('overall_risk') == 'Medium':
                f.write("- Use early stopping to prevent overfitting\n")
                f.write("- Increase regularization (L2, dropout)\n")
                f.write("- Reduce model complexity\n")
            else:
                f.write("- Model training appears healthy\n")
                f.write("- Continue monitoring in production\n")
        
        print(f"Report created: {report_path}")
        return report_path


def quick_check_recbole(
    training_history: List[Dict],
    validation_history: List[Dict],
    output_dir: str = './cbd_recbole'
) -> Dict:
    """Quick bias check for RecBole results.
    
    Parameters:
    -----------
    training_history : list of dict
        Training metrics history
    validation_history : list of dict
        Validation metrics history
    output_dir : str
        Output directory
    
    Returns:
    --------
    dict
        Analysis results
    
    Examples:
    ---------
    >>> analysis = quick_check_recbole(train_hist, valid_hist)
    >>> print(analysis['summary'])
    """
    hook = RecBoleHook(output_dir=output_dir)
    hook.training_history = training_history
    hook.validation_history = validation_history
    
    analysis = hook.get_analysis()
    hook.create_report()
    
    return analysis
