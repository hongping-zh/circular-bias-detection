# 部署前检查清单

## ✅ 必须完成

在运行 `vercel` 命令之前，确认：

### 1. Vercel CLI 已安装
```powershell
vercel --version
```
如果未安装: `npm install -g vercel`

### 2. 已登录 Vercel
```powershell
vercel login
```

### 3. 文件检查

- [x] `vercel.json` 已创建
- [ ] `vercel.json` 中的后端 URL 已更新（部署后端后更新）
- [x] 代码无错误
- [x] 本地测试通过

### 4. 环境变量准备

如果有 Gemini API Key，准备好：
- `GEMINI_API_KEY=AIza...`

### 5. 部署顺序

**重要**: 必须先部署后端，再部署前端！

1. 后端: `cd backend && vercel --prod`
2. 前端: `cd check-sleuth-ai && vercel --prod`

---

## 🚀 快速部署命令

### 后端部署

```powershell
cd C:\Users\14593\CascadeProjects\circular-bias-detection\backend
vercel --prod
```

### 前端部署（记得先更新 vercel.json）

```powershell
cd C:\Users\14593\CascadeProjects\circular-bias-detection\check-sleuth-ai
vercel --prod
```

---

## 📝 部署后记录

**后端 URL**: _____________________________

**前端 URL**: _____________________________

**部署时间**: _____________________________
