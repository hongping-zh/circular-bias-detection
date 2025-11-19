"""One-sentence risk summary generation for non-expert users.

Converts complex statistical results into plain language risk assessments.
"""
from typing import Dict, Optional, List
import numpy as np


def generate_risk_summary(
    detection_result: Dict,
    metric_name: str = "performance",
    include_recommendations: bool = True
) -> str:
    """Generate a one-sentence risk summary from detection results.
    
    Parameters:
    -----------
    detection_result : dict
        Result dictionary from detect_bias() or other detection functions
    metric_name : str, default="performance"
        Name of the metric being evaluated (for clarity)
    include_recommendations : bool, default=True
        Whether to include actionable recommendations
    
    Returns:
    --------
    str
        Plain language risk summary
    
    Examples:
    ---------
    >>> result = detect_bias(model, X, y, accuracy_score)
    >>> summary = generate_risk_summary(result, "accuracy")
    >>> print(summary)
    "高风险：性能随计算资源线性增长（ρ_PC=0.78），可能存在调参作弊"
    """
    p_value = detection_result.get('p_value', 1.0)
    alpha = detection_result.get('alpha', 0.05)
    observed = detection_result.get('observed_metric', 0.0)
    
    # Determine risk level
    if p_value <= 0.001:
        risk_level = "极高风险"
        risk_emoji = "🚨"
    elif p_value <= 0.01:
        risk_level = "高风险"
        risk_emoji = "⚠️"
    elif p_value <= alpha:
        risk_level = "中等风险"
        risk_emoji = "⚡"
    elif p_value <= 0.1:
        risk_level = "低风险"
        risk_emoji = "ℹ️"
    else:
        risk_level = "无明显风险"
        risk_emoji = "✅"
    
    # Build summary components
    components = []
    
    # Main risk statement
    if p_value <= alpha:
        components.append(
            f"{risk_emoji} {risk_level}：{metric_name}异常高 "
            f"(观测值={observed:.3f}, p={p_value:.4f})"
        )
    else:
        components.append(
            f"{risk_emoji} {risk_level}：{metric_name}在正常范围内 "
            f"(p={p_value:.3f} > {alpha})"
        )
    
    # Add specific patterns if available
    patterns = []
    
    # Check for correlation patterns (from PSI analysis)
    if 'psi_correlation' in detection_result:
        corr = detection_result['psi_correlation']
        if abs(corr) > 0.7:
            pattern_type = "线性增长" if corr > 0 else "线性下降"
            patterns.append(f"性能随计算资源{pattern_type}（ρ_PC={corr:.2f}）")
    
    # Check for stratification (imbalanced data handling)
    if detection_result.get('stratified', False):
        patterns.append("已考虑类别不平衡")
    
    # Check for parallel execution
    if detection_result.get('n_jobs', 1) > 1:
        patterns.append(f"使用{detection_result['n_jobs']}核并行验证")
    
    # Check for retrain method (conservative)
    if detection_result.get('null_method') == 'retrain':
        patterns.append("使用保守重训练检验")
    
    if patterns:
        components.append("，".join(patterns))
    
    # Add potential cheating type
    if p_value <= alpha:
        cheating_types = []
        
        if abs(detection_result.get('psi_correlation', 0)) > 0.7:
            cheating_types.append("调参作弊")
        
        if detection_result.get('n_classes', 2) == 2 and observed > 0.95:
            cheating_types.append("数据泄露")
        
        if detection_result.get('subsampled', False):
            cheating_types.append("样本选择偏差")
        
        if cheating_types:
            components.append(f"可能存在{' 或 '.join(cheating_types)}")
    
    # Add recommendations
    if include_recommendations and p_value <= alpha:
        recommendations = _generate_recommendations(detection_result)
        if recommendations:
            components.append(f"建议：{recommendations}")
    
    return "，".join(components)


