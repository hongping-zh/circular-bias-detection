"""
Simple Bias Detector - Industrial Edition

快速、直观的偏差检测，专为工业界设计。
- 响应时间 <1秒
- Yes/No判断
- 无需复杂依赖
- 清晰的建议

vs 学术版的区别:
- 无Bootstrap (太慢)
- 无贝叶斯 (太复杂)
- 固定阈值 (够用)
- 简单输出 (清晰)
"""

import numpy as np
import pandas as pd
from typing import Union, List, Optional, Dict
from datetime import datetime


class SimpleBiasDetector:
    """
    工业级简化偏差检测器
    
    专为企业用户设计：
    - 快速响应 (<1秒)
    - 直观结果 (Red/Green)
    - 实用建议
    - 无复杂依赖
    """
    
    def __init__(self,
                 psi_threshold: float = 0.15,
                 ccs_threshold: float = 0.85,
                 rho_pc_threshold: float = 0.5):
        """
        初始化检测器
        
        Parameters:
        -----------
        psi_threshold : float
            参数稳定性阈值 (建议: 0.15)
        ccs_threshold : float
            约束一致性阈值 (建议: 0.85)
        rho_pc_threshold : float
            性能-约束相关性阈值 (建议: 0.5)
        """
        self.psi_threshold = psi_threshold
        self.ccs_threshold = ccs_threshold
        self.rho_pc_threshold = rho_pc_threshold
    
    def quick_check(self,
                    performance_matrix: Union[np.ndarray, pd.DataFrame],
                    constraint_matrix: Union[np.ndarray, pd.DataFrame],
                    algorithm_names: Optional[List[str]] = None) -> Dict:
        """
        快速偏差检测 - 核心API
        
        工业界最常用的接口，返回简单的yes/no判断。
        
        Parameters:
        -----------
        performance_matrix : array-like
            性能数据，shape (T, K)
        constraint_matrix : array-like
            约束数据，shape (T, p)
        algorithm_names : list, optional
            算法名称
            
        Returns:
        --------
        dict
            {
                'has_bias': bool,           # True/False
                'confidence': str,          # 'high', 'medium', 'low'
                'risk_level': str,          # 'critical', 'high', 'medium', 'low'
                'recommendation': str,       # 实用建议
                'details': {...},           # 详细指标
                'timestamp': str            # 检测时间
            }
            
        Example:
        --------
        >>> detector = SimpleBiasDetector()
        >>> result = detector.quick_check(performance, constraints)
        >>> 
        >>> if result['has_bias']:
        >>>     print(f"⚠️ 偏差检测到 - {result['risk_level'].upper()}")
        >>>     print(f"建议: {result['recommendation']}")
        >>> else:
        >>>     print("✅ 无偏差，可安全部署")
        """
        
        # 转换为numpy数组
        if isinstance(performance_matrix, pd.DataFrame):
            performance_matrix = performance_matrix.values
        if isinstance(constraint_matrix, pd.DataFrame):
            constraint_matrix = constraint_matrix.values
        
        # 快速计算核心指标（无Bootstrap）
        from .core import compute_psi, compute_ccs, compute_rho_pc
        
        psi = compute_psi(performance_matrix)
        ccs = compute_ccs(constraint_matrix)
        rho_pc = compute_rho_pc(performance_matrix, constraint_matrix)
        
        # 简单阈值判断
        psi_bias = psi >= self.psi_threshold
        ccs_bias = ccs < self.ccs_threshold
        rho_bias = abs(rho_pc) >= self.rho_pc_threshold
        
        # 总体判断
        has_bias = psi_bias or ccs_bias or rho_bias
        
        # 风险级别评估
        risk_count = sum([psi_bias, ccs_bias, rho_bias])
        if risk_count == 3:
            risk_level = 'critical'
            confidence = 'high'
        elif risk_count == 2:
            risk_level = 'high'
            confidence = 'high'
        elif risk_count == 1:
            risk_level = 'medium'
            confidence = 'medium'
        else:
            risk_level = 'low'
            confidence = 'high'
        
        # 生成实用建议
        recommendation = self._generate_recommendation(psi_bias, ccs_bias, rho_bias)
        
        return {
            'has_bias': has_bias,
            'confidence': confidence,
            'risk_level': risk_level,
            'recommendation': recommendation,
            'details': {
                'psi': {
                    'value': float(psi),
                    'threshold': self.psi_threshold,
                    'status': 'fail' if psi_bias else 'pass',
                    'meaning': 'Parameters changed during evaluation' if psi_bias else 'Parameters stable'
                },
                'ccs': {
                    'value': float(ccs),
                    'threshold': self.ccs_threshold,
                    'status': 'fail' if ccs_bias else 'pass',
                    'meaning': 'Constraints inconsistent' if ccs_bias else 'Constraints consistent'
                },
                'rho_pc': {
                    'value': float(rho_pc),
                    'threshold': self.rho_pc_threshold,
                    'status': 'fail' if rho_bias else 'pass',
                    'meaning': 'Performance depends on constraints' if rho_bias else 'Performance independent'
                }
            },
            'timestamp': datetime.now().isoformat(),
            'algorithm_names': algorithm_names or [],
            'evaluation': {
                'time_periods': len(performance_matrix),
                'num_algorithms': performance_matrix.shape[1] if len(performance_matrix.shape) > 1 else 1,
                'num_constraints': constraint_matrix.shape[1] if len(constraint_matrix.shape) > 1 else 1
            }
        }
    
    def _generate_recommendation(self, psi_bias: bool, ccs_bias: bool, rho_bias: bool) -> str:
        """生成实用的建议"""
        
        if not (psi_bias or ccs_bias or rho_bias):
            return "✅ No bias detected. Safe to deploy this model."
        
        recommendations = []
        
        if psi_bias:
            recommendations.append(
                "🔧 Lock hyperparameters: Your model parameters changed during evaluation. "
                "Fix temperature, max_tokens, and other settings before re-evaluating."
            )
        
        if ccs_bias:
            recommendations.append(
                "📊 Standardize constraints: Your evaluation constraints (compute, memory, dataset size) "
                "varied inconsistently. Use the same environment for all tests."
            )
        
        if rho_bias:
            recommendations.append(
                "⚠️ Performance-constraint dependency: Your model's performance correlates with "
                "constraint changes. This suggests results may be artificially inflated. "
                "Re-evaluate with fixed constraints."
            )
        
        # 总体建议
        recommendations.append(
            "\n💡 Next Steps:\n"
            "1. Address the issues above\n"
            "2. Re-run evaluation with fixed settings\n"
            "3. Scan again to verify fixes"
        )
        
        return "\n\n".join(recommendations)
    
    def generate_simple_report(self, result: Dict) -> str:
        """
        生成简单文本报告（适合打印或发送）
        
        Parameters:
        -----------
        result : dict
            quick_check()的返回结果
            
        Returns:
        --------
        str
            格式化的文本报告
        """
        
        lines = []
        lines.append("=" * 60)
        lines.append("AI BIAS DETECTION REPORT")
        lines.append("=" * 60)
        lines.append("")
        
        # 总体结果
        if result['has_bias']:
            lines.append(f"🔴 BIAS DETECTED - {result['risk_level'].upper()} RISK")
        else:
            lines.append("✅ NO BIAS DETECTED")
        
        lines.append(f"Confidence: {result['confidence'].upper()}")
        lines.append(f"Timestamp: {result['timestamp']}")
        lines.append("")
        
        # 详细指标
        lines.append("DETAILED METRICS:")
        lines.append("-" * 60)
        
        for metric_name, metric_data in result['details'].items():
            status_icon = "❌" if metric_data['status'] == 'fail' else "✅"
            lines.append(f"\n{metric_name.upper()}: {status_icon} {metric_data['status'].upper()}")
            lines.append(f"  Value: {metric_data['value']:.4f}")
            lines.append(f"  Threshold: {metric_data['threshold']:.4f}")
            lines.append(f"  Meaning: {metric_data['meaning']}")
        
        lines.append("")
        lines.append("=" * 60)
        
        # 建议
        lines.append("RECOMMENDATION:")
        lines.append("-" * 60)
        lines.append(result['recommendation'])
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)


