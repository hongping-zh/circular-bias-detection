# Zenodo Integration - Quick Start

快速开始使用 Sleuth API 与 Zenodo 数据集集成。

## 🚀 快速启动

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

新增依赖：
- `requests>=2.31.0` - 用于 Zenodo API 调用

### 2. 启动服务器

```bash
python app.py
```

服务器将启动在 `http://localhost:5000`

### 3. 测试集成

```bash
python test_zenodo_integration.py
```

## 📋 新增 API 端点

### 1. 分析 Zenodo 数据集

```bash
# 最简单的调用（使用所有默认值）
curl -X POST http://localhost:5000/api/analyze_zenodo \
  -H "Content-Type: application/json" \
  -d '{}'
```

返回：
- Zenodo 数据集元数据
- 数据集统计信息
- Sleuth 循环偏差分析结果

### 2. 获取数据集摘要

```bash
curl http://localhost:5000/api/zenodo/summary
```

### 3. 清除缓存

```bash
curl -X POST http://localhost:5000/api/cache/clear
```

## 🎯 使用场景

### 场景 1: 自动分析 Zenodo 数据集

```python
import requests

# 获取并分析数据集
response = requests.post('http://localhost:5000/api/analyze_zenodo', json={})
results = response.json()

print(f"CBS Score: {results['sleuth_analysis']['cbs_score']}")
print(f"Bias Detected: {results['sleuth_analysis']['bias_detected']}")
```

### 场景 2: 前端集成

```javascript
// 在您的前端应用中
async function analyzeData() {
  const response = await fetch('http://localhost:5000/api/analyze_zenodo', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ run_bootstrap: false })
  });
  
  const data = await response.json();
  displayResults(data);
}
```

### 场景 3: 批量处理工作流

```python
# 定期分析和监控
import schedule
import time

def analyze_and_log():
    response = requests.post('http://localhost:5000/api/analyze_zenodo', json={})
    results = response.json()
    
    # 记录结果
    with open('analysis_log.txt', 'a') as f:
        f.write(f"{results['processing_info']['timestamp']}: CBS={results['sleuth_analysis']['cbs_score']}\n")

# 每天运行一次
schedule.every().day.at("02:00").do(analyze_and_log)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 📂 新增文件

```
backend/
├── app.py                          # 更新：新增 3 个端点
├── core/
│   └── integration_service.py      # 新增：集成服务
├── utils/
│   └── zenodo_client.py            # 新增：Zenodo API 客户端
├── requirements.txt                # 更新：添加 requests
├── test_zenodo_integration.py      # 新增：测试脚本
├── ZENODO_INTEGRATION_GUIDE.md     # 新增：详细文档
└── README_ZENODO.md                # 本文件
```

## 🔑 核心特性

### ✅ 已实现

1. **自动数据获取** - 从 Zenodo 自动下载 CSV 数据
2. **智能验证** - 自动验证数据格式是否符合 Sleuth 要求
3. **结果整合** - 将 Zenodo 元数据与分析结果整合
4. **内存缓存** - 自动缓存分析结果，避免重复计算
5. **错误处理** - 完善的异常捕获和错误消息
6. **CORS 支持** - 支持前端跨域调用

### 🔜 未来增强

1. Redis 缓存（持久化）
2. 批量文件分析
3. 定时任务调度
4. 结果数据库存储
5. WebSocket 实时进度推送

## 🛠️ 技术架构

```
用户 → API端点 → IntegrationService
                      ↓
                ZenodoClient (获取数据)
                      ↓
              detect_circular_bias (分析)
                      ↓
                  整合结果返回
```

**关键优势**：
- 🔒 **安全**: API 密钥和逻辑在后端
- ⚡ **高效**: 服务器间通信 + 缓存机制
- 🔧 **可扩展**: 易于添加新功能
- 🎨 **简洁**: 前端只需一个 API 调用

## 📖 详细文档

查看 `ZENODO_INTEGRATION_GUIDE.md` 获取：
- 完整 API 文档
- 详细使用示例
- 性能优化建议
- 故障排查指南
- 安全最佳实践

## 🧪 测试

运行完整测试套件：

```bash
python test_zenodo_integration.py
```

测试包括：
- Health check
- API 信息查询
- Zenodo 摘要获取
- 简单分析
- 自定义参数分析
- 缓存功能验证
- 缓存清除

## ⚡ 性能提示

1. **启用缓存**: 相同参数的查询会使用缓存，速度提升 10-50 倍
2. **禁用 Bootstrap**: 如不需要置信区间，可节省 5-20 倍时间
3. **网络优化**: 确保服务器与 Zenodo 之间网络畅通

## 🐛 常见问题

**Q: 无法连接到 Zenodo？**
- 检查网络连接
- 验证 Zenodo.org 是否可访问
- 查看防火墙设置

**Q: CSV 文件解析失败？**
- 使用 `/api/zenodo/summary` 查看可用文件
- 确认文件格式符合要求（见文档）

**Q: 分析速度慢？**
- 确保启用了缓存
- 考虑禁用 Bootstrap
- 检查网络延迟

## 📞 支持

- **完整文档**: `ZENODO_INTEGRATION_GUIDE.md`
- **GitHub**: https://github.com/hongping-zh/circular-bias-detection
- **Issues**: 在 GitHub 上报告问题

## 📄 许可证

本集成遵循主项目许可证。使用 Zenodo 数据请遵守其许可条款。

---

**开始使用**: 运行 `python app.py` 并访问 `http://localhost:5000/api/info` 查看所有可用端点！
