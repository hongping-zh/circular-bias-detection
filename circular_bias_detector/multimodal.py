"""
Multi-Modal Support for Vision-Language Models (VLMs)

Extends Sleuth to support bias detection in multi-modal AI systems:
- Vision-Language Models (CLIP, GPT-4V, LLaVA)
- Multi-modal constraints (image resolution, latency)
- HELM/MMLU benchmarks
- Cross-modal bias detection
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Union
import warnings

try:
    import clip
    import torch
    from PIL import Image
    HAS_CLIP = True
except ImportError:
    HAS_CLIP = False
    warnings.warn("CLIP not installed. Install with: pip install git+https://github.com/openai/CLIP.git")


class MultiModalConstraintMatrix:
    """
    Extended constraint matrix for multi-modal evaluations.
    
    Supports both text-only and vision-language constraints.
    """
    
    def __init__(self, constraint_type: str = "text_only"):
        """
        Initialize multi-modal constraint matrix.
        
        Parameters:
        -----------
        constraint_type : str
            "text_only", "vision_only", or "multi_modal"
        """
        self.constraint_type = constraint_type
        self.constraints = []
        
    def add_text_constraints(self, 
                            max_tokens: int,
                            temperature: float,
                            memory_gb: float):
        """Add text model constraints"""
        self.constraints.append({
            'modality': 'text',
            'max_tokens': max_tokens,
            'temperature': temperature,
            'memory_gb': memory_gb
        })
        
    def add_vision_constraints(self,
                              image_resolution: Tuple[int, int],
                              inference_time_ms: float,
                              memory_gb: float):
        """Add vision model constraints"""
        self.constraints.append({
            'modality': 'vision',
            'image_resolution': image_resolution,
            'inference_time_ms': inference_time_ms,
            'memory_gb': memory_gb
        })
        
    def add_multimodal_constraints(self,
                                   text_max_tokens: int,
                                   image_resolution: Tuple[int, int],
                                   temperature: float,
                                   inference_time_ms: float,
                                   memory_gb: float):
        """Add vision-language model constraints"""
        self.constraints.append({
            'modality': 'multi_modal',
            'text_max_tokens': text_max_tokens,
            'image_resolution': image_resolution,
            'temperature': temperature,
            'inference_time_ms': inference_time_ms,
            'memory_gb': memory_gb
        })
    
    def to_matrix(self) -> np.ndarray:
        """
        Convert to numpy matrix for bias detection.
        
        Returns:
        --------
        np.ndarray
            Shape (T, p) where T is time periods, p is constraint dimensions
        """
        if not self.constraints:
            raise ValueError("No constraints added")
        
        # Normalize different constraint types to fixed-length vectors
        matrix_rows = []
        
        for constraint in self.constraints:
            if constraint['modality'] == 'text':
                row = [
                    constraint['max_tokens'],
                    constraint['temperature'],
                    constraint['memory_gb'],
                    0,  # image_res_width (not applicable)
                    0,  # image_res_height
                    0   # inference_time_ms
                ]
            elif constraint['modality'] == 'vision':
                row = [
                    0,  # max_tokens (not applicable)
                    0,  # temperature
                    constraint['memory_gb'],
                    constraint['image_resolution'][0],
                    constraint['image_resolution'][1],
                    constraint['inference_time_ms']
                ]
            else:  # multi_modal
                row = [
                    constraint['text_max_tokens'],
                    constraint['temperature'],
                    constraint['memory_gb'],
                    constraint['image_resolution'][0],
                    constraint['image_resolution'][1],
                    constraint['inference_time_ms']
                ]
            
            matrix_rows.append(row)
        
        return np.array(matrix_rows)
    
    def get_constraint_names(self) -> List[str]:
        """Get human-readable constraint names"""
        return [
            'text_max_tokens',
            'temperature',
            'memory_gb',
            'image_width',
            'image_height',
            'inference_time_ms'
        ]


def evaluate_clip_model(
    model_name: str = "ViT-B/32",
    image_texts_pairs: Optional[List[Tuple[str, str]]] = None,
    device: str = "cpu"
) -> Dict[str, Union[float, List[float]]]:
    """
    Evaluate CLIP model and return performance + constraint metrics.
    
    Parameters:
    -----------
    model_name : str
        CLIP model variant (e.g., "ViT-B/32", "ViT-L/14")
    image_texts_pairs : list of tuples, optional
        List of (image_path, text) pairs for evaluation
    device : str
        "cpu" or "cuda"
        
    Returns:
    --------
    dict
        {
            'clip_score': float,  # Average CLIP similarity
            'image_resolution': tuple,
            'inference_time_ms': float,
            'memory_gb': float
        }
    """
    
    if not HAS_CLIP:
        raise ImportError("CLIP not installed. Install with: pip install git+https://github.com/openai/CLIP.git")
    
    import time
    
    # Load CLIP model
    model, preprocess = clip.load(model_name, device=device)
    
    if image_texts_pairs is None:
        # Return model specs only
        return {
            'model_name': model_name,
            'device': device,
            'image_resolution': (224, 224) if "B" in model_name else (336, 336)
        }
    
    # Evaluate on provided pairs
    scores = []
    inference_times = []
    
    for img_path, text in image_texts_pairs:
        # Load and preprocess image
        image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)
        text_input = clip.tokenize([text]).to(device)
        
        # Measure inference time
        start_time = time.time()
        
        with torch.no_grad():
            image_features = model.encode_image(image)
            text_features = model.encode_text(text_input)
            
            # Compute cosine similarity
            similarity = (image_features @ text_features.T).item()
        
        inference_time = (time.time() - start_time) * 1000  # ms
        
        scores.append(similarity)
        inference_times.append(inference_time)
    
    # Estimate memory usage
    memory_gb = torch.cuda.memory_allocated(device) / 1e9 if device == "cuda" else 0.5
    
    return {
        'clip_score': np.mean(scores),
        'clip_scores_all': scores,
        'image_resolution': (224, 224) if "B" in model_name else (336, 336),
        'inference_time_ms': np.mean(inference_times),
        'memory_gb': memory_gb,
        'model_name': model_name
    }


def load_helm_benchmark(
    benchmark_name: str = "summarization",
    subset: str = "cnn_dailymail"
) -> Dict:
    """
    Load HELM benchmark data for multi-modal evaluation.
    
    HELM (Holistic Evaluation of Language Models) provides comprehensive
    benchmarks across multiple scenarios.
    
    Parameters:
    -----------
    benchmark_name : str
        HELM scenario (e.g., "summarization", "question_answering", "image_caption")
    subset : str
        Dataset subset
        
    Returns:
    --------
    dict
        Benchmark data and metadata
    """
    
    # Placeholder implementation
    # In production, integrate with official HELM API
    
    available_benchmarks = {
        "summarization": ["cnn_dailymail", "xsum"],
        "question_answering": ["natural_questions", "triviaqa"],
        "image_caption": ["coco", "flickr30k"],
        "vqa": ["vqav2", "gqa"]
    }
    
    if benchmark_name not in available_benchmarks:
        raise ValueError(f"Benchmark '{benchmark_name}' not supported. "
                        f"Available: {list(available_benchmarks.keys())}")
    
    return {
        "benchmark": benchmark_name,
        "subset": subset,
        "url": f"https://crfm.stanford.edu/helm/latest/?group={benchmark_name}",
        "note": "HELM integration placeholder. Implement full loading logic."
    }


def load_mmlu_benchmark(
    subject: str = "abstract_algebra",
    split: str = "test"
) -> Dict:
    """
    Load MMLU (Massive Multitask Language Understanding) benchmark.
    
    Parameters:
    -----------
    subject : str
        MMLU subject (57 subjects available)
    split : str
        "dev", "test", or "val"
        
    Returns:
    --------
    dict
        MMLU data and metadata
    """
    
    try:
        from datasets import load_dataset
        
        dataset = load_dataset("cais/mmlu", subject, split=split)
        
        return {
            "subject": subject,
            "split": split,
            "num_examples": len(dataset),
            "dataset": dataset,
            "url": "https://github.com/hendrycks/test"
        }
        
    except ImportError:
        warnings.warn("datasets library not installed. Install with: pip install datasets")
        return {
            "subject": subject,
            "split": split,
            "note": "Install datasets library to load MMLU"
        }


def detect_multimodal_bias(
    text_performance: np.ndarray,
    vision_performance: np.ndarray,
    multimodal_constraints: MultiModalConstraintMatrix,
    algorithm_names: Optional[List[str]] = None
) -> Dict:
    """
    Detect circular bias in multi-modal AI evaluation.
    
    Analyzes whether vision and language modalities exhibit
    circular reasoning patterns independently or jointly.
    
    Parameters:
    -----------
    text_performance : np.ndarray
        Text-only performance matrix, shape (T, K)
    vision_performance : np.ndarray
        Vision-only performance matrix, shape (T, K)
    multimodal_constraints : MultiModalConstraintMatrix
        Combined constraints
    algorithm_names : list, optional
        Algorithm/model names
        
    Returns:
    --------
    dict
        Multi-modal bias detection results
    """
    
    from circular_bias_detector import BiasDetector
    
    # Combined performance (average of text and vision)
    combined_performance = (text_performance + vision_performance) / 2
    
    # Convert constraints to matrix
    constraint_matrix = multimodal_constraints.to_matrix()
    
    # Standard bias detection
    detector = BiasDetector(
        psi_threshold=0.15,
        ccs_threshold=0.85,
        rho_pc_threshold=0.5
    )
    
    results_combined = detector.detect_bias(
        performance_matrix=combined_performance,
        constraint_matrix=constraint_matrix,
        algorithm_names=algorithm_names,
        enable_bootstrap=True
    )
    
    # Modality-specific analysis
    results_text = detector.detect_bias(
        performance_matrix=text_performance,
        constraint_matrix=constraint_matrix[:, :3],  # Text constraints only
        algorithm_names=algorithm_names
    )
    
    results_vision = detector.detect_bias(
        performance_matrix=vision_performance,
        constraint_matrix=constraint_matrix[:, 3:],  # Vision constraints only
        algorithm_names=algorithm_names
    )
    
    return {
        'combined': results_combined,
        'text_only': results_text,
        'vision_only': results_vision,
        'cross_modal_correlation': np.corrcoef(
            text_performance.flatten(),
            vision_performance.flatten()
        )[0, 1],
        'recommendation': _interpret_multimodal_results(
            results_combined, results_text, results_vision
        )
    }


def _interpret_multimodal_results(
    combined: Dict,
    text: Dict,
    vision: Dict
) -> str:
    """Generate interpretation of multi-modal bias results"""
    
    report = []
    
    if combined['overall_bias']:
        report.append("⚠️  MULTI-MODAL BIAS DETECTED")
        
        if text['overall_bias'] and vision['overall_bias']:
            report.append("Both text and vision modalities show circular bias.")
            report.append("Recommendation: Re-evaluate entire multi-modal pipeline.")
        elif text['overall_bias']:
            report.append("Bias primarily in text modality.")
            report.append("Recommendation: Fix text prompt engineering.")
        elif vision['overall_bias']:
            report.append("Bias primarily in vision modality.")
            report.append("Recommendation: Standardize image preprocessing.")
        else:
            report.append("Bias emerges only when modalities combined.")
            report.append("Recommendation: Review fusion mechanism.")
    else:
        report.append("✅ NO MULTI-MODAL BIAS DETECTED")
        report.append("Both modalities appear unbiased.")
    
    return "\n".join(report)


# Example datasets for multi-modal evaluation
MULTIMODAL_BENCHMARKS = {
    "COCO_Captions": {
        "task": "image_captioning",
        "modalities": ["vision", "text"],
        "size": "5k images",
        "url": "https://cocodataset.org/"
    },
    "Flickr30k": {
        "task": "image_captioning",
        "modalities": ["vision", "text"],
        "size": "31k images",
        "url": "https://shannon.cs.illinois.edu/DenotationGraph/"
    },
    "VQAv2": {
        "task": "visual_question_answering",
        "modalities": ["vision", "text"],
        "size": "1.1M questions",
        "url": "https://visualqa.org/"
    },
    "HELM": {
        "task": "holistic_evaluation",
        "modalities": ["text", "vision", "code"],
        "size": "42 scenarios",
        "url": "https://crfm.stanford.edu/helm/"
    },
    "MMLU": {
        "task": "multitask_understanding",
        "modalities": ["text"],
        "size": "57 subjects",
        "url": "https://github.com/hendrycks/test"
    }
}


def create_multimodal_example():
    """
    Create example multi-modal evaluation data.
    
    Useful for testing and demonstrations.
    """
    
    # Simulate GPT-4V evaluation across 5 time periods
    T = 5
    K = 3  # 3 models: GPT-4V, LLaVA, CLIP
    
    # Text performance (accuracy on text-only tasks)
    text_perf = np.array([
        [0.85, 0.78, 0.72],
        [0.87, 0.80, 0.73],
        [0.89, 0.82, 0.75],
        [0.91, 0.84, 0.77],
        [0.93, 0.86, 0.79]
    ])
    
    # Vision performance (CLIP scores)
    vision_perf = np.array([
        [0.82, 0.88, 0.92],
        [0.84, 0.89, 0.93],
        [0.86, 0.90, 0.94],
        [0.88, 0.91, 0.95],
        [0.90, 0.92, 0.96]
    ])
    
    # Multi-modal constraints
    constraints = MultiModalConstraintMatrix("multi_modal")
    
    for t in range(T):
        constraints.add_multimodal_constraints(
            text_max_tokens=512 + t * 50,
            image_resolution=(224 + t * 10, 224 + t * 10),
            temperature=0.7 + t * 0.05,
            inference_time_ms=100 + t * 20,
            memory_gb=8.0 + t * 0.5
        )
    
    return {
        'text_performance': text_perf,
        'vision_performance': vision_perf,
        'constraints': constraints,
        'algorithm_names': ['GPT-4V', 'LLaVA-1.5', 'CLIP-ViT-L/14']
    }
