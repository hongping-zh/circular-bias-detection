# ⚡ Check Sleuth AI - 快速开始

## 🎯 一分钟启动指南

### 方式 1: 使用启动脚本 (最简单)

```bash
# 双击或运行
START.bat
```

### 方式 2: 手动启动

**步骤 1️⃣: 设置 API Key**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```
获取 API Key: https://makersuite.google.com/app/apikey

**步骤 2️⃣: 启动后端** (新终端)
```bash
cd ..\backend
pip install -r requirements.txt
python app.py
```

**步骤 3️⃣: 启动前端** (新终端)
```bash
cd check-sleuth-ai
npm install
npm run dev
```

**步骤 4️⃣: 访问应用**
- 前端: http://localhost:3000
- 后端: http://localhost:5000

---

## 🧪 快速测试

### 测试后端健康
```bash
curl http://localhost:5000/health
```

### 测试 CSV 分析
1. 访问 http://localhost:3000
2. 上传任意 CSV 文件
3. 查看 AI 分析结果

---

## 📚 完整文档

- **安装指南**: README.md
- **部署指南**: DEPLOYMENT_GUIDE.md
- **实施总结**: ../MVP_IMPLEMENTATION_SUMMARY.md

---

## ⚠️ 常见问题

### Q: TypeScript 错误怎么办？
**A:** 运行 `npm install` 后自动解决

### Q: 没有 API Key 可以运行吗？
**A:** 可以！会使用 Mock 数据（演示模式）

### Q: 端口被占用？
**A:** 修改 `vite.config.ts` (前端) 或 `app.py` (后端)

---

## 🚀 部署到生产环境

**最简单:** Vercel
```bash
npm install -g vercel
vercel
```

**详细步骤:** 参见 DEPLOYMENT_GUIDE.md

---

**需要帮助？** 查看 MVP_IMPLEMENTATION_SUMMARY.md 获取完整指南
