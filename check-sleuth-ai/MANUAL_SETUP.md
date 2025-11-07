# Check Sleuth AI - 手动执行指南

## 🎯 目标

启动前端和后端，测试 CSV 分析功能。

---

## 📋 前置检查

```powershell
# 检查 Node.js
node --version
# 应显示: v16.x.x 或更高

# 检查 Python
python --version
# 应显示: Python 3.8.x 或更高

# 检查 pip
pip --version
# 应显示版本信息
```

---

## 🚀 执行步骤

### 步骤 1: 安装前端依赖

```powershell
# 进入前端目录
cd C:\Users\14593\CascadeProjects\circular-bias-detection\check-sleuth-ai

# 安装依赖
npm install
```

**预期输出**: 
```
added XXX packages in XXs
```

---

### 步骤 2: 安装后端依赖

```powershell
# 进入后端目录
cd C:\Users\14593\CascadeProjects\circular-bias-detection\backend

# 安装依赖
pip install -r requirements.txt
```

**预期输出**:
```
Successfully installed flask-3.x.x pandas-2.x.x google-generativeai-0.x.x ...
```

---

### 步骤 3: 设置环境变量（重要）

**选项 A: 有 Gemini API Key**

```powershell
# PowerShell
$env:GEMINI_API_KEY="AIzaSy...你的API密钥..."
```

获取 API Key: https://makersuite.google.com/app/apikey

**选项 B: 没有 API Key（演示模式）**

不设置环境变量，应用会使用 Mock 数据运行。

---

### 步骤 4: 启动后端服务器

**打开新的 PowerShell 终端（终端1）**

```powershell
# 如果有 API Key，先设置
$env:GEMINI_API_KEY="你的密钥"

# 进入后端目录
cd C:\Users\14593\CascadeProjects\circular-bias-detection\backend

# 启动服务器
python app.py
```

**预期输出**:
```
======================================================================
🚀 Starting Sleuth API Server with Zenodo Integration
======================================================================

Endpoints:
  GET  /health                - Health check
  GET  /api/info              - API information
  POST /api/detect            - Bias detection (custom data)
  POST /api/analyze-csv       - Gemini AI CSV analysis
  POST /api/analyze_zenodo    - Analyze Zenodo dataset
  GET  /api/zenodo/summary    - Zenodo dataset summary
  POST /api/cache/clear       - Clear results cache

Zenodo Dataset: DOI 10.5281/zenodo.17201032
Server running on: http://localhost:5000
======================================================================

✅ Gemini API configured successfully
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

**如果看到**:
```
⚠️  Warning: GEMINI_API_KEY not set. CSV analysis endpoint will return mock data.
```
说明在演示模式下运行（这是正常的）。

**保持这个终端运行，不要关闭！**

---

### 步骤 5: 启动前端开发服务器

**打开另一个新的 PowerShell 终端（终端2）**

```powershell
# 进入前端目录
cd C:\Users\14593\CascadeProjects\circular-bias-detection\check-sleuth-ai

# 启动开发服务器
npm run dev
```

**预期输出**:
```
  VITE v6.2.0  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: http://192.168.x.x:3000/
  ➜  press h + enter to show help
```

**保持这个终端运行，不要关闭！**

---

### 步骤 6: 测试后端健康状态

**打开第三个 PowerShell 终端（终端3）**

```powershell
# 测试后端健康状态
curl http://localhost:5000/health
```

**预期输出**:
```json
{"status":"ok","service":"Sleuth Bias Detection API","version":"1.0.0"}
```

**或者在浏览器访问**: http://localhost:5000/health

---

### 步骤 7: 访问前端应用

**在浏览器中打开**: http://localhost:3000

你应该看到：
- ✅ 深色主题的页面
- ✅ "Check Sleuth AI" 标题
- ✅ CSV 上传区域

---

### 步骤 8: 测试 CSV 上传功能

**创建测试 CSV 文件**

创建文件 `C:\Users\14593\test.csv`，内容如下：

```csv
id,name,age,income,churned
1,Alice,25,50000,0
2,Bob,30,60000,1
3,Charlie,35,70000,0
4,David,28,55000,1
5,Eve,32,65000,0
```

**上传测试**:
1. 在浏览器中点击上传区域
2. 选择 `test.csv` 文件
3. 等待分析结果（1-3秒）

**预期结果**:
- ✅ 显示文件名
- ✅ 显示数据表格
- ✅ 显示 AI 分析摘要
- ✅ 显示数据质量洞察
- ✅ 显示偏差检测洞察

---

## ✅ 验证清单

运行以下命令验证系统状态：

```powershell
# 测试 1: 后端健康检查
curl http://localhost:5000/health
# 应返回: {"status":"ok",...}