def generate_batch_risk_summary(
    results: List[Dict],
    test_names: Optional[List[str]] = None,
    correction_applied: bool = False
) -> str:
    """Generate summary for multiple tests.
    
    Parameters:
    -----------
    results : list of dict
        List of detection results
    test_names : list of str, optional
        Names for each test
    correction_applied : bool, default=False
        Whether multiple testing correction was applied
    
    Returns:
    --------
    str
        Batch summary
    
    Examples:
    ---------
    >>> results = [detect_bias(...) for _ in range(5)]
    >>> summary = generate_batch_risk_summary(results)
    >>> print(summary)
    "批量检测：5个测试中3个显示异常（60%），建议进一步审查"
    """
    n_tests = len(results)
    if n_tests == 0:
        return "无测试结果"
    
    # Count significant results
    n_significant = sum(1 for r in results if r.get('p_value', 1.0) <= r.get('alpha', 0.05))
    
    # Count by risk level
    high_risk = sum(1 for r in results if r.get('p_value', 1.0) <= 0.01)
    medium_risk = sum(1 for r in results if 0.01 < r.get('p_value', 1.0) <= 0.05)
    
    # Build summary
    components = []
    
    # Main statement
    if correction_applied:
        components.append(f"🔍 批量检测（已校正多重比较）：")
    else:
        components.append(f"🔍 批量检测：")
    
    components.append(
        f"{n_tests}个测试中{n_significant}个显示异常"
        f"（{n_significant/n_tests*100:.0f}%）"
    )
    
    # Risk breakdown
    if high_risk > 0:
        components.append(f"其中{high_risk}个高风险")
    if medium_risk > 0:
        components.append(f"{medium_risk}个中等风险")
    
    # Overall assessment
    if n_significant == 0:
        components.append("✅ 整体风险低")
    elif n_significant <= n_tests * 0.2:
        components.append("⚡ 部分测试异常，建议重点审查")
    elif n_significant <= n_tests * 0.5:
        components.append("⚠️ 多个测试异常，建议全面审查")
    else:
        components.append("🚨 大量测试异常，强烈建议深入调查")
    
    # List problematic tests
    if test_names and n_significant > 0 and n_significant <= 5:
        problematic = [
            test_names[i] for i, r in enumerate(results)
            if r.get('p_value', 1.0) <= r.get('alpha', 0.05)
        ]
        components.append(f"异常测试：{', '.join(problematic)}")
    
    return "，".join(components)


def generate_prompt_risk_summary(prompt_analysis_result: Dict) -> str:
    """Generate risk summary for prompt constraint analysis.
    
    Parameters:
    -----------
    prompt_analysis_result : dict
        Result from detect_prompt_constraint_cheating()
    
    Returns:
    --------
    str
        Plain language summary
    
    Examples:
    ---------
    >>> result = detect_prompt_constraint_cheating(prompts, scores)
    >>> summary = generate_prompt_risk_summary(result)
    >>> print(summary)
    "⚠️ 中等风险：3组提示词高度相似但性能差异大，可能存在提示词工程作弊"
    """
    risk_level = prompt_analysis_result.get('risk_level', 'Unknown')
    n_suspicious = prompt_analysis_result.get('n_suspicious_pairs', 0)
    avg_sim = prompt_analysis_result.get('avg_similarity', 0)
    perf_var = prompt_analysis_result.get('performance_variance', 0)
    
    # Risk emoji
    risk_emoji = {
        'Low': '✅',
        'Medium': '⚡',
        'High': '🚨'
    }.get(risk_level, 'ℹ️')
    
    # Build summary
    if risk_level == 'Low':
        return (
            f"{risk_emoji} 低风险：提示词多样性正常"
            f"（平均相似度={avg_sim:.2f}），未发现异常模式"
        )
    elif risk_level == 'Medium':
        return (
            f"{risk_emoji} 中等风险：{n_suspicious}组提示词高度相似但性能差异大"
            f"（相似度>{prompt_analysis_result['thresholds']['similarity_threshold']}），"
            f"可能存在提示词工程作弊"
        )
    else:  # High
        return (
            f"{risk_emoji} 高风险：大量提示词异常相似但性能波动"
            f"（{n_suspicious}组可疑配对），"
            f"强烈怀疑通过提示词微调来操纵评测结果"
        )


def generate_multivariate_risk_summary(
    multivariate_result: Dict,
    metric_names: Optional[List[str]] = None
) -> str:
    """Generate risk summary for multivariate detection.
    
    Parameters:
    -----------
    multivariate_result : dict
        Result from multivariate PSI or MANOVA
    metric_names : list of str, optional
        Names of metrics being tested
    
    Returns:
    --------
    str
        Plain language summary
    
    Examples:
    ---------
    >>> result = detect_multivariate_bias(...)
    >>> summary = generate_multivariate_risk_summary(result, ['accuracy', 'F1', 'precision'])
    >>> print(summary)
    "🚨 高风险：3个指标联合显示异常（p=0.002），多维度作弊模式"
    """
    p_value = multivariate_result.get('p_value', 1.0)
    alpha = multivariate_result.get('alpha', 0.05)
    n_metrics = multivariate_result.get('n_metrics', 0)
    test_type = multivariate_result.get('test_type', 'unknown')
    
    # Risk level
    if p_value <= 0.001:
        risk_emoji = "🚨"
        risk_level = "极高风险"
    elif p_value <= 0.01:
        risk_emoji = "⚠️"
        risk_level = "高风险"
    elif p_value <= alpha:
        risk_emoji = "⚡"
        risk_level = "中等风险"
    else:
        risk_emoji = "✅"
        risk_level = "低风险"
    
    # Build summary
    if p_value <= alpha:
        metric_str = f"{n_metrics}个指标" if n_metrics > 1 else "指标"
        if metric_names:
            metric_str = f"{', '.join(metric_names[:3])}" + ("等" if len(metric_names) > 3 else "")
        
        return (
            f"{risk_emoji} {risk_level}：{metric_str}联合显示异常"
            f"（{test_type}, p={p_value:.4f}），"
            f"多维度作弊模式，建议全面审查"
        )
    else:
        return (
            f"{risk_emoji} {risk_level}：{n_metrics}个指标联合检测未发现异常"
            f"（p={p_value:.3f}）"
        )


