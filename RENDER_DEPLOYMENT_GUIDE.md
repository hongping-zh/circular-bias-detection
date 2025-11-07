# Render 后端部署指南

## 🎯 为什么选择 Render

- ✅ **免费层**: 750 小时/月（足够个人项目）
- ✅ **Python 原生支持**: 无依赖问题
- ✅ **自动 HTTPS**: 免费 SSL 证书
- ✅ **自动部署**: Git push 自动部署
- ✅ **简单配置**: 5-10 分钟完成

---

## 📋 部署前准备

### 必需条件

- [x] GitHub 账号
- [x] Render 账号（免费注册）
- [x] 后端代码已准备好

### 文件检查

- [x] `requirements.txt` 已更新（包含 gunicorn）
- [x] `render.yaml` 已创建
- [x] `app.py` 可以运行

---

## 🚀 部署步骤

### 第一步：注册 Render

1. 访问：https://render.com/
2. 点击 "Get Started" 或 "Sign Up"
3. 选择 "Sign in with GitHub"（推荐）
4. 授权 Render 访问你的仓库

---

### 第二步：推送代码到 GitHub（如果还没有）

#### 选项 A：创建新仓库

```powershell
cd C:\Users\14593\CascadeProjects\circular-bias-detection

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit - Circular Bias Detector"

# 创建 GitHub 仓库（在 GitHub 网站创建后）
git remote add origin https://github.com/你的用户名/circular-bias-detection.git

# 推送
git push -u origin main
```

#### 选项 B：使用现有仓库

```powershell
cd C:\Users\14593\CascadeProjects\circular-bias-detection

git add .
git commit -m "Add Render deployment config"
git push
```

---

### 第三步：在 Render 创建 Web Service

1. **登录 Render Dashboard**
   - https://dashboard.render.com/

2. **点击 "New +"**
   - 选择 "Web Service"

3. **连接 GitHub 仓库**
   - 选择你的仓库：`circular-bias-detection`
   - 或者搜索仓库名称

4. **配置服务**

   **Name**: `circular-bias-api`
   
   **Region**: `Oregon (US West)` 或最近的区域
   
   **Branch**: `main` 或 `master`
   
   **Root Directory**: `backend`
   
   **Runtime**: `Python 3`
   
   **Build Command**: 
   ```
   pip install -r requirements.txt
   ```
   
   **Start Command**:
   ```
   gunicorn app:app
   ```
   
   **Instance Type**: `Free`

5. **高级设置（可选）**
   
   **Environment Variables**:
   - Key: `FLASK_ENV`
   - Value: `production`
   
   如果有 Gemini API Key:
   - Key: `GEMINI_API_KEY`
   - Value: `你的API Key`

6. **点击 "Create Web Service"**

---

### 第四步：等待部署

**部署过程**（约 3-5 分钟）:

```
1. 克隆仓库 ✓
2. 安装依赖 ✓ (pip install)
3. 构建应用 ✓
4. 启动服务 ✓
```

**成功标志**:
- 状态显示：`Live` 🟢
- 有一个 URL：`https://circular-bias-api.onrender.com`

---

### 第五步：获取后端 URL

部署成功后，你会看到：

```
https://circular-bias-api.onrender.com
```

或类似的 URL。**复制这个 URL！**

---

### 第六步：测试后端

在浏览器访问：
```
https://circular-bias-api.onrender.com/health
```

**预期响应**:
```json
{
  "status": "ok",
  "service": "Sleuth Bias Detection API",
  "version": "1.0.0"
}
```

✅ 如果看到这个，后端部署成功！

---

### 第七步：更新前端配置

回到前端，更新 API 端点：

**编辑**: `check-sleuth-ai/services/geminiService.ts`

找到 API_BASE_URL，更新为：
```typescript
const API_BASE_URL = 'https://circular-bias-api.onrender.com';
```

或者使用环境变量（推荐）:

**创建**: `check-sleuth-ai/.env`
```
VITE_API_URL=https://circular-bias-api.onrender.com
```

---

### 第八步：重新部署前端

```powershell
cd C:\Users\14593\CascadeProjects\circular-bias-detection\check-sleuth-ai
vercel --prod
```

---

## ✅ 验证完整系统

### 测试流程

1. **访问前端**: https://biasdetector-xxx.vercel.app
2. **上传 CSV**: 使用测试文件
3. **查看结果**: 应该显示真实的 AI 分析（不是 Demo）

---

## 🔧 故障排查

### 问题 1: 部署失败

**查看日志**:
- Render Dashboard → 你的服务 → Logs
- 查看错误信息

**常见原因**:
- Python 版本不兼容
- 依赖安装失败
- 启动命令错误

**解决**:
```yaml
# 在 render.yaml 中指定 Python 版本
envVars:
  - key: PYTHON_VERSION
    value: 3.9.16
```

---

### 问题 2: 服务启动后崩溃

**检查**:
- 确认 `gunicorn app:app` 正确
- 确认 `app.py` 中有 `app = Flask(__name__)`

