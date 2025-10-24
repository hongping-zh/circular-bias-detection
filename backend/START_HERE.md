# 🚀 开始使用 Zenodo-Sleuth 集成

## ⚡ 快速开始（3 步）

### 1️⃣ 安装依赖

```bash
cd C:\Users\14593\CascadeProjects\circular-bias-detection\backend
pip install -r requirements.txt
```

新增依赖：
- `requests>=2.31.0` (用于 Zenodo API 调用)

### 2️⃣ 启动服务器

```bash
python app.py
```

您将看到：
```
======================================================================
🚀 Starting Sleuth API Server with Zenodo Integration
======================================================================

Endpoints:
  GET  /health                - Health check
  GET  /api/info              - API information
  POST /api/detect            - Bias detection (custom data)
  POST /api/analyze_zenodo    - Analyze Zenodo dataset
  GET  /api/zenodo/summary    - Zenodo dataset summary
  POST /api/cache/clear       - Clear results cache

Zenodo Dataset: DOI 10.5281/zenodo.17201032
Server running on: http://localhost:5000
======================================================================
```

### 3️⃣ 测试 API

**选项 A: 使用测试脚本（推荐）**
```bash
python test_zenodo_integration.py
```

**选项 B: 使用示例代码**
```bash
python example_usage.py
```

**选项 C: 使用 cURL**
```bash
curl -X POST http://localhost:5000/api/analyze_zenodo -H "Content-Type: application/json" -d "{}"
```

## 🎯 核心功能

### 1. 自动分析 Zenodo 数据集

```python
import requests

response = requests.post('http://localhost:5000/api/analyze_zenodo', json={})
result = response.json()

print(f"CBS 得分: {result['sleuth_analysis']['cbs_score']}")
print(f"检测到偏差: {result['sleuth_analysis']['bias_detected']}")
```

### 2. 获取数据集信息

```python
response = requests.get('http://localhost:5000/api/zenodo/summary')
summary = response.json()

print(f"标题: {summary['title']}")
print(f"文件: {[f['key'] for f in summary['files']]}")
```

### 3. 自定义分析参数

```python
response = requests.post(
    'http://localhost:5000/api/analyze_zenodo',
    json={
        'run_bootstrap': False,
        'weights': [0.4, 0.3, 0.3],
        'use_cache': True
    }
)
```

## 📁 新增文件一览

```
backend/
├── app.py                           ✏️  已更新（+3 个新端点）
├── core/
│   └── integration_service.py       ✨ 新增（集成服务）
├── utils/
│   └── zenodo_client.py             ✨ 新增（Zenodo 客户端）
├── requirements.txt                 ✏️  已更新（+requests）
│
├── 📚 文档
├── START_HERE.md                    👈 您在这里
├── README_ZENODO.md                 ✨ 快速入门
├── ZENODO_INTEGRATION_GUIDE.md      ✨ 完整文档
├── INTEGRATION_SUMMARY.md           ✨ 架构总结
│
└── 🧪 测试和示例
    ├── test_zenodo_integration.py   ✨ 集成测试
    └── example_usage.py             ✨ 使用示例
```

## 🎓 学习路径

1. **第一步**: 运行 `python app.py` 启动服务器
2. **第二步**: 运行 `python test_zenodo_integration.py` 验证功能
3. **第三步**: 查看 `README_ZENODO.md` 了解基本用法
4. **第四步**: 运行 `python example_usage.py` 学习各种场景
5. **第五步**: 阅读 `ZENODO_INTEGRATION_GUIDE.md` 深入了解
6. **第六步**: 查看 `INTEGRATION_SUMMARY.md` 理解架构

## 🔌 API 端点速查

| 端点 | 方法 | 用途 |
|------|------|------|
| `/api/analyze_zenodo` | POST | 分析 Zenodo 数据集 |
| `/api/zenodo/summary` | GET | 获取数据集摘要 |
| `/api/cache/clear` | POST | 清除缓存 |
| `/api/detect` | POST | 分析自定义数据（原有） |
| `/api/info` | GET | API 信息 |
| `/health` | GET | 健康检查 |

## 💡 常见使用场景

### 场景 1: 快速分析
```bash
curl -X POST http://localhost:5000/api/analyze_zenodo -H "Content-Type: application/json" -d "{}"
```

### 场景 2: 前端集成
```javascript
const response = await fetch('http://localhost:5000/api/analyze_zenodo', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({})
});
const data = await response.json();
```

### 场景 3: Python 脚本
```python
import requests

def analyze():
    r = requests.post('http://localhost:5000/api/analyze_zenodo', json={})
    return r.json()

result = analyze()
print(result['sleuth_analysis']['cbs_score'])
```

## ⚠️ 常见问题

### Q: 服务器启动失败？
**A**: 检查端口 5000 是否被占用
```bash
# Windows
netstat -ano | findstr :5000

# 如果被占用，可以在 app.py 中修改端口号
app.run(host='0.0.0.0', port=5001)  # 改为 5001
```

### Q: 无法连接到 Zenodo？
**A**: 
1. 检查网络连接
2. 确认可以访问 https://zenodo.org
3. 查看防火墙设置

### Q: 数据验证失败？
**A**: 
1. 使用 `/api/zenodo/summary` 查看数据集结构
2. 确认数据包含必需列：`time_period`, `algorithm`, `performance`, `constraint_*`
3. 检查数据格式是否正确

### Q: 分析速度慢？
**A**: 
1. 确保启用缓存：`"use_cache": true`
2. 禁用 Bootstrap：`"run_bootstrap": false`
3. 检查网络延迟

## 📊 性能提示

- ✅ **使用缓存**: 相同参数查询提速 10-50x
- ✅ **禁用 Bootstrap**: 如不需要置信区间，节省 5-20x 时间
- ✅ **减少迭代**: 将 `n_bootstrap` 从 1000 降到 100-500

## 🔐 安全提示

当前配置适合开发环境。**生产部署时请**：

1. 使用反向代理（Nginx）
2. 启用 HTTPS
3. 添加 API 认证
4. 配置速率限制
5. 使用环境变量管理配置

## 📞 获取帮助

- **快速参考**: `README_ZENODO.md`
- **完整文档**: `ZENODO_INTEGRATION_GUIDE.md`
- **架构说明**: `INTEGRATION_SUMMARY.md`
- **代码示例**: `example_usage.py`
- **GitHub**: https://github.com/hongping-zh/circular-bias-detection

## 🎉 下一步

现在您可以：

1. ✅ 集成到您的前端应用
2. ✅ 自定义分析参数
3. ✅ 添加更多数据源
4. ✅ 实现批量分析
5. ✅ 添加定时任务
6. ✅ 部署到生产环境

---

**开始探索**: 运行 `python app.py` 然后访问 http://localhost:5000/api/info 🚀
