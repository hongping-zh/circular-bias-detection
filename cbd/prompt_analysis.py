"""Prompt variation quantification using Sentence-BERT embeddings.

This module detects potential cheating through prompt engineering by measuring
semantic similarity between prompts using state-of-the-art sentence embeddings.
"""
from typing import List, Dict, Optional, Union, Tuple
import numpy as np
import warnings


def compute_prompt_similarity(
    prompts: List[str],
    model_name: str = "all-MiniLM-L6-v2",
    batch_size: int = 32,
    normalize: bool = True
) -> np.ndarray:
    """Compute pairwise cosine similarity between prompts using Sentence-BERT.
    
    Parameters:
    -----------
    prompts : list of str
        List of prompt texts to compare
    model_name : str, default="all-MiniLM-L6-v2"
        Sentence-BERT model name. Options:
        - "all-MiniLM-L6-v2" (fast, 384 dim, recommended)
        - "all-mpnet-base-v2" (best quality, 768 dim)
        - "paraphrase-multilingual-MiniLM-L12-v2" (multilingual)
    batch_size : int, default=32
        Batch size for encoding
    normalize : bool, default=True
        Whether to normalize embeddings (required for cosine similarity)
    
    Returns:
    --------
    np.ndarray
        Pairwise cosine similarity matrix (n_prompts x n_prompts)
    
    Examples:
    ---------
    >>> prompts = [
    ...     "Translate English to French: Hello",
    ...     "Translate to French: Hello",
    ...     "What is the capital of France?"
    ... ]
    >>> similarity_matrix = compute_prompt_similarity(prompts)
    >>> print(similarity_matrix[0, 1])  # High similarity (paraphrase)
    0.92
    >>> print(similarity_matrix[0, 2])  # Low similarity (different task)
    0.31
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        raise ImportError(
            "sentence-transformers is required for prompt analysis. "
            "Install with: pip install sentence-transformers"
        )
    
    if len(prompts) < 2:
        raise ValueError("Need at least 2 prompts for similarity computation")
    
    # Load model
    model = SentenceTransformer(model_name)
    
    # Encode prompts
    embeddings = model.encode(
        prompts,
        batch_size=batch_size,
        normalize_embeddings=normalize,
        show_progress_bar=False
    )
    
    # Compute pairwise cosine similarity
    similarity_matrix = embeddings @ embeddings.T
    
    return similarity_matrix


def detect_prompt_constraint_cheating(
    prompts: List[str],
    performance_scores: List[float],
    similarity_threshold: float = 0.85,
    performance_variance_threshold: float = 0.1,
    model_name: str = "all-MiniLM-L6-v2"
) -> Dict:
    """Detect potential cheating through prompt constraint manipulation.
    
    This detects the common LLM evaluation cheating pattern where:
    1. Prompts are semantically very similar (high constraint)
    2. But performance varies significantly (suspicious)
    
    Parameters:
    -----------
    prompts : list of str
        List of prompts used in evaluation
    performance_scores : list of float
        Corresponding performance scores (e.g., accuracy, F1)
    similarity_threshold : float, default=0.85
        Cosine similarity threshold above which prompts are considered "too similar"
    performance_variance_threshold : float, default=0.1
        Performance variance threshold above which variation is suspicious
    model_name : str, default="all-MiniLM-L6-v2"
        Sentence-BERT model to use
    
    Returns:
    --------
    dict
        Detection results with similarity matrix, suspicious pairs, and conclusion
    
    Examples:
    ---------
    >>> # Suspicious: very similar prompts, different performance
    >>> prompts = [
    ...     "Translate to French: Hello world",
    ...     "Translate into French: Hello world",
    ...     "French translation: Hello world"
    ... ]
    >>> scores = [0.95, 0.72, 0.88]  # High variance despite similar prompts
    >>> result = detect_prompt_constraint_cheating(prompts, scores)
    >>> print(result['conclusion'])
    "High risk: Found 3 prompt pairs with high similarity but varying performance"
    """
    if len(prompts) != len(performance_scores):
        raise ValueError("prompts and performance_scores must have same length")
    
    if len(prompts) < 2:
        raise ValueError("Need at least 2 prompts for cheating detection")
    
    # Compute prompt similarity
    similarity_matrix = compute_prompt_similarity(prompts, model_name=model_name)
    
    # Find suspicious pairs
    suspicious_pairs = []
    n = len(prompts)
    
    for i in range(n):
        for j in range(i + 1, n):
            sim = similarity_matrix[i, j]
            perf_diff = abs(performance_scores[i] - performance_scores[j])
            
            # High similarity but different performance = suspicious
            if sim >= similarity_threshold and perf_diff >= performance_variance_threshold:
                suspicious_pairs.append({
                    'prompt_idx_1': i,
                    'prompt_idx_2': j,
                    'prompt_1': prompts[i][:100] + "..." if len(prompts[i]) > 100 else prompts[i],
                    'prompt_2': prompts[j][:100] + "..." if len(prompts[j]) > 100 else prompts[j],
                    'similarity': float(sim),
                    'performance_1': float(performance_scores[i]),
                    'performance_2': float(performance_scores[j]),
                    'performance_diff': float(perf_diff)
                })
    
    # Compute statistics
    avg_similarity = float(np.mean(similarity_matrix[np.triu_indices(n, k=1)]))
    max_similarity = float(np.max(similarity_matrix[np.triu_indices(n, k=1)]))
    min_similarity = float(np.min(similarity_matrix[np.triu_indices(n, k=1)]))
    
    performance_variance = float(np.var(performance_scores))
    performance_range = float(np.max(performance_scores) - np.min(performance_scores))
    
    # Risk assessment
    n_suspicious = len(suspicious_pairs)
    total_pairs = n * (n - 1) // 2
    
    if n_suspicious == 0:
        risk_level = "Low"
        conclusion = f"Low risk: No suspicious prompt-performance patterns detected (avg similarity: {avg_similarity:.2f})"
    elif n_suspicious <= total_pairs * 0.2:
        risk_level = "Medium"
        conclusion = f"Medium risk: Found {n_suspicious} suspicious prompt pairs with high similarity but varying performance"
    else:
        risk_level = "High"
        conclusion = f"High risk: Found {n_suspicious} suspicious prompt pairs - possible prompt constraint cheating"
    
    return {
        'risk_level': risk_level,
        'conclusion': conclusion,
        'n_prompts': n,
        'n_suspicious_pairs': n_suspicious,
        'total_pairs': total_pairs,
        'suspicious_pairs': suspicious_pairs,
        'similarity_matrix': similarity_matrix.tolist(),
        'avg_similarity': avg_similarity,
        'max_similarity': max_similarity,
        'min_similarity': min_similarity,
        'performance_variance': performance_variance,
        'performance_range': performance_range,
        'thresholds': {
            'similarity_threshold': similarity_threshold,
            'performance_variance_threshold': performance_variance_threshold
        }
    }


def analyze_prompt_diversity(
    prompts: List[str],
    model_name: str = "all-MiniLM-L6-v2",
    return_clusters: bool = False
) -> Dict:
    """Analyze diversity of prompts in evaluation dataset.
    
    Parameters:
    -----------
    prompts : list of str
        List of prompts to analyze
    model_name : str, default="all-MiniLM-L6-v2"
        Sentence-BERT model to use
    return_clusters : bool, default=False
        If True, perform clustering and return cluster assignments
    
    Returns:
    --------
    dict
        Diversity metrics and optional cluster assignments
    
    Examples:
    ---------
    >>> prompts = ["Translate: ...", "Summarize: ...", "Answer: ..."]
    >>> diversity = analyze_prompt_diversity(prompts)
    >>> print(f"Diversity score: {diversity['diversity_score']:.2f}")
    """
    if len(prompts) < 2:
        raise ValueError("Need at least 2 prompts for diversity analysis")
    
    # Compute similarity matrix
    similarity_matrix = compute_prompt_similarity(prompts, model_name=model_name)
    
    # Diversity metrics
    n = len(prompts)
    upper_triangle = similarity_matrix[np.triu_indices(n, k=1)]
    
    avg_similarity = float(np.mean(upper_triangle))
    std_similarity = float(np.std(upper_triangle))
    min_similarity = float(np.min(upper_triangle))
    max_similarity = float(np.max(upper_triangle))
    
    # Diversity score: lower similarity = higher diversity
    diversity_score = 1.0 - avg_similarity
    
    # Assess diversity level
    if avg_similarity > 0.8:
        diversity_level = "Low"
        assessment = "Prompts are very similar - low diversity may indicate overfitting to specific patterns"
    elif avg_similarity > 0.6:
        diversity_level = "Medium"
        assessment = "Moderate prompt diversity - acceptable for most evaluations"
    else:
        diversity_level = "High"
        assessment = "High prompt diversity - good coverage of different task formulations"
    
    result = {
        'n_prompts': n,
        'diversity_score': diversity_score,
        'diversity_level': diversity_level,
        'assessment': assessment,
        'avg_similarity': avg_similarity,
        'std_similarity': std_similarity,
        'min_similarity': min_similarity,
        'max_similarity': max_similarity,
        'similarity_matrix': similarity_matrix.tolist()
    }
    
    # Optional clustering
    if return_clusters:
        try:
            from sklearn.cluster import AgglomerativeClustering
            
            # Convert similarity to distance
            distance_matrix = 1.0 - similarity_matrix
            
            # Determine optimal number of clusters (heuristic: sqrt(n))
            n_clusters = max(2, min(int(np.sqrt(n)), n // 2))
            
            clustering = AgglomerativeClustering(
                n_clusters=n_clusters,
                metric='precomputed',
                linkage='average'
            )
            cluster_labels = clustering.fit_predict(distance_matrix)
            
            result['n_clusters'] = n_clusters
            result['cluster_labels'] = cluster_labels.tolist()
            
            # Cluster sizes
            unique, counts = np.unique(cluster_labels, return_counts=True)
            result['cluster_sizes'] = dict(zip(unique.tolist(), counts.tolist()))
            
        except ImportError:
            warnings.warn("scikit-learn required for clustering. Install with: pip install scikit-learn")
    
    return result


def compute_prompt_constraint_score(
    prompts: List[str],
    model_name: str = "all-MiniLM-L6-v2"
) -> float:
    """Compute a single constraint score for a set of prompts.
    
    Higher score = more constrained (similar) prompts.
    Lower score = more diverse prompts.
    
    This can be used as a "constraint_text" dimension in bias detection.
    
    Parameters:
    -----------
    prompts : list of str
        List of prompts
    model_name : str, default="all-MiniLM-L6-v2"
        Sentence-BERT model to use
    
    Returns:
    --------
    float
        Constraint score in [0, 1], where 1 = all prompts identical
    
    Examples:
    ---------
    >>> prompts_diverse = ["Translate: ...", "Summarize: ...", "Classify: ..."]
    >>> prompts_similar = ["Translate: A", "Translate: B", "Translate: C"]
    >>> print(compute_prompt_constraint_score(prompts_diverse))  # ~0.3
    >>> print(compute_prompt_constraint_score(prompts_similar))  # ~0.9
    """
    if len(prompts) < 2:
        return 0.0
    
    similarity_matrix = compute_prompt_similarity(prompts, model_name=model_name)
    
    # Average pairwise similarity (excluding diagonal)
    n = len(prompts)
    upper_triangle = similarity_matrix[np.triu_indices(n, k=1)]
    constraint_score = float(np.mean(upper_triangle))
    
    return constraint_score


def batch_prompt_analysis(
    prompt_groups: Dict[str, List[str]],
    performance_groups: Optional[Dict[str, List[float]]] = None,
    model_name: str = "all-MiniLM-L6-v2"
) -> Dict:
    """Analyze multiple groups of prompts (e.g., different models or datasets).
    
    Parameters:
    -----------
    prompt_groups : dict
        Dictionary mapping group names to lists of prompts
    performance_groups : dict, optional
        Dictionary mapping group names to performance scores
    model_name : str, default="all-MiniLM-L6-v2"
        Sentence-BERT model to use
    
    Returns:
    --------
    dict
        Analysis results for each group and cross-group comparisons
    
    Examples:
    ---------
    >>> prompt_groups = {
    ...     'model_A': ["Translate: ...", "Summarize: ..."],
    ...     'model_B': ["Translate: ...", "Answer: ..."]
    ... }
    >>> results = batch_prompt_analysis(prompt_groups)
    """
    results = {}
    
    # Analyze each group
    for group_name, prompts in prompt_groups.items():
        diversity = analyze_prompt_diversity(prompts, model_name=model_name)
        constraint_score = compute_prompt_constraint_score(prompts, model_name=model_name)
        
        group_result = {
            'n_prompts': len(prompts),
            'diversity_score': diversity['diversity_score'],
            'constraint_score': constraint_score,
            'avg_similarity': diversity['avg_similarity'],
            'diversity_level': diversity['diversity_level']
        }
        
        # Add cheating detection if performance provided
        if performance_groups and group_name in performance_groups:
            cheating_result = detect_prompt_constraint_cheating(
                prompts,
                performance_groups[group_name],
                model_name=model_name
            )
            group_result['cheating_detection'] = cheating_result
        
        results[group_name] = group_result
    
    # Cross-group comparison
    if len(prompt_groups) > 1:
        constraint_scores = [results[g]['constraint_score'] for g in prompt_groups.keys()]
        results['cross_group_comparison'] = {
            'avg_constraint_score': float(np.mean(constraint_scores)),
            'std_constraint_score': float(np.std(constraint_scores)),
            'max_constraint_score': float(np.max(constraint_scores)),
            'min_constraint_score': float(np.min(constraint_scores)),
            'most_constrained_group': max(prompt_groups.keys(), key=lambda g: results[g]['constraint_score']),
            'most_diverse_group': min(prompt_groups.keys(), key=lambda g: results[g]['constraint_score'])
        }
    
    return results