# 测试 2: API 信息
curl http://localhost:5000/api/info
# 应返回: API 文档 JSON

# 测试 3: 前端是否运行
# 浏览器访问 http://localhost:3000
# 应看到应用界面
```

---

## 🛑 停止服务

**停止后端** (终端1):
```
按 Ctrl + C
```

**停止前端** (终端2):
```
按 Ctrl + C
```

---

## 🐛 常见问题

### 问题 1: 端口已被占用

**错误**:
```
OSError: [WinError 10048] 通常每个套接字地址(协议/网络地址/端口)只允许使用一次
```

**解决**:
```powershell
# 查找占用端口的进程
netstat -ano | findstr :5000

# 终止进程（替换 <PID> 为实际进程ID）
taskkill /PID <PID> /F
```

### 问题 2: 模块未找到

**错误**:
```
ModuleNotFoundError: No module named 'flask'
```

**解决**:
```powershell
cd C:\Users\14593\CascadeProjects\circular-bias-detection\backend
pip install -r requirements.txt
```

### 问题 3: npm install 失败

**解决**:
```powershell
# 清理缓存
npm cache clean --force

# 删除 node_modules
Remove-Item -Recurse -Force node_modules

# 重新安装
npm install
```

### 问题 4: CSV 分析返回 Mock 数据

**原因**: 未设置 GEMINI_API_KEY 或 API Key 无效

**解决**:
1. 确认在终端1中设置了环境变量
2. 重启后端服务器
3. 检查 API Key 是否有效

---

## 📊 终端布局建议

```
┌─────────────────────────┐  ┌─────────────────────────┐
│   终端 1: 后端服务器    │  │   终端 2: 前端服务器    │
│                         │  │                         │
│   python app.py         │  │   npm run dev           │
│   Port: 5000            │  │   Port: 3000            │
└─────────────────────────┘  └─────────────────────────┘

┌─────────────────────────┐  ┌─────────────────────────┐
│   终端 3: 测试命令      │  │   浏览器                │
│                         │  │                         │
│   curl ...              │  │   localhost:3000        │
│   验证命令              │  │   上传 CSV 文件         │
└─────────────────────────┘  └─────────────────────────┘
```

---

## 📝 快速命令参考

```powershell
# 设置 API Key
$env:GEMINI_API_KEY="your-key"

# 启动后端
cd C:\Users\14593\CascadeProjects\circular-bias-detection\backend
python app.py

# 启动前端（新终端）
cd C:\Users\14593\CascadeProjects\circular-bias-detection\check-sleuth-ai
npm run dev

# 测试（新终端）
curl http://localhost:5000/health
```

---

## 🎉 成功标志

当你看到以下内容时，说明系统运行正常：

1. ✅ 后端显示: `✅ Gemini API configured successfully` 或 `⚠️ Warning: GEMINI_API_KEY not set`
2. ✅ 前端显示: `➜ Local: http://localhost:3000/`
3. ✅ 浏览器能打开应用
4. ✅ 上传 CSV 后能看到分析结果
5. ✅ 控制台无错误信息

---

## 📞 需要帮助？

如果遇到问题：
1. 检查上面的"常见问题"部分
2. 查看终端的错误信息
3. 记录错误信息，随时请教

---

**祝运行顺利！** 🚀

有问题随时找我，我随时待命！
