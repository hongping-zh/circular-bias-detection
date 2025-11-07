# Check Sleuth AI - MVP部署指南

## 📋 目录

1. [系统架构](#系统架构)
2. [本地开发环境](#本地开发环境)
3. [生产环境部署](#生产环境部署)
4. [安全配置](#安全配置)
5. [故障排查](#故障排查)

---

## 系统架构

### 当前架构图

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│                 │         │                  │         │                 │
│  React Frontend │ ───────▶│  Flask Backend   │ ───────▶│  Gemini API     │
│  (Port 3000)    │  /api/* │  (Port 5000)     │  HTTPS  │  (Google)       │
│                 │         │                  │         │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
      ↑                             ↑
      │                             │
      │                     GEMINI_API_KEY
      │                     (Environment Variable)
      │
   用户上传CSV
```

### 技术栈

**前端**
- React 19
- TypeScript
- Vite (开发服务器 + 构建工具)
- Tailwind CSS

**后端**
- Python 3.8+
- Flask 3.0+
- google-generativeai
- Flask-CORS

---

## 本地开发环境

### 第一步：检查前置条件

```bash
# 检查 Node.js 版本 (需要 v16+)
node --version

# 检查 Python 版本 (需要 3.8+)
python --version

# 检查 pip
pip --version
```

### 第二步：安装前端依赖

```bash
cd C:\Users\14593\CascadeProjects\circular-bias-detection\check-sleuth-ai
npm install
```

**注意**: 初次运行时，VSCode 可能会显示 TypeScript 错误。这是正常的，运行 `npm install` 后会自动解决。

### 第三步：安装后端依赖

```bash
cd ..\backend
pip install -r requirements.txt
```

### 第四步：配置环境变量

获取 Gemini API Key:
1. 访问 https://makersuite.google.com/app/apikey
2. 登录 Google 账号
3. 创建或复制 API Key

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY="AIzaSy..."
```

**Windows CMD:**
```cmd
set GEMINI_API_KEY=AIzaSy...
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY=AIzaSy...
```

### 第五步：启动后端服务器

```bash
# 在 backend 目录
python app.py
```

**预期输出:**
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
```

**如果没有设置 API Key:**
```
⚠️  Warning: GEMINI_API_KEY not set. CSV analysis endpoint will return mock data.
```

### 第六步：启动前端开发服务器

```bash
# 在新的终端，check-sleuth-ai 目录
npm run dev
```

**预期输出:**
```
  VITE v6.2.0  ready in XXX ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: http://192.168.x.x:3000/
  ➜  press h + enter to show help
```

### 第七步：测试应用

1. 在浏览器打开 http://localhost:3000
2. 上传一个 CSV 文件
3. 查看 AI 分析结果

**测试后端健康状态:**
```bash
# 在新终端
curl http://localhost:5000/health
```

---

## 生产环境部署

### 方案 1: Vercel (推荐 - 最简单)

**优点:**
- 零配置部署
- 自动 HTTPS
- 免费套餐足够 MVP
- 自动 CI/CD

**步骤:**

1. **安装 Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **创建 `vercel.json` 配置**
   ```bash
   cd C:\Users\14593\CascadeProjects\circular-bias-detection
   ```

3. **部署**
   ```bash
   vercel
   ```

4. **设置环境变量**
   ```bash
   vercel env add GEMINI_API_KEY
   # 输入你的 API Key
   ```

5. **访问生产 URL**
   ```
   https://your-app.vercel.app
   ```

**Vercel 配置文件示例** (`check-sleuth-ai/vercel.json`):
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-backend-url.com/api/:path*"
    }
  ]
}
```

### 方案 2: Netlify (Frontend) + Google Cloud Function (Backend)

**Frontend 部署 (Netlify):**

1. **构建前端**
   ```bash
   cd check-sleuth-ai
   npm run build
   ```

2. **部署到 Netlify**
   - 方法 1: 拖拽 `dist/` 文件夹到 https://app.netlify.com/drop
   - 方法 2: 使用 Netlify CLI
     ```bash
     npm install -g netlify-cli
     netlify deploy --prod
     ```

3. **配置重定向**
   
   创建 `check-sleuth-ai/dist/_redirects`:
   ```
   /api/*  https://your-cloud-function-url.com/api/:splat  200
   ```

**Backend 部署 (Google Cloud Function):**

1. **准备 Cloud Function**
   
   创建 `backend/main.py`:
   ```python
   from app import app
   
   def handle_request(request):
       return app(request.environ, lambda *args: None)
   ```

2. **部署**
   ```bash
   cd backend
   gcloud functions deploy sleuth-backend \
     --runtime python39 \
     --trigger-http \
     --allow-unauthenticated \
     --set-env-vars GEMINI_API_KEY=your-api-key
   ```

### 方案 3: 传统 VM 部署

**Frontend (Nginx):**
```bash
# 构建
cd check-sleuth-ai
npm run build

# 复制到 Nginx
sudo cp -r dist/* /var/www/html/

# Nginx 配置
location /api/ {
    proxy_pass http://localhost:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

**Backend (Systemd Service):**

创建 `/etc/systemd/system/sleuth-backend.service`:
```ini
[Unit]
Description=Sleuth Backend API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/sleuth/backend
Environment="GEMINI_API_KEY=your-api-key"
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务:
```bash
sudo systemctl enable sleuth-backend
sudo systemctl start sleuth-backend
sudo systemctl status sleuth-backend
```

---

## 安全配置

### 1. API Key 安全

**✅ 正确做法:**
- 永远使用环境变量
- 不要提交到 Git
- 使用密钥管理服务 (AWS Secrets Manager, Google Secret Manager)

**❌ 错误做法:**
- 硬编码在代码中
- 提交到版本控制
- 在前端代码中使用

### 2. CORS 配置

**开发环境:** (已配置)
```python
CORS(app)  # 允许所有来源
```

**生产环境:**
```python
CORS(app, origins=[
    "https://your-domain.com",
    "https://www.your-domain.com"
])
```

### 3. 速率限制

生产环境建议添加:
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)

@app.route('/api/analyze-csv', methods=['POST'])
@limiter.limit("10 per minute")
def analyze_csv():
    # ...
```

### 4. HTTPS

生产环境必须使用 HTTPS:
- Vercel/Netlify: 自动配置
- 自托管: 使用 Let's Encrypt + Certbot

### 5. Google Analytics 配置

**快速设置 (生产环境):**

1. **获取 GA4 Measurement ID**
   - 访问 https://analytics.google.com/
   - 创建 GA4 属性
   - 复制 Measurement ID (格式: `G-XXXXXXXXXX`)

2. **方式 A: 简单配置** (单环境)
   
   编辑 `index.html` (第37-46行)，取消注释并替换 ID:
   ```html
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-YOUR-ID"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'G-YOUR-ID');
   </script>
   ```

3. **方式 B: 环境变量配置** (推荐)
   
   **Vercel:**
   ```bash
   vercel env add VITE_GA_MEASUREMENT_ID
   # 输入: G-YOUR-ID
   ```
   
   **Netlify:**
   在 Site settings → Environment variables 添加:
   ```
   VITE_GA_MEASUREMENT_ID = G-YOUR-ID
   ```

4. **验证配置**
   - 部署后访问网站
   - 在 GA4 → Realtime 中查看活跃用户
   - 应该能看到实时数据

**详细配置:** 参见 `GOOGLE_ANALYTICS_SETUP.md`
- 环境变量方案
- 自定义事件追踪
- Cookie 同意机制
- GDPR 合规

---

## 故障排查

### 问题 1: TypeScript 错误

**症状:** VSCode 显示 "Cannot find module 'vite'"

**解决方案:**
```bash
cd check-sleuth-ai
npm install
```

### 问题 2: 后端 API 调用失败

**症状:** 前端显示 "Network Error"

**检查清单:**
1. 后端是否在运行?
   ```bash
   curl http://localhost:5000/health
   ```

2. 端口是否正确? (后端: 5000, 前端: 3000)

3. 查看浏览器控制台网络标签

4. 检查后端日志

### 问题 3: Gemini API 返回 403

**症状:** "API key not valid"

**解决方案:**
1. 验证 API Key:
   ```bash
   echo $env:GEMINI_API_KEY  # PowerShell
   echo %GEMINI_API_KEY%     # CMD
   ```

2. 检查 API Key 是否在 Google AI Studio 中激活

3. 确认 Gemini API 配额未超限

### 问题 4: CORS 错误

**症状:** "Access-Control-Allow-Origin header"

**解决方案:**
1. 确认后端安装了 `flask-cors`:
   ```bash
   pip install flask-cors
   ```

2. 检查 CORS 配置在 `app.py`:
   ```python
   from flask_cors import CORS
   CORS(app)
   ```

### 问题 5: 生产环境 API 代理失败

**症状:** 生产环境 API 调用 404

**解决方案:**

更新 `geminiService.ts` 使用绝对 URL:
```typescript
const analysisEndpoint = import.meta.env.PROD 
  ? 'https://your-backend-url.com/api/analyze-csv'
  : '/api/analyze-csv';
```

---

## 性能优化

### 1. 前端优化

```bash
# 分析构建大小
npm run build
npx vite-bundle-visualizer
```

### 2. 后端优化

**添加响应压缩:**
```python
from flask_compress import Compress
Compress(app)
```

**添加缓存:**
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/analyze-csv', methods=['POST'])
@cache.memoize(timeout=300)
def analyze_csv():
    # ...
```

### 3. Gemini API 优化

- 使用 `gemini-2.0-flash-exp` (更快)
- 限制 CSV 预览行数 (当前: 20 行)
- 实现请求去重

---

## 监控与日志

### 生产环境建议

1. **日志聚合**: Sentry, LogRocket
2. **性能监控**: Google Analytics, Plausible
3. **错误追踪**: 
   ```python
   import sentry_sdk
   sentry_sdk.init(dsn="your-sentry-dsn")
   ```

4. **健康检查端点**: 
   ```bash
   # 设置定时检查
   */5 * * * * curl https://your-app.com/health
   ```

---

## 下一步

- [ ] 本地测试完整流程
- [ ] 选择部署方案
- [ ] 配置生产环境变量
- [ ] 部署到生产环境
- [ ] 设置自定义域名
- [ ] 配置监控和日志
- [ ] 性能优化
- [ ] 用户反馈收集

---

## 联系与支持

- GitHub Issues: https://github.com/hongping-zh/circular-bias-detection/issues
- 文档: check-sleuth-ai/README.md
- API 文档: http://localhost:5000/api/info

---

**最后更新:** 2025-11-05
**版本:** 1.0.0
