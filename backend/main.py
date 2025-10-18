"""
Sleuth v1.2 - FastAPI Backend
REST API for AI Bias Detection

Features:
- /api/v1/detect - Bias detection endpoint
- /api/v1/report - PDF report generation
- API key authentication
- Rate limiting
- Usage tracking
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import numpy as np
from datetime import datetime
import hashlib
import secrets

# Import our bias detector
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from circular_bias_detector import BiasDetector

# Initialize FastAPI
app = FastAPI(
    title="Sleuth API",
    description="REST API for AI Evaluation Bias Detection",
    version="1.2.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hongping-zh.github.io",
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Data Models
# ============================================================================

class DetectionRequest(BaseModel):
    """Request model for bias detection"""
    performance_matrix: List[List[float]] = Field(
        ...,
        description="Performance data (T×K matrix)",
        example=[[0.85, 0.78], [0.87, 0.80], [0.91, 0.84]]
    )
    constraint_matrix: List[List[float]] = Field(
        ...,
        description="Constraint data (T×p matrix)",
        example=[[512, 0.7], [550, 0.75], [600, 0.8]]
    )
    algorithm_names: Optional[List[str]] = Field(
        None,
        description="Algorithm names",
        example=["ModelA", "ModelB"]
    )
    psi_threshold: float = Field(0.15, ge=0, le=1)
    ccs_threshold: float = Field(0.85, ge=0, le=1)
    rho_pc_threshold: float = Field(0.5, ge=0, le=1)


class DetectionResponse(BaseModel):
    """Response model for bias detection"""
    has_bias: bool
    risk_level: str  # 'low', 'medium', 'high', 'critical'
    confidence: str  # 'low', 'medium', 'high'
    recommendation: str
    details: dict
    timestamp: str
    processing_time_ms: float


class LLMQuickScanRequest(BaseModel):
    """Request for LLM quick scan"""
    model_id: str = Field(
        ...,
        description="HuggingFace model ID",
        example="gpt2"
    )
    benchmark: Optional[str] = Field(
        "glue",
        description="Benchmark name",
        example="glue"
    )


class ReportRequest(BaseModel):
    """Request for PDF report generation"""
    detection_result: dict
    format: str = Field("pdf", description="Output format: pdf, json, html")
    branding: Optional[dict] = Field(None, description="Custom branding")


class APIKeyResponse(BaseModel):
    """Response for API key generation"""
    api_key: str
    tier: str  # 'free', 'pro', 'enterprise'
    usage_limit: int
    created_at: str


class UsageResponse(BaseModel):
    """Response for usage statistics"""
    tier: str
    usage_count: int
    usage_limit: int
    remaining: int
    reset_date: str


# ============================================================================
# Simple In-Memory Storage (TODO: Replace with database)
# ============================================================================

# API Keys storage
api_keys_db = {
    "demo_free_key_12345": {
        "tier": "free",
        "usage_count": 0,
        "usage_limit": 5,
        "created_at": datetime.now().isoformat()
    }
}

# Usage tracking
usage_db = {}


# ============================================================================
# Authentication
# ============================================================================

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify API key and check quota"""
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required. Get yours at https://is.gd/check_sleuth"
        )
    
    if x_api_key not in api_keys_db:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    key_info = api_keys_db[x_api_key]
    
    # Check usage limit
    if key_info["usage_count"] >= key_info["usage_limit"]:
        raise HTTPException(
            status_code=429,
            detail=f"Usage limit exceeded. Upgrade to Pro: https://is.gd/check_sleuth"
        )
    
    return x_api_key


def increment_usage(api_key: str):
    """Increment usage count for API key"""
    if api_key in api_keys_db:
        api_keys_db[api_key]["usage_count"] += 1


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """API root - redirect to docs"""
    return {
        "message": "Welcome to Sleuth API v1.2",
        "docs": "/api/docs",
        "website": "https://is.gd/check_sleuth",
        "github": "https://github.com/hongping-zh/circular-bias-detection"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.2.0",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/v1/detect", response_model=DetectionResponse)