def quick_scan(model_id: str = None,
               performance_matrix: np.ndarray = None,
               constraint_matrix: np.ndarray = None) -> Dict:
    """
    全局快速扫描函数（最简单的API）
    
    使用示例:
    >>> result = quick_scan(performance_matrix=perf, constraint_matrix=const)
    >>> print("Bias detected!" if result['has_bias'] else "All clear!")
    
    Parameters:
    -----------
    model_id : str, optional
        模型ID（如果使用LLM自动扫描）
    performance_matrix : np.ndarray
        性能矩阵
    constraint_matrix : np.ndarray
        约束矩阵
        
    Returns:
    --------
    dict
        检测结果
    """
    
    detector = SimpleBiasDetector()
    
    if model_id and performance_matrix is None:
        # LLM自动扫描模式
        # 这里会调用api/llm_pipeline.py
        raise NotImplementedError(
            "LLM auto-scan requires API server. "
            "Please use: python api/llm_pipeline.py"
        )
    
    return detector.quick_check(performance_matrix, constraint_matrix)


# CLI支持
if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("Sleuth Simple Bias Detector - Industrial Edition")
    print("=" * 60)
    print()
    
    # 示例用法
    print("Example Usage:")
    print()
    print("```python")
    print("from circular_bias_detector import SimpleBiasDetector")
    print()
    print("detector = SimpleBiasDetector()")
    print("result = detector.quick_check(performance, constraints)")
    print()
    print("if result['has_bias']:")
    print("    print('⚠️ Bias detected!')")
    print("    print(result['recommendation'])")
    print("else:")
    print("    print('✅ Safe to deploy')")
    print("```")
    print()
    print("For API server, run: python api/llm_pipeline.py")
    print("=" * 60)
