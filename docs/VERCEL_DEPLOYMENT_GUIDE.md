# Vercel 部署完整指南

## 🎯 部署目标

将 Check Sleuth AI MVP 部署到 Vercel，获得公网访问 URL。

**预计时间**: 30-45 分钟

---

## 📋 部署前检查清单

- [x] 本地测试通过
- [x] 前端正常运行
- [x] 后端正常运行
- [x] Vercel 配置文件已创建
- [ ] 安装 Vercel CLI
- [ ] 登录 Vercel 账号

---

## 🚀 部署步骤

### 第一步：安装 Vercel CLI

```powershell
# 全局安装 Vercel CLI
npm install -g vercel

# 验证安装
vercel --version
```

**预期输出**: `Vercel CLI 33.x.x` (或最新版本)

---

### 第二步：登录 Vercel

```powershell
vercel login
```

**选择登录方式**:
- GitHub (推荐)
- GitLab
- Bitbucket
- Email

**按提示操作**:
1. 浏览器会自动打开
2. 选择账号并授权
3. 返回终端看到 "Success!" 消息

---

### 第三步：部署后端

#### 3.1 准备后端

```powershell
cd C:\Users\14593\CascadeProjects\circular-bias-detection\backend
```

#### 3.2 首次部署

```powershell
vercel
```

**交互式问题**:

```
? Set up and deploy "backend"? [Y/n] 
→ 输入: y

? Which scope do you want to deploy to?
→ 选择你的账号

? Link to existing project? [y/N]
→ 输入: n

? What's your project's name? 
→ 输入: sleuth-api 或 check-sleuth-backend

? In which directory is your code located?
→ 输入: ./ (当前目录)

? Want to modify these settings? [y/N]
→ 输入: n
```

**部署过程**:
```
Building...
Deploying...
✓ Deployment ready [20s]

Preview: https://sleuth-api-xxx.vercel.app
```

**重要**: 复制这个 URL，稍后需要用到！

#### 3.3 配置环境变量

```powershell
# 添加 Gemini API Key (如果有)
vercel env add GEMINI_API_KEY production

# 会提示输入值
? What's the value of GEMINI_API_KEY?
→ 粘贴你的 API Key

# 添加其他环境变量
vercel env add FLASK_ENV production
? What's the value of FLASK_ENV?
→ 输入: production
```

#### 3.4 重新部署（应用环境变量）

```powershell
vercel --prod
```

**完成后获得生产 URL**:
```
Production: https://sleuth-api.vercel.app
```

---

### 第四步：部署前端

#### 4.1 更新 API 配置

**编辑**: `check-sleuth-ai\vercel.json`

将 `YOUR_BACKEND_URL` 替换为后端实际 URL:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://sleuth-api.vercel.app/api/:path*"
    }
  ]
}
```

**保存文件！**

#### 4.2 切换到前端目录

```powershell
cd C:\Users\14593\CascadeProjects\circular-bias-detection\check-sleuth-ai
```

#### 4.3 首次部署

```powershell
vercel
```

**交互式问题**:

```
? Set up and deploy "check-sleuth-ai"? [Y/n] 
→ 输入: y

? Which scope do you want to deploy to?
→ 选择你的账号

? Link to existing project? [y/N]
→ 输入: n

? What's your project's name? 
→ 输入: check-sleuth-ai

? In which directory is your code located?
→ 输入: ./ 

? Want to modify these settings? [y/N]
→ 输入: n
```

**部署过程**:
```
Building...
Deploying...
✓ Deployment ready [30s]

Preview: https://check-sleuth-ai-xxx.vercel.app
```

#### 4.4 部署到生产环境

```powershell
vercel --prod
```

**完成后获得生产 URL**:
```
Production: https://check-sleuth-ai.vercel.app
```

---

### 第五步：验证部署

#### 5.1 测试后端

```powershell
# 测试 Health Check
curl https://sleuth-api.vercel.app/health