async def detect_bias(
    request: DetectionRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Detect circular reasoning bias in AI evaluation data
    
    **Required:** API key in `X-API-Key` header
    
    **Free tier:** 5 requests/month  
    **Pro tier:** Unlimited requests
    
    **Example:**
    ```bash
    curl -X POST "https://api.sleuth.ai/api/v1/detect" \\
         -H "X-API-Key: your-api-key" \\
         -H "Content-Type: application/json" \\
         -d '{
           "performance_matrix": [[0.85, 0.78], [0.87, 0.80]],
           "constraint_matrix": [[512, 0.7], [550, 0.75]]
         }'
    ```
    """
    start_time = datetime.now()
    
    try:
        # Convert to numpy arrays
        performance = np.array(request.performance_matrix)
        constraints = np.array(request.constraint_matrix)
        
        # Validate shapes
        if len(performance.shape) != 2 or len(constraints.shape) != 2:
            raise HTTPException(
                status_code=400,
                detail="Matrices must be 2-dimensional"
            )
        
        if performance.shape[0] != constraints.shape[0]:
            raise HTTPException(
                status_code=400,
                detail="Performance and constraint matrices must have same number of rows (time periods)"
            )
        
        # Run bias detection
        detector = BiasDetector(
            psi_threshold=request.psi_threshold,
            ccs_threshold=request.ccs_threshold,
            rho_pc_threshold=request.rho_pc_threshold
        )
        
        result = detector.detect_bias(
            performance_matrix=performance,
            constraint_matrix=constraints,
            algorithm_names=request.algorithm_names
        )
        
        # Convert BiasDetector result to API response format
        has_bias = result['overall_bias']
        confidence_value = result['confidence']
        
        # Determine risk level based on bias votes
        bias_votes = result.get('bias_votes', 0)
        if bias_votes >= 3:
            risk_level = 'critical'
        elif bias_votes == 2:
            risk_level = 'high'
        elif bias_votes == 1:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        # Determine confidence label
        if confidence_value >= 0.7:
            confidence = 'high'
        elif confidence_value >= 0.4:
            confidence = 'medium'
        else:
            confidence = 'low'
        
        # Generate recommendation
        if has_bias:
            issues = []
            if result.get('psi_bias'):
                issues.append("Lock hyperparameters")
            if result.get('ccs_bias'):
                issues.append("Use consistent evaluation constraints")
            if result.get('rho_pc_bias'):
                issues.append("Ensure performance doesn't depend on resource changes")
            recommendation = f"⚠️ Bias detected. Recommendations: {', '.join(issues)}"
        else:
            recommendation = "✅ No bias detected. Evaluation appears sound."
        
        # Build details
        details = {
            'psi': {
                'value': round(result['psi_score'], 4),
                'threshold': request.psi_threshold,
                'status': 'fail' if result.get('psi_bias') else 'pass',
                'meaning': 'Parameters changed during evaluation' if result.get('psi_bias') else 'Parameters stable'
            },
            'ccs': {
                'value': round(result['ccs_score'], 4),
                'threshold': request.ccs_threshold,
                'status': 'fail' if result.get('ccs_bias') else 'pass',
                'meaning': 'Constraints inconsistent' if result.get('ccs_bias') else 'Constraints consistent'
            },
            'rho_pc': {
                'value': round(result['rho_pc_score'], 4),
                'threshold': request.rho_pc_threshold,
                'status': 'fail' if result.get('rho_pc_bias') else 'pass',
                'meaning': 'Performance depends on constraints' if result.get('rho_pc_bias') else 'Performance independent'
            },
            'metadata': result.get('metadata', {})
        }
        
        # Increment usage
        increment_usage(api_key)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return DetectionResponse(
            has_bias=has_bias,
            risk_level=risk_level,
            confidence=confidence,
            recommendation=recommendation,
            details=details,
            timestamp=datetime.now().isoformat(),
            processing_time_ms=round(processing_time, 2)
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/api/v1/llm-quick-scan")
async def llm_quick_scan(
    request: LLMQuickScanRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Quick bias scan for LLM evaluations (30 seconds)
    
    Automatically fetches model metadata from HuggingFace and analyzes
    common bias patterns in LLM benchmarks.
    
    **Status:** 🚧 Coming soon in v1.2
    """
    # TODO: Implement LLM quick scan
    # - Fetch model from HuggingFace
    # - Extract evaluation history
    # - Detect prompt engineering bias
    # - Check sampling parameter stability
    
    increment_usage(api_key)
    
    return {
        "status": "coming_soon",
        "message": "LLM Quick Scan will be available in v1.2",
        "eta": "2 weeks",
        "model_id": request.model_id,
        "subscribe": "https://is.gd/check_sleuth"
    }


@app.post("/api/v1/report")
async def generate_report(
    request: ReportRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Generate professional PDF report
    
    **Status:** 🚧 Coming soon in v1.2
    """
    # TODO: Implement PDF report generation
    # - Use ReportLab
    # - Custom branding
    # - Multiple templates
    
    increment_usage(api_key)
    
    return {
        "status": "coming_soon",
        "message": "PDF Report generation will be available in v1.2",
        "eta": "3 weeks"
    }


@app.post("/api/v1/keys/generate", response_model=APIKeyResponse)
async def generate_api_key(email: str, tier: str = "free"):
    """
    Generate new API key
    
    **Note:** In production, this would require email verification
    and payment processing for Pro/Enterprise tiers.
    """
    # Generate secure API key
    raw_key = secrets.token_urlsafe(32)
    api_key = f"sk_{tier}_{raw_key}"
    
    # Set usage limit based on tier
    limits = {
        "free": 5,
        "pro": 9999,
        "enterprise": 999999
    }
    
    # Store in database
    api_keys_db[api_key] = {
        "tier": tier,
        "usage_count": 0,
        "usage_limit": limits.get(tier, 5),
        "email": email,
        "created_at": datetime.now().isoformat()
    }
    
    return APIKeyResponse(
        api_key=api_key,
        tier=tier,
        usage_limit=limits.get(tier, 5),
        created_at=datetime.now().isoformat()
    )


@app.get("/api/v1/usage", response_model=UsageResponse)
async def get_usage(api_key: str = Depends(verify_api_key)):
    """Get usage statistics for API key"""
    key_info = api_keys_db[api_key]
    
    return UsageResponse(
        tier=key_info["tier"],
        usage_count=key_info["usage_count"],
        usage_limit=key_info["usage_limit"],
        remaining=key_info["usage_limit"] - key_info["usage_count"],
        reset_date="2024-12-01"  # TODO: Implement monthly reset
    )


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat(),
            "docs": "https://api.sleuth.ai/docs"
        }
    )


# ============================================================================
# Lifespan Events (FastAPI 0.93+)
# ============================================================================

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    print("🚀 Sleuth API v1.2 starting...")
    print("📖 API docs: http://localhost:8000/api/docs")
    print("🔑 Demo API key: demo_free_key_12345")
    
    yield
    
    # Shutdown
    print("👋 Sleuth API shutting down...")

# Apply lifespan to app
app.router.lifespan_context = lifespan


# ============================================================================
# Run (for development)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
