# Zenodo Integration Guide

本指南说明如何使用 Sleuth API 与 Zenodo 数据集 (DOI: 10.5281/zenodo.17201032) 的集成功能。

## 概述

集成服务将 Zenodo 数据仓库与 Sleuth 循环偏差检测分析引擎结合，实现：

1. **自动数据获取**：从 Zenodo 自动下载数据集
2. **智能分析**：使用 Sleuth 引擎分析数据集的循环偏差
3. **结果整合**：将数据源信息与分析结果整合返回
4. **缓存机制**：自动缓存分析结果，避免重复计算

## 架构设计

```
用户请求
    ↓
API端点 (/api/analyze_zenodo)
    ↓
IntegrationService (集成服务)
    ↓
    ├─→ ZenodoClient (获取数据)
    │       ↓
    │   Zenodo API
    │
    └─→ detect_circular_bias (分析引擎)
            ↓
        返回整合结果
```

## 安装和运行

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动服务器

```bash
python app.py
```

服务器将在 `http://localhost:5000` 启动。

## API 端点

### 1. 分析 Zenodo 数据集

**端点**: `POST /api/analyze_zenodo`

**描述**: 从 Zenodo 获取数据并运行循环偏差检测分析。

**请求体** (JSON, 所有参数可选):

```json
{
  "file_key": "dataset.csv",
  "run_bootstrap": false,
  "n_bootstrap": 1000,
  "weights": [0.33, 0.33, 0.34],
  "use_cache": true
}
```

**参数说明**:
- `file_key` (可选): 指定要分析的文件名。若不指定，自动选择第一个 CSV 文件
- `run_bootstrap` (可选, 默认: false): 是否运行 Bootstrap 置信区间计算
- `n_bootstrap` (可选, 默认: 1000): Bootstrap 迭代次数
- `weights` (可选, 默认: [0.33, 0.33, 0.34]): PSI/CCS/ρ_PC 指标权重
- `use_cache` (可选, 默认: true): 是否使用缓存结果

**响应示例**:

```json
{
  "source_data": {
    "doi": "10.5281/zenodo.17201032",
    "record_id": "17201032",
    "title": "Dataset Title",
    "creators": ["Author Name"],
    "publication_date": "2024-01-01",
    "description": "Dataset description...",
    "license": "cc-by-4.0",
    "access_right": "open"
  },
  "dataset_info": {
    "rows": 100,
    "columns": 5,
    "column_names": ["time_period", "algorithm", "performance", "constraint_compute", "constraint_memory"],
    "algorithms": ["A", "B", "C"],
    "time_periods": [1, 2, 3, 4, 5],
    "performance_range": {
      "min": 0.45,
      "max": 0.95,
      "mean": 0.72
    }
  },
  "sleuth_analysis": {
    "cbs_score": 0.156,
    "bias_detected": false,
    "metrics": {
      "psi": 0.234,
      "ccs": 0.123,
      "rho_pc": 0.089
    },
    "interpretation": "Low circular bias detected",
    "recommendation": "The evaluation appears relatively unbiased."
  },
  "processing_info": {
    "elapsed_time_seconds": 2.45,
    "timestamp": "2024-10-22 10:30:00",
    "from_cache": false
  }
}
```

**使用示例**:

```bash
# 使用默认参数（最简单）
curl -X POST http://localhost:5000/api/analyze_zenodo \
  -H "Content-Type: application/json" \
  -d '{}'

# 指定文件并运行 Bootstrap
curl -X POST http://localhost:5000/api/analyze_zenodo \
  -H "Content-Type: application/json" \
  -d '{
    "file_key": "evaluation_data.csv",
    "run_bootstrap": true,
    "n_bootstrap": 500
  }'

# 自定义权重
curl -X POST http://localhost:5000/api/analyze_zenodo \
  -H "Content-Type: application/json" \
  -d '{
    "weights": [0.4, 0.3, 0.3]
  }'
```

### 2. 获取 Zenodo 数据集摘要

**端点**: `GET /api/zenodo/summary`