def _generate_recommendations(detection_result: Dict) -> str:
    """Generate actionable recommendations based on detection results."""
    recommendations = []
    
    p_value = detection_result.get('p_value', 1.0)
    
    # Very strong evidence
    if p_value <= 0.001:
        recommendations.append("立即暂停使用该模型")
        recommendations.append("进行完整的数据审计")
    
    # Strong evidence
    elif p_value <= 0.01:
        recommendations.append("深入调查训练数据来源")
        recommendations.append("检查是否存在数据泄露")
    
    # Moderate evidence
    elif p_value <= 0.05:
        recommendations.append("在独立数据集上重新验证")
        recommendations.append("检查评测流程是否规范")
    
    # Check specific patterns
    if abs(detection_result.get('psi_correlation', 0)) > 0.7:
        recommendations.append("审查超参数调优过程")
    
    if detection_result.get('n_classes', 2) == 2 and detection_result.get('observed_metric', 0) > 0.95:
        recommendations.append("检查测试集是否泄露到训练集")
    
    return "；".join(recommendations[:3])  # Limit to top 3


def format_technical_details(detection_result: Dict, verbose: bool = False) -> str:
    """Format technical details for expert users.
    
    Parameters:
    -----------
    detection_result : dict
        Detection result dictionary
    verbose : bool, default=False
        Include all technical details
    
    Returns:
    --------
    str
        Formatted technical summary
    """
    lines = []
    
    # Core statistics
    lines.append("📊 技术细节：")
    lines.append(f"  观测指标: {detection_result.get('observed_metric', 0):.4f}")
    lines.append(f"  p值: {detection_result.get('p_value', 1.0):.6f}")
    lines.append(f"  显著性水平: {detection_result.get('alpha', 0.05)}")
    lines.append(f"  置换次数: {detection_result.get('n_permutations', 0)}")
    
    # Confidence interval if available
    if 'p_value_ci' in detection_result:
        ci = detection_result['p_value_ci']
        lines.append(f"  p值置信区间: [{ci[0]:.4f}, {ci[1]:.4f}]")
    
    # Method details
    lines.append(f"  零假设方法: {detection_result.get('null_method', 'unknown')}")
    lines.append(f"  并行后端: {detection_result.get('backend', 'sequential')}")
    
    if verbose:
        lines.append(f"  样本数: {detection_result.get('n_samples', 0)}")
        lines.append(f"  类别数: {detection_result.get('n_classes', 0)}")
        lines.append(f"  是否分层: {detection_result.get('stratified', False)}")
        lines.append(f"  是否子采样: {detection_result.get('subsampled', False)}")
    
    return "\n".join(lines)


def create_risk_report(
    detection_result: Dict,
    metric_name: str = "performance",
    include_technical: bool = True,
    include_recommendations: bool = True
) -> str:
    """Create a comprehensive risk report combining summary and details.
    
    Parameters:
    -----------
    detection_result : dict
        Detection result
    metric_name : str
        Metric name
    include_technical : bool, default=True
        Include technical details
    include_recommendations : bool, default=True
        Include recommendations
    
    Returns:
    --------
    str
        Full risk report
    
    Examples:
    ---------
    >>> result = detect_bias(model, X, y, accuracy_score)
    >>> report = create_risk_report(result, "accuracy")
    >>> print(report)
    """
    sections = []
    
    # Main summary
    summary = generate_risk_summary(
        detection_result,
        metric_name,
        include_recommendations=include_recommendations
    )
    sections.append(f"## 风险评估\n{summary}\n")
    
    # Technical details
    if include_technical:
        technical = format_technical_details(detection_result, verbose=True)
        sections.append(f"\n{technical}\n")
    
    # Conclusion
    p_value = detection_result.get('p_value', 1.0)
    alpha = detection_result.get('alpha', 0.05)
    
    if p_value <= alpha:
        sections.append(
            f"\n⚠️ **结论**: 检测到统计学显著的异常模式，"
            f"建议进行进一步调查以排除作弊可能性。"
        )
    else:
        sections.append(
            f"\n✅ **结论**: 未检测到明显的异常模式，"
            f"但仍建议保持警惕并定期监控。"
        )
    
    return "\n".join(sections)
