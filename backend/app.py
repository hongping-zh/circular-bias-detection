"""
Flask API for Circular Bias Detection

Provides RESTful API endpoints for the Sleuth bias detection service.

Endpoints:
- POST /api/detect: Main bias detection endpoint
- POST /api/analyze_zenodo: Analyze Zenodo dataset
- GET /api/zenodo/summary: Get Zenodo dataset summary
- GET /health: Health check
- GET /api/info: API information
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from io import StringIO
import traceback

from core.bias_scorer import detect_circular_bias
from core.integration_service import IntegrationService

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for web app integration

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize integration service
integration_service = IntegrationService(doi="10.5281/zenodo.17201032")


@app.route('/', methods=['GET'])
def welcome():
    """
    Welcome page with API navigation.
    
    Returns:
        HTML welcome page with links to API endpoints
    """
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sleuth API - Zenodo Integration</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                padding: 40px;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 15px;
                margin-top: 0;
            }
            h2 {
                color: #34495e;
                margin-top: 30px;
            }
            .endpoint {
                background: #f8f9fa;
                border-left: 4px solid #3498db;
                padding: 15px;
                margin: 15px 0;
                border-radius: 4px;
            }
            .method {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
                margin-right: 10px;
            }
            .get { background: #28a745; color: white; }
            .post { background: #007bff; color: white; }
            .endpoint-path {
                font-family: 'Courier New', monospace;
                color: #e83e8c;
                font-weight: bold;
            }
            .description {
                color: #6c757d;
                margin-top: 8px;
            }
            .try-it {
                background: #3498db;
                color: white;
                padding: 8px 16px;
                text-decoration: none;
                border-radius: 4px;
                display: inline-block;
                margin-top: 8px;
                font-size: 14px;
            }
            .try-it:hover {
                background: #2980b9;
            }
            .badge {
                background: #e74c3c;
                color: white;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: bold;
                margin-left: 8px;
            }
            .info-box {
                background: #e8f4fd;
                border: 1px solid #bee5eb;
                border-radius: 4px;
                padding: 15px;
                margin: 20px 0;
            }
            code {
                background: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Sleuth API - Zenodo Integration</h1>
            <p style="font-size: 18px; color: #555;">
                循环偏差检测服务 + Zenodo 数据集集成
            </p>
            
            <div class="info-box">
                <strong>📊 服务状态:</strong> 运行中<br>
                <strong>🔗 Zenodo DOI:</strong> <code>10.5281/zenodo.17201032</code><br>
                <strong>📖 文档:</strong> 查看 <code>backend/START_HERE.md</code>
            </div>

            <h2>🔌 API 端点</h2>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <span class="endpoint-path">/api/analyze_zenodo</span>
                <span class="badge">新增</span>
                <div class="description">
                    分析 Zenodo 数据集 - 自动获取数据并运行 Sleuth 偏差检测
                </div>
                <a href="#" class="try-it" onclick="tryAnalyze(); return false;">试用</a>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/api/zenodo/summary</span>
                <span class="badge">新增</span>
                <div class="description">
                    获取 Zenodo 数据集摘要信息
                </div>
                <a href="/api/zenodo/summary" class="try-it" target="_blank">查看</a>
            </div>

            <div class="endpoint">
                <span class="method post">POST</span>
                <span class="endpoint-path">/api/detect</span>
                <div class="description">
                    使用自定义 CSV 数据进行偏差检测
                </div>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/api/info</span>
                <div class="description">
                    完整的 API 信息和文档
                </div>
                <a href="/api/info" class="try-it" target="_blank">查看</a>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/health</span>
                <div class="description">
                    健康检查
                </div>
                <a href="/health" class="try-it" target="_blank">查看</a>
            </div>

            <h2>📚 快速开始</h2>
            <p>使用 cURL 测试 API：</p>
            <code style="display: block; padding: 12px; background: #2c3e50; color: #ecf0f1; border-radius: 4px; margin: 10px 0;">
                curl -X POST http://localhost:5000/api/analyze_zenodo -H "Content-Type: application/json" -d '{}'
            </code>

            <h2>🔗 更多资源</h2>
            <ul style="line-height: 2;">
                <li><strong>快速入门:</strong> <code>backend/START_HERE.md</code></li>
                <li><strong>完整文档:</strong> <code>backend/ZENODO_INTEGRATION_GUIDE.md</code></li>
                <li><strong>测试脚本:</strong> <code>python test_zenodo_integration.py</code></li>
                <li><strong>示例代码:</strong> <code>python example_usage.py</code></li>
            </ul>
        </div>

        <script>
            function tryAnalyze() {
                if (confirm('这将调用 /api/analyze_zenodo 端点。\\n\\n处理可能需要几秒钟，确定继续吗？')) {
                    fetch('/api/analyze_zenodo', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({})
                    })
                    .then(response => response.json())
                    .then(data => {
                        alert('分析完成！\\n\\nCBS Score: ' + data.sleuth_analysis.cbs_score.toFixed(4) + 
                              '\\nBias Detected: ' + data.sleuth_analysis.bias_detected +
                              '\\n\\n详细结果已在浏览器控制台输出');
                        console.log('分析结果:', data);
                    })
                    .catch(error => {
                        alert('错误: ' + error);
                        console.error('错误:', error);
                    });
                }
            }
        </script>
    </body>
    </html>
    """
    return html


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
                    'csv_data': 'time_period,algorithm,performance,constraint_compute\n1,A,0.7,100',
                    'run_bootstrap': False
                }
            },
            '/api/analyze_zenodo': {
                'method': 'POST',
                'description': 'Fetch data from Zenodo and run bias detection',
                'parameters': {
                    'file_key': 'String, specific file to analyze (optional, defaults to first CSV)',
                    'run_bootstrap': 'Boolean, run bootstrap CI (optional, default: false)',
                    'n_bootstrap': 'Integer, number of bootstrap iterations (optional, default: 1000)',
                    'weights': 'Array of 3 floats, weights for PSI/CCS/ρ_PC (optional, default: [0.33, 0.33, 0.34])',
                    'use_cache': 'Boolean, use cached results (optional, default: true)'
                }
            },
            '/api/zenodo/summary': {
                'method': 'GET',
                'description': 'Get summary information about the Zenodo dataset'
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


@app.route('/api/analyze_zenodo', methods=['POST'])
def analyze_zenodo():
    """
    Analyze Zenodo dataset endpoint.
    
    Fetches data from Zenodo and runs Sleuth bias detection.
    
    Request Body (JSON):
        {
            "file_key": "<filename>" (optional),
            "run_bootstrap": false (optional),
            "n_bootstrap": 1000 (optional),
            "weights": [0.33, 0.33, 0.34] (optional),
            "use_cache": true (optional)
        }
    
    Returns:
        200 OK with integrated analysis results
        400 Bad Request if parameters are invalid
        500 Internal Server Error if processing fails
    """
    
    try:
        # Parse request (can be empty JSON)
        data = {}
        if request.is_json:
            data = request.get_json()
        
        # Extract parameters
        file_key = data.get('file_key', None)
        run_bootstrap = data.get('run_bootstrap', False)
        n_bootstrap = data.get('n_bootstrap', 1000)
        weights = data.get('weights', [0.33, 0.33, 0.34])
        use_cache = data.get('use_cache', True)
        
        print(f"📥 Zenodo integration request: file_key={file_key}, bootstrap={run_bootstrap}")
        
        # Run integration
        results = integration_service.analyze_zenodo_dataset(
            file_key=file_key,
            weights=weights,
            run_bootstrap=run_bootstrap,
            n_bootstrap=n_bootstrap,
            use_cache=use_cache
        )
        
        print(f"✅ Zenodo analysis complete")
        
        return jsonify(results), 200
    
    except ValueError as e:
        print(f"⚠️  Validation error: {str(e)}")
        return jsonify({
            'error': 'Validation error',
            'details': str(e)
        }), 400
    
    except Exception as e:
        print(f"❌ Error processing Zenodo request: {str(e)}")
        traceback.print_exc()
        
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


@app.route('/api/zenodo/summary', methods=['GET'])
def zenodo_summary():
    """
    Get Zenodo dataset summary.
    
    Returns:
        200 OK with dataset summary
        500 Internal Server Error if fetch fails
    """
    
    try:
        print(f"📥 Fetching Zenodo summary...")
        
        summary = integration_service.get_zenodo_summary()
        
        print(f"✅ Summary retrieved")
        
        return jsonify(summary), 200
    
    except Exception as e:
        print(f"❌ Error fetching Zenodo summary: {str(e)}")
        traceback.print_exc()
        
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """
    Clear the analysis cache.
    
    Returns:
        200 OK with confirmation
    """
    try:
        integration_service.clear_cache()
        return jsonify({
            'status': 'success',
            'message': 'Cache cleared successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to clear cache',
            'details': str(e)
        }), 500


# CLI runner
if __name__ == '__main__':
    print("=" * 70)
    print("🚀 Starting Sleuth API Server with Zenodo Integration")
    print("=" * 70)
    print("\nEndpoints:")
    print("  GET  /health                - Health check")
    print("  GET  /api/info              - API information")
    print("  POST /api/detect            - Bias detection (custom data)")
    print("  POST /api/analyze_zenodo    - Analyze Zenodo dataset")
    print("  GET  /api/zenodo/summary    - Zenodo dataset summary")
    print("  POST /api/cache/clear       - Clear results cache")
    print("\nZenodo Dataset: DOI 10.5281/zenodo.17201032")
    print("Server running on: http://localhost:5000")
    print("=" * 70)
    print("\nPress Ctrl+C to stop\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