# 预期输出: {"status":"ok",...}
```

或在浏览器访问:
```
https://sleuth-api.vercel.app/health
```

#### 5.2 测试前端

在浏览器打开:
```
https://check-sleuth-ai.vercel.app
```

**验证清单**:
- [ ] 页面正常加载
- [ ] 样式显示正确
- [ ] CSV 上传功能正常
- [ ] 分析结果显示
- [ ] Demo Mode 提示显示
- [ ] 无 CORS 错误

#### 5.3 端到端测试

1. 上传 CSV 文件
2. 查看分析结果
3. 验证功能完整

---

## 🔧 故障排查

### 问题 1: 后端部署失败

**症状**: 构建错误或依赖问题

**解决**:

1. **检查 Python 版本**:
```json
// 添加到 vercel.json
{
  "build": {
    "env": {
      "PYTHON_VERSION": "3.9"
    }
  }
}
```

2. **简化依赖**:
```powershell
# 使用简化版 requirements
cp requirements-vercel.txt requirements.txt
vercel --prod
```

3. **查看构建日志**:
- 访问 Vercel Dashboard
- 选择项目
- 查看 Deployments → 最新部署 → Build Logs

---

### 问题 2: 前端无法连接后端

**症状**: CORS 错误或 404

**解决**:

1. **检查 vercel.json 配置**:
```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://YOUR-ACTUAL-BACKEND.vercel.app/api/:path*"
    }
  ]
}
```

2. **确认后端 URL 正确**:
- 访问后端 URL
- 应该看到欢迎页面

3. **检查后端 CORS 设置**:
```python
# app.py 应该有:
CORS(app)  # 允许所有来源
```

---

### 问题 3: 环境变量未生效

**症状**: Demo Mode 仍然显示

**解决**:

```powershell
# 列出环境变量
vercel env ls

# 重新添加
vercel env add GEMINI_API_KEY production

# 重新部署
vercel --prod
```

---

### 问题 4: 构建超时

**症状**: Deployment timeout

**解决**:

1. **移除大型依赖**:
```
# 从 requirements.txt 移除:
- matplotlib
- seaborn
- scikit-learn
```

2. **优化构建**:
```json
// vercel.json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ]
}
```

---

## 🎨 自定义域名（可选）

### 添加自定义域名

1. **前往 Vercel Dashboard**
2. **选择项目** → Settings → Domains
3. **添加域名**: `yourdomain.com`
4. **配置 DNS**:
   - A 记录: `76.76.21.21`
   - CNAME: `cname.vercel-dns.com`

---

## 📊 部署后优化

### 1. 配置 Google Analytics

如果之前配置了 GA:

```powershell
# 添加环境变量
vercel env add VITE_GA_MEASUREMENT_ID production
? What's the value?
→ 输入: G-XXXXXXXXXX

# 重新部署
cd check-sleuth-ai
vercel --prod
```

### 2. 监控性能

访问 Vercel Dashboard:
- Analytics (访问统计)
- Speed Insights (性能监控)
- Logs (运行日志)

### 3. 设置通知

配置部署通知:
- Email
- Slack
- GitHub

---

## 🔐 安全最佳实践

### 1. 保护 API Key

```powershell
# 永远不要在代码中硬编码
# 使用环境变量
vercel env add GEMINI_API_KEY production
```

### 2. 限制 CORS

如果需要限制来源:

```python
# app.py
CORS(app, origins=[
    "https://check-sleuth-ai.vercel.app",
    "https://yourdomain.com"
])
```

### 3. 添加速率限制

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    default_limits=["100 per hour"]
)
```

---

## 📈 部署完成清单

部署完成后，确认：

### 后端
- [ ] 部署成功
- [ ] Health check 返回 200
- [ ] API endpoints 可访问
- [ ] 环境变量已配置
- [ ] 无构建错误

### 前端
- [ ] 部署成功
- [ ] 页面正常加载
- [ ] 样式显示正确
- [ ] API 通信正常
- [ ] CSV 上传功能正常

### 集成
- [ ] 端到端流程测试通过
- [ ] Demo Mode 正常显示
- [ ] 分析结果正确
- [ ] 无 CORS 错误
- [ ] 性能可接受

---

## 🎉 部署完成后

### 获得的 URL

**后端**: `https://sleuth-api.vercel.app`  
**前端**: `https://check-sleuth-ai.vercel.app`

### 分享给他人

你现在可以分享前端 URL 给任何人:
```
https://check-sleuth-ai.vercel.app
```

### 持续部署

每次推送代码到 Git，Vercel 会自动重新部署（如果配置了 Git 集成）。

---

## 🔄 更新部署

### 更新代码后重新部署

```powershell
# 后端
cd backend
vercel --prod

# 前端
cd ..\check-sleuth-ai
vercel --prod
```

### 回滚部署

在 Vercel Dashboard:
1. 选择项目
2. Deployments
3. 找到之前的版本
4. 点击 "Promote to Production"

---

## 📞 获取帮助

### Vercel 文档
- https://vercel.com/docs

### 常见问题
- https://vercel.com/support

### 社区
- https://github.com/vercel/vercel/discussions

---

## 📝 部署记录

**前端 URL**: _____________________________  
**后端 URL**: _____________________________  
**部署日期**: _____________________________  
**部署者**: _____________________________  
**状态**: [ ] 成功  [ ] 部分成功  [ ] 失败  

**备注**: _____________________________________

---

**祝部署成功！** 🚀

有问题随时查看本指南或寻求帮助。
