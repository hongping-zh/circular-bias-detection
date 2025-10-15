"""
Flask API for Circular Bias Detection

Provides RESTful API endpoints for the Sleuth bias detection service.

Endpoints:
- POST /api/detect: Main bias detection endpoint
- GET /health: Health check
- GET /api/info: API information
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from io import StringIO
import traceback

from core.bias_scorer import detect_circular_bias

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for web app integration

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    
    Returns:
        200 OK with status message
    """
    return jsonify({
        'status': 'ok',
        'service': 'Sleuth Bias Detection API',
        'version': '1.0.0'
    }), 200


@app.route('/api/info', methods=['GET'])
def api_info():
    """
    API information endpoint.
    
    Returns:
        API documentation and usage information
    """
    return jsonify({
        'name': 'Sleuth - Circular Bias Detection API',
        'version': '1.0.0',
        'endpoints': {
            '/health': {
                'method': 'GET',
                'description': 'Health check'
            },
            '/api/info': {
                'method': 'GET',
                'description': 'API information'
            },
            '/api/detect': {
                'method': 'POST',
                'description': 'Detect circular bias in evaluation data',
                'parameters': {
                    'csv_data': 'CSV string with evaluation data (required)',
                    'run_bootstrap': 'Boolean, run bootstrap CI (optional, default: false)',
                    'n_bootstrap': 'Integer, number of bootstrap iterations (optional, default: 1000)',
                    'weights': 'Array of 3 floats, weights for PSI/CCS/ρ_PC (optional, default: [0.33, 0.33, 0.34])'
                },
                'example': {
                    'csv_data': 'time_period,algorithm,performance,constraint_compute\\n1,A,0.7,100',
                    'run_bootstrap': False
                }
            }
        },
        'required_columns': [
            'time_period',
            'algorithm',
            'performance',
            'constraint_* (at least one)'
        ],
        'documentation': 'https://github.com/hongping-zh/circular-bias-detection'
    }), 200


@app.route('/api/detect', methods=['POST'])
def detect_bias():
    """
    Main bias detection endpoint.
    
    Accepts CSV data and returns bias detection results.
    
    Request Body (JSON):
        {
            "csv_data": "<CSV string>",
            "run_bootstrap": false (optional),
            "n_bootstrap": 1000 (optional),
            "weights": [0.33, 0.33, 0.34] (optional)
        }
    
    Returns:
        200 OK with bias detection results
        400 Bad Request if data is invalid
        500 Internal Server Error if processing fails
    """
    
    try:
        # Parse request
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        
        # Validate required fields
        if 'csv_data' not in data:
            return jsonify({
                'error': 'Missing required field: csv_data'
            }), 400
        
        csv_data = data['csv_data']
        run_bootstrap = data.get('run_bootstrap', False)
        n_bootstrap = data.get('n_bootstrap', 1000)
        weights = data.get('weights', [0.33, 0.33, 0.34])
        
        # Parse CSV
        try:
            df = pd.read_csv(StringIO(csv_data))
        except Exception as e:
            return jsonify({
                'error': 'Failed to parse CSV data',
                'details': str(e)
            }), 400
        
        # Validate data
        validation_error = _validate_data(df)
        if validation_error:
            return jsonify({
                'error': 'Invalid data',
                'details': validation_error
            }), 400
        
        # Run bias detection
        print(f"📥 Received request: {len(df)} rows, bootstrap={run_bootstrap}")
        
        results = detect_circular_bias(
            df,
            weights=weights,
            run_bootstrap=run_bootstrap,
            n_bootstrap=n_bootstrap
        )
        
        print(f"✅ Detection complete: CBS={results['cbs_score']:.3f}, Bias={results['bias_detected']}")
        
        # Return results
        return jsonify(results), 200
    
    except Exception as e:
        # Log error
        print(f"❌ Error processing request: {str(e)}")
        traceback.print_exc()
        
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


def _validate_data(df: pd.DataFrame) -> str:
    """
    Validate input data format.
    
    Args:
        df: DataFrame to validate
    
    Returns:
        Error message string if invalid, None if valid
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
    
    # Check data types and ranges
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


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'error': 'File too large',
        'details': 'Maximum file size is 16MB'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'details': 'The requested endpoint does not exist. See /api/info for available endpoints.'
    }), 404


# CLI runner
if __name__ == '__main__':
    print("=" * 70)
    print("🚀 Starting Sleuth API Server")
    print("=" * 70)
    print("\nEndpoints:")
    print("  GET  /health       - Health check")
    print("  GET  /api/info     - API information")
    print("  POST /api/detect   - Bias detection")
    print("\nServer running on: http://localhost:5000")
    print("=" * 70)
    print("\nPress Ctrl+C to stop\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