**测试本地**:
```powershell
cd backend
pip install gunicorn
gunicorn app:app
```

---

### 问题 3: CORS 错误

**确认** `app.py` 中有：
```python
from flask_cors import CORS
CORS(app)
```

---

### 问题 4: API 响应慢

**原因**: 免费层会在不活动时休眠（"cold start"）

**解决**:
- 首次请求可能需要 30-60 秒
- 或升级到付费层（$7/月）

**优化**:
- 使用 Render Cron Jobs 定期 ping
- 或使用 UptimeRobot 保持唤醒

---

## 💰 成本说明

### 免费层限制

- ✅ 750 小时/月（约 31 天连续运行）
- ✅ 512MB RAM
- ✅ 0.1 CPU
- ⚠️ 15 分钟不活动后休眠
- ⚠️ 带宽限制：100GB/月

### 付费层 ($7/月)

- ✅ 始终在线（无休眠）
- ✅ 更多资源
- ✅ 自定义域名

**建议**: 先用免费层测试，有流量后再升级

---

## 🔐 环境变量管理

### 添加环境变量

1. Render Dashboard → 你的服务
2. Environment → Add Environment Variable
3. 输入 Key 和 Value
4. 点击 "Save Changes"
5. 服务会自动重新部署

### 常用环境变量

```
FLASK_ENV=production
GEMINI_API_KEY=你的API Key
DATABASE_URL=postgresql://... (如果用数据库)
```

---

## 📊 监控和日志

### 查看日志

Render Dashboard → 你的服务 → Logs

**实时日志**:
```
[2025-11-06 12:00:00] Starting gunicorn...
[2025-11-06 12:00:01] Listening on :10000
[2025-11-06 12:00:05] POST /api/analyze-csv 200
```

### 监控指标

- CPU 使用率
- 内存使用
- 请求数量
- 响应时间

---

## 🔄 自动部署

### 设置自动部署

1. **Push 代码到 GitHub**
2. **Render 自动检测变更**
3. **自动重新部署**

**工作流程**:
```
本地修改代码
    ↓
git push
    ↓
Render 自动部署
    ↓
新版本上线
```

---

## 🌐 自定义域名（可选）

### 添加域名

1. Render Dashboard → Settings → Custom Domain
2. 输入你的域名：`api.yourdomain.com`
3. 添加 DNS 记录（Render 会提供）:
   - Type: `CNAME`
   - Name: `api`
   - Value: `circular-bias-api.onrender.com`

---

## 📈 性能优化

### 1. 添加缓存

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_computation(data):
    # 你的计算逻辑
    pass
```

### 2. 使用 Redis（可选）

Render 提供免费 Redis：
- Dashboard → New + → Redis
- 连接到你的 Web Service

### 3. 数据库（可选）

如果需要存储数据：
- Dashboard → New + → PostgreSQL
- 免费层：256MB 存储

---

## 🔗 结合 Supabase（高级）

### 为什么加入 Supabase

- 存储分析历史
- 用户认证
- 实时功能

### 集成步骤

1. **注册 Supabase**: https://supabase.com
2. **创建项目**
3. **获取 API Keys**
4. **在 Render 添加环境变量**:
   ```
   SUPABASE_URL=https://xxx.supabase.co
   SUPABASE_KEY=你的Key
   ```
5. **在 Flask 中连接**:
   ```python
   from supabase import create_client
   
   supabase = create_client(
       os.getenv('SUPABASE_URL'),
       os.getenv('SUPABASE_KEY')
   )
   ```

---

## 📝 部署清单

完成部署后确认：

- [ ] Render 账号已创建
- [ ] GitHub 仓库已推送
- [ ] Web Service 已创建
- [ ] 部署状态：Live 🟢
- [ ] Health check 返回 200
- [ ] 环境变量已配置
- [ ] 前端已更新 API URL
- [ ] 前端已重新部署
- [ ] 端到端测试通过

---

## 🎉 部署完成

你现在有：
- ✅ 前端在 Vercel
- ✅ 后端在 Render
- ✅ 完全可用的应用
- ✅ 自动部署流程

**你的应用架构**:
```
用户浏览器
    ↓
Vercel (前端)
    ↓
Render (Flask API)
    ↓
Gemini AI / Supabase (可选)
```

---

## 📞 获取帮助

- **Render 文档**: https://render.com/docs
- **Render 社区**: https://community.render.com/
- **支持**: support@render.com

---

## 🚀 下一步

1. ✅ 测试所有功能
2. ✅ 监控性能
3. ✅ 收集用户反馈
4. 考虑添加功能：
   - 用户认证
   - 分析历史
   - 数据导出
   - 高级报告

---

**恭喜！你的应用已完整部署！** 🎉

**前端**: https://biasdetector-xxx.vercel.app  
**后端**: https://circular-bias-api.onrender.com

---

**部署日期**: ___________  
**后端 URL**: ___________  
**状态**: [ ] 完成