**描述**: 获取 Zenodo 数据集的元数据摘要，不进行分析。

**响应示例**:

```json
{
  "doi": "10.5281/zenodo.17201032",
  "record_id": "17201032",
  "title": "Circular Bias Detection Dataset",
  "creators": ["Author Name"],
  "publication_date": "2024-01-01",
  "description": "A comprehensive dataset for...",
  "keywords": ["bias detection", "machine learning"],
  "files": [
    {
      "key": "dataset.csv",
      "size": 102400,
      "type": "csv"
    }
  ],
  "access_right": "open",
  "license": "cc-by-4.0"
}
```

**使用示例**:

```bash
curl http://localhost:5000/api/zenodo/summary
```

### 3. 清除缓存

**端点**: `POST /api/cache/clear`

**描述**: 清除所有缓存的分析结果。

**响应示例**:

```json
{
  "status": "success",
  "message": "Cache cleared successfully"
}
```

**使用示例**:

```bash
curl -X POST http://localhost:5000/api/cache/clear
```

### 4. 传统检测端点（自定义数据）

**端点**: `POST /api/detect`

**描述**: 使用自定义 CSV 数据进行偏差检测（不使用 Zenodo）。

详见原有文档。

## Python 客户端示例

```python
import requests
import json

# 基础 URL
BASE_URL = "http://localhost:5000"

def analyze_zenodo(file_key=None, run_bootstrap=False):
    """分析 Zenodo 数据集"""
    url = f"{BASE_URL}/api/analyze_zenodo"
    
    payload = {
        "file_key": file_key,
        "run_bootstrap": run_bootstrap
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    return response.json()

def get_zenodo_summary():
    """获取数据集摘要"""
    url = f"{BASE_URL}/api/zenodo/summary"
    response = requests.get(url)
    response.raise_for_status()
    
    return response.json()

# 使用示例
if __name__ == "__main__":
    # 1. 先查看数据集摘要
    print("获取 Zenodo 数据集摘要...")
    summary = get_zenodo_summary()
    print(f"标题: {summary['title']}")
    print(f"文件: {[f['key'] for f in summary['files']]}")
    
    # 2. 运行分析
    print("\n运行偏差分析...")
    results = analyze_zenodo(run_bootstrap=False)
    
    print(f"\nCBS 得分: {results['sleuth_analysis']['cbs_score']:.3f}")
    print(f"检测到偏差: {results['sleuth_analysis']['bias_detected']}")
    print(f"处理时间: {results['processing_info']['elapsed_time_seconds']}秒")
```

## JavaScript/前端示例

```javascript
// 分析 Zenodo 数据集
async function analyzeZenodo(options = {}) {
  const response = await fetch('http://localhost:5000/api/analyze_zenodo', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(options)
  });
  
  if (!response.ok) {
    throw new Error(`API 错误: ${response.statusText}`);
  }
  
  return await response.json();
}

// 获取数据集摘要
async function getZenodoSummary() {
  const response = await fetch('http://localhost:5000/api/zenodo/summary');
  
  if (!response.ok) {
    throw new Error(`API 错误: ${response.statusText}`);
  }
  
  return await response.json();
}

// 使用示例
(async () => {
  try {
    // 获取摘要
    const summary = await getZenodoSummary();
    console.log('数据集标题:', summary.title);
    
    // 运行分析
    const results = await analyzeZenodo({
      run_bootstrap: false,
      use_cache: true
    });
    
    console.log('CBS 得分:', results.sleuth_analysis.cbs_score);
    console.log('检测到偏差:', results.sleuth_analysis.bias_detected);
    
  } catch (error) {
    console.error('错误:', error);
  }
})();
```

## 缓存机制

### 工作原理

集成服务使用内存缓存来存储分析结果：

- **缓存键**: 基于 `file_key`, `weights`, `run_bootstrap`, `n_bootstrap` 生成
- **自动缓存**: 默认启用，可通过 `use_cache=false` 禁用
- **缓存清除**: 调用 `/api/cache/clear` 或重启服务器

### 何时使用缓存

