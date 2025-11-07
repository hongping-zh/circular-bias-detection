# Vercel 域名配置指南

## 🎯 目标

将前端 URL 从：
```
https://biasdetector-qhhge8z0l-hongpings-projects.vercel.app
```

优化为：
```
https://biasdetector.vercel.app
```

---

## 📋 配置步骤（5 分钟）

### 第一步：访问 Vercel Dashboard

1. **打开浏览器**，访问：
   ```
   https://vercel.com/hongpings-projects/biasdetector
   ```

2. **或者从 Dashboard 进入**：
   - 访问：https://vercel.com/dashboard
   - 找到项目 "biasdetector"
   - 点击进入

---

### 第二步：进入域名设置

1. **在项目页面，点击 "Settings" 标签**（顶部菜单）

2. **在左侧菜单，点击 "Domains"**

3. **你会看到当前域名**：
   ```
   biasdetector-qhhge8z0l-hongpings-projects.vercel.app (Production)
   ```

---

### 第三步：添加新域名

1. **在 "Domains" 页面，找到输入框**

2. **输入新域名**：
   ```
   biasdetector.vercel.app
   ```

3. **点击 "Add" 按钮**

---

### 第四步：确认配置

**Vercel 会自动**：
- ✅ 验证域名可用性
- ✅ 配置 SSL 证书（自动）
- ✅ 设置 DNS（自动）
- ✅ 将域名设为 Production

**如果域名已被占用**：
- 尝试：`bias-detector.vercel.app`
- 或：`circular-bias-detector.vercel.app`
- 或：`sleuth-detector.vercel.app`

---

### 第五步：设为主域名（可选）

1. **在域名列表中，找到新添加的域名**

2. **点击域名右侧的三个点 (...)** 

3. **选择 "Set as Primary Domain"**

这样旧域名会自动重定向到新域名。

---

## ✅ 完成后

你的应用将可以通过以下 URL 访问：

### 主域名
```
https://biasdetector.vercel.app
```

### 旧域名（自动重定向）
```
https://biasdetector-qhhge8z0l-hongpings-projects.vercel.app
```

---

## 🔐 SSL 证书

**自动配置**：
- ✅ Vercel 自动提供免费 SSL 证书
- ✅ 支持 HTTPS
- ✅ 自动续期
- ✅ A+ 评级

**无需任何操作！**

---

## 🌐 DNS 配置

**无需配置**：
- ✅ `*.vercel.app` 域名由 Vercel 管理
- ✅ 自动全球 CDN
- ✅ 超快访问速度

---

## 📊 完整配置对比

| 项目 | 优化前 | 优化后 |
|------|--------|--------|
| **前端 URL** | biasdetector-qhhge8z0l-hongpings-projects.vercel.app | biasdetector.vercel.app |
| **后端 URL** | hongpingzhang.pythonanywhere.com | 保持不变 |
| **SSL** | ✅ 自动 | ✅ 自动 |
| **CDN** | ✅ 全球 | ✅ 全球 |
| **成本** | $0 | $0 |

---

## 🔧 故障排查

### 问题 1：域名已被占用

**错误信息**：`Domain is already in use`

**解决**：
选择其他域名：
- `bias-detector.vercel.app`
- `circular-bias.vercel.app`
- `sleuth-ai.vercel.app`
- `ml-bias-detector.vercel.app`

---

### 问题 2：SSL 证书未生效

**症状**：浏览器显示不安全

**解决**：
- 等待 5-10 分钟（SSL 自动配置）
- 刷新浏览器
- 清除缓存

---

### 问题 3：域名无法访问

**检查**：
1. 在 Vercel Dashboard 确认域名状态为 "Valid"
2. 确认已设为 Production
3. 等待 DNS 传播（最多 5 分钟）

---

## 📝 配置清单

完成后检查：

- [ ] 访问 Vercel Dashboard
- [ ] 进入 biasdetector 项目
- [ ] 添加 `biasdetector.vercel.app` 域名
- [ ] 域名状态显示 "Valid"
- [ ] 设为 Primary Domain
- [ ] 在浏览器访问新域名
- [ ] 确认 HTTPS 正常
- [ ] 确认应用正常运行
- [ ] 旧域名自动重定向

---

## 🎉 优化效果

### URL 对比

**优化前**：
```
https://biasdetector-qhhge8z0l-hongpings-projects.vercel.app
```
- 字符数：65
- 可读性：❌ 差
- 专业性：❌ 差

**优化后**：
```
https://biasdetector.vercel.app
```
- 字符数：32
- 可读性：✅ 优秀
- 专业性：✅ 良好

**改善**：
- ✅ 短了 50%
- ✅ 易于记忆
- ✅ 易于分享
- ✅ 更专业

---

## 🔗 完整应用架构

```
用户访问
    ↓
https://biasdetector.vercel.app
(Vercel 前端 - 全球 CDN)
    ↓
https://hongpingzhang.pythonanywhere.com
(PythonAnywhere 后端 - Flask API)
    ↓
Gemini AI / Demo Mode
```

---

## 📱 分享你的应用

**简短 URL**：
```
biasdetector.vercel.app
```

**社交媒体分享**：
```
🚀 Check out my new AI-powered bias detector!
👉 https://biasdetector.vercel.app

Detect circular bias and data leakage in ML datasets.
```

**二维码生成**（可选）：
- 访问：https://www.qr-code-generator.com/
- 输入：`https://biasdetector.vercel.app`
- 下载二维码用于推广

---

## 🎯 下一步优化建议

### 立即可做：
1. ✅ 配置 Vercel 域名（5 分钟）
2. ✅ 测试新 URL
3. ✅ 更新 README 和文档

### 后续可做：
1. 注册真正的自定义域名（如 `biasdetector.com`）
2. 配置 Gemini API Key
3. 添加 Google Analytics
4. 性能优化

---

## 📞 需要帮助？

如果遇到问题：
- Vercel 文档：https://vercel.com/docs/concepts/projects/domains
- Vercel 支持：https://vercel.com/support

---

**预计完成时间：5 分钟**

**难度：⭐☆☆☆☆（非常简单）**

---

## ✅ 完成确认

配置完成后，请访问：
```
https://biasdetector.vercel.app
```

应该看到你的应用正常运行！

---

**祝配置顺利！** 🎉
