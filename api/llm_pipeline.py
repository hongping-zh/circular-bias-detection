"""
LLM Pipeline Integration for Automated Bias Detection

Enables users to run LLM evaluations directly from the Web App.
Uses Hugging Face Transformers for model loading and GLUE for benchmarking.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List, Dict
import numpy as np
from datetime import datetime
import asyncio
import logging

# Optional imports (install when needed)
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    from datasets import load_dataset
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    logging.warning("transformers and datasets not installed. Install with: pip install transformers datasets torch")

from circular_bias_detector import BiasDetector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Sleuth LLM Pipeline API",
    description="Automated LLM bias detection via Hugging Face integration",
    version="1.2.0"
)

# Request/Response Models
class LLMScanRequest(BaseModel):
    """Request model for LLM scan"""
    model_id: str  # e.g., "gpt2", "bert-base-uncased"
    task: str = "text-classification"  # transformers task type
    dataset: str = "glue/sst2"  # GLUE dataset
    n_iterations: int = 5  # Number of evaluation runs
    prompt_template: Optional[str] = None  # Custom prompt
    few_shot_examples: Optional[List[Dict]] = None
    constraints: Optional[Dict] = {
        "max_tokens": 512,
        "temperature": 0.7,
        "batch_size": 32
    }

class LLMScanResponse(BaseModel):
    """Response model for LLM scan"""
    status: str
    performance_matrix: List[List[float]]
    constraint_matrix: List[List[float]]
    bias_results: Dict
    execution_time: float
    model_info: Dict
    warnings: Optional[List[str]] = []

class ScanStatus(BaseModel):
    """Scan status for async tracking"""
    scan_id: str
    status: str  # "pending", "running", "completed", "failed"
    progress: float  # 0.0 to 1.0
    message: str

# In-memory storage (replace with Redis in production)
scan_results = {}
scan_statuses = {}


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "service": "Sleuth LLM Pipeline API",
        "version": "1.2.0",
        "status": "operational",
        "transformers_available": HAS_TRANSFORMERS
    }


@app.post("/api/llm-scan", response_model=LLMScanResponse)
async def create_llm_scan(request: LLMScanRequest, background_tasks: BackgroundTasks):
    """
    Run automated LLM bias detection scan.
    
    This endpoint:
    1. Loads the specified model from Hugging Face
    2. Runs evaluation on GLUE dataset
    3. Generates performance/constraint time series
    4. Computes bias indicators
    5. Returns comprehensive results
    """
    
    if not HAS_TRANSFORMERS:
        raise HTTPException(
            status_code=501,
            detail="Transformers library not installed. Install with: pip install transformers datasets torch"
        )
    
    logger.info(f"Starting LLM scan for model: {request.model_id}")
    
    try:
        start_time = datetime.now()
        
        # Step 1: Load model and tokenizer
        logger.info("Loading model and tokenizer...")
        model_pipeline = pipeline(
            request.task,
            model=request.model_id,
            tokenizer=request.model_id,
            device=-1  # CPU, change to 0 for GPU
        )
        
        # Step 2: Load dataset
        logger.info(f"Loading dataset: {request.dataset}")
        dataset_name, subset = request.dataset.split('/')
        dataset = load_dataset(dataset_name, subset, split='validation[:100]')  # Limit for speed
        
        # Step 3: Run multiple evaluation iterations
        logger.info(f"Running {request.n_iterations} evaluation iterations...")
        performance_matrix = []
        constraint_matrix = []
        
        for iteration in range(request.n_iterations):
            # Simulate parameter variations across iterations
            max_tokens = request.constraints['max_tokens'] + iteration * 10
            temperature = request.constraints['temperature'] + iteration * 0.05
            
            # Run evaluation
            predictions = []
            for example in dataset:
                text = example['sentence']
                result = model_pipeline(text[:max_tokens])[0]
                predictions.append(result['score'])
            
            # Compute performance metric (average confidence)
            performance = np.mean(predictions)
            performance_matrix.append([performance])
            
            # Record constraints
            constraint_matrix.append([
                max_tokens,
                temperature,
                request.constraints['batch_size']
            ])
            
            logger.info(f"Iteration {iteration+1}/{request.n_iterations}: performance={performance:.4f}")
        
        # Convert to numpy arrays
        performance_matrix = np.array(performance_matrix)
        constraint_matrix = np.array(constraint_matrix)
        
        # Step 4: Run bias detection
        logger.info("Computing bias indicators...")
        detector = BiasDetector(
            psi_threshold=0.15,
            ccs_threshold=0.85,
            rho_pc_threshold=0.5
        )
        
        bias_results = detector.detect_bias(
            performance_matrix=performance_matrix,
            constraint_matrix=constraint_matrix,
            algorithm_names=[request.model_id],
            enable_bootstrap=True,
            n_bootstrap=1000
        )
        
        # Step 5: Prepare response
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Clean results for JSON serialization
        cleaned_results = {}
        for key, value in bias_results.items():
            if isinstance(value, (np.integer, np.floating)):
                cleaned_results[key] = float(value)
            elif key != 'metadata':
                cleaned_results[key] = value
        
        response = LLMScanResponse(
            status="success",
            performance_matrix=performance_matrix.tolist(),
            constraint_matrix=constraint_matrix.tolist(),
            bias_results=cleaned_results,
            execution_time=execution_time,
            model_info={
                "model_id": request.model_id,
                "task": request.task,
                "dataset": request.dataset,
                "n_iterations": request.n_iterations
            },
            warnings=[]
        )
        
        logger.info(f"LLM scan completed in {execution_time:.2f}s")
        return response
        
    except Exception as e:
        logger.error(f"LLM scan failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")


@app.post("/api/llm-scan/async")
async def create_llm_scan_async(request: LLMScanRequest):
    """
    Start async LLM scan (for long-running evaluations).
    Returns scan_id for status tracking.
    """
    import uuid
    
    scan_id = str(uuid.uuid4())
    
    # Initialize status
    scan_statuses[scan_id] = ScanStatus(
        scan_id=scan_id,
        status="pending",
        progress=0.0,
        message="Scan queued"
    )
    
    # TODO: Implement async processing with Celery or similar
    
    return {
        "scan_id": scan_id,
        "status": "pending",
        "check_status_url": f"/api/llm-scan/status/{scan_id}"
    }


@app.get("/api/llm-scan/status/{scan_id}", response_model=ScanStatus)
async def get_scan_status(scan_id: str):
    """Get status of async scan"""
    if scan_id not in scan_statuses:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return scan_statuses[scan_id]


@app.get("/api/models/supported")
async def get_supported_models():
    """
    Get list of recommended models for quick scanning.
    """
    return {
        "text_classification": [
            {
                "model_id": "distilbert-base-uncased-finetuned-sst-2-english",
                "description": "DistilBERT for sentiment analysis (fast)",
                "size": "~250MB",
                "recommended": True
            },
            {
                "model_id": "bert-base-uncased",
                "description": "BERT base model",
                "size": "~440MB",
                "recommended": True
            },
            {
                "model_id": "roberta-base",
                "description": "RoBERTa base model",
                "size": "~500MB",
                "recommended": False
            }
        ],
        "text_generation": [
            {
                "model_id": "gpt2",
                "description": "GPT-2 base (124M params)",
                "size": "~500MB",
                "recommended": True
            },
            {
                "model_id": "distilgpt2",
                "description": "Distilled GPT-2 (faster)",
                "size": "~350MB",
                "recommended": True
            }
        ]
    }


@app.get("/api/datasets/supported")
async def get_supported_datasets():
    """
    Get list of supported GLUE datasets.
    """
    return {
        "glue": [
            {
                "name": "glue/sst2",
                "description": "Stanford Sentiment Treebank",
                "task": "sentiment classification",
                "size": "67k examples"
            },
            {
                "name": "glue/cola",
                "description": "Corpus of Linguistic Acceptability",
                "task": "grammatical correctness",
                "size": "8.5k examples"
            },
            {
                "name": "glue/mrpc",
                "description": "Microsoft Research Paraphrase Corpus",
                "task": "paraphrase detection",
                "size": "3.7k examples"
            },
            {
                "name": "glue/qqp",
                "description": "Quora Question Pairs",
                "task": "duplicate detection",
                "size": "363k examples"
            }
        ]
    }


# Example usage function (for testing)
async def example_usage():
    """
    Example of how to use the API programmatically.
    """
    
    # Create scan request
    request = LLMScanRequest(
        model_id="distilbert-base-uncased-finetuned-sst-2-english",
        task="text-classification",
        dataset="glue/sst2",
        n_iterations=5,
        constraints={
            "max_tokens": 512,
            "temperature": 0.7,
            "batch_size": 32
        }
    )
    
    # Run scan
    # result = await create_llm_scan(request, BackgroundTasks())
    # print(result)


if __name__ == "__main__":
    import uvicorn
    
    print("""
    ========================================
    Sleuth LLM Pipeline API
    ========================================
    
    Starting server on http://localhost:8000
    
    API Endpoints:
    - GET  /                       - Health check
    - POST /api/llm-scan          - Run LLM bias scan
    - POST /api/llm-scan/async    - Start async scan
    - GET  /api/llm-scan/status/{id} - Check scan status
    - GET  /api/models/supported  - List recommended models
    - GET  /api/datasets/supported - List GLUE datasets
    
    Interactive docs: http://localhost:8000/docs
    ========================================
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