✅ **建议使用**:
- 相同参数的重复查询
- 生产环境中的常规查询
- 需要快速响应时

❌ **建议禁用**:
- 数据集已更新
- 测试不同参数
- 需要最新结果时

## 数据要求

Zenodo 数据集中的 CSV 文件必须包含以下列：

### 必需列
- `time_period`: 时间周期（数值）
- `algorithm`: 算法名称（字符串）
- `performance`: 性能指标（0-1 之间的数值）
- `constraint_*`: 至少一个约束列（例如 `constraint_compute`, `constraint_memory`）

### 数据要求
- 至少 4 行数据
- 至少 2 个不同的算法
- 至少 2 个不同的时间周期
- 性能值在 [0, 1] 范围内

## 错误处理

### 常见错误

**400 Bad Request - 验证错误**
```json
{
  "error": "Validation error",
  "details": "Missing required columns: time_period"
}
```

**500 Internal Server Error - 网络错误**
```json
{
  "error": "Internal server error",
  "details": "Failed to fetch Zenodo metadata: Connection timeout"
}
```

### 调试建议

1. **检查网络连接**: 确保可以访问 Zenodo API
2. **验证数据格式**: 使用 `/api/zenodo/summary` 查看可用文件
3. **查看服务器日志**: 控制台输出详细的错误信息
4. **测试简单请求**: 先用空 JSON `{}` 测试基本功能

## 性能优化

### 建议

1. **启用缓存**: 对于重复查询使用缓存可显著提升速度
2. **禁用 Bootstrap**: 如不需要置信区间，设置 `run_bootstrap=false`
3. **减少 Bootstrap 次数**: 将 `n_bootstrap` 从 1000 减少到 500 或 100
4. **批量处理**: 如需分析多个文件，考虑使用异步请求

### 性能指标

典型处理时间（无 Bootstrap）：
- 小数据集（< 100 行）: 1-2 秒
- 中等数据集（100-1000 行）: 2-5 秒
- 大数据集（> 1000 行）: 5-10 秒

使用 Bootstrap（1000 次迭代）会增加 5-20 倍处理时间。

## 安全性

### 已实现的安全措施

1. **CORS 支持**: 配置了 CORS 以支持前端集成
2. **文件大小限制**: 最大 16MB
3. **超时设置**: API 请求设置 30-60 秒超时
4. **错误隔离**: 详细的异常捕获和错误消息

### 生产环境建议

1. 配置反向代理（Nginx/Apache）
2. 使用 HTTPS
3. 添加 API 速率限制
4. 实现请求认证
5. 使用 Redis 替代内存缓存

## 扩展功能

### 未来可能的增强

1. **Redis 缓存**: 持久化缓存，支持分布式部署
2. **批量分析**: 一次请求分析多个文件
3. **定时任务**: 定期自动更新分析结果
4. **结果存储**: 将分析结果存入数据库
5. **WebSocket 支持**: 实时推送长时间运行的分析进度
6. **数据集比较**: 比较不同数据集的偏差特征

## 故障排查

### 问题: 无法连接到 Zenodo

**症状**: `Failed to fetch Zenodo metadata: Connection timeout`

**解决方案**:
1. 检查网络连接
2. 验证防火墙设置
3. 尝试手动访问: https://zenodo.org/api/records/17201032

### 问题: CSV 解析失败

**症状**: `Failed to parse CSV data`

**解决方案**:
1. 使用 `/api/zenodo/summary` 查看可用文件
2. 检查文件编码（应为 UTF-8）
3. 确认文件格式符合要求

### 问题: 数据验证失败

**症状**: `Missing required columns: ...`

**解决方案**:
1. 检查 CSV 列名是否正确
2. 确保所有必需列都存在
3. 验证数据类型和范围

## 联系和支持

- **GitHub**: https://github.com/hongping-zh/circular-bias-detection
- **文档**: 查看项目 README.md
- **问题报告**: 在 GitHub 上提交 Issue

## 许可证

本集成服务遵循项目主许可证。Zenodo 数据集的使用请遵守其自身的许可证条款。
