# 🚀 Sleuth v1.1 部署指南

本指南提供完整的代码提交和网站发布流程。

---

## ⚡ 快速部署（推荐）

### 方法1：使用自动化脚本

双击运行项目根目录的 `deploy.bat` 文件，脚本会自动：
1. ✅ 提交所有代码到GitHub
2. ✅ 构建Web App生产版本
3. ✅ 部署到GitHub Pages

**使用步骤：**
```bash
# 直接双击 deploy.bat 文件
# 或在命令行中运行：
.\deploy.bat
```

---

## 📋 手动部署流程

如果您希望分步骤手动操作，请按以下步骤进行：

### 第1步：提交代码到GitHub

```bash
# 1. 进入项目目录
cd C:\Users\14593\CascadeProjects\circular-bias-detection

# 2. 查看所有修改
git status

# 3. 添加所有文件
git add .

# 4. 创建提交
git commit -m "feat(v1.1): Add comprehensive enhancements

- Bootstrap statistical analysis (n=1000, CI, p-values)
- Adaptive thresholds via permutation tests  
- LLM evaluation support with guide
- Data validation and auto-cleaning
- Enhanced visualizations (heatmaps, Plotly)
- New examples: llm_evaluation, visualization
- Updated documentation"

# 5. 推送到GitHub
git push origin main
```

**预期输出：**
```
Enumerating objects: 25, done.
Counting objects: 100% (25/25), done.
Delta compression using up to 8 threads
Compressing objects: 100% (15/15), done.
Writing objects: 100% (15/15), 5.23 KiB | 1.74 MiB/s, done.
Total 15 (delta 10), reused 0 (delta 0), pack-reused 0
To https://github.com/hongping-zh/circular-bias-detection.git
   abc1234..def5678  main -> main
```

---

### 第2步：构建Web App

```bash
# 1. 进入Web App目录
cd web-app

# 2. 安装依赖（首次或更新后需要）
npm install

# 3. 构建生产版本
npm run build
```

**预期输出：**
```
vite v7.1.7 building for production...
✓ 245 modules transformed.
dist/index.html                   0.81 kB │ gzip:  0.45 kB
dist/assets/index-abc123.css      8.24 kB │ gzip:  2.31 kB
dist/assets/index-def456.js     143.52 kB │ gzip: 46.23 kB
✓ built in 3.24s
```

---

### 第3步：部署到GitHub Pages

```bash
# 部署到gh-pages分支
npm run deploy
```

**预期输出：**
```
> web-app@1.0.0 predeploy
> npm run build

> web-app@1.0.0 deploy
> gh-pages -d dist

Published
```

---

## 🌐 验证部署

### 1. 检查GitHub仓库

访问: https://github.com/hongping-zh/circular-bias-detection

- ✅ `main`分支应包含所有新文件
- ✅ `gh-pages`分支应包含构建后的静态文件

### 2. 访问网站

**网站URL:** https://hongping-zh.github.io/circular-bias-detection/

⏰ **注意：** GitHub Pages通常需要1-3分钟更新。如果看不到更改，请：
- 等待几分钟
- 清除浏览器缓存（Ctrl+F5）
- 使用隐私/无痕模式打开

### 3. 验证新功能

在网站上检查：
- ✅ Bootstrap统计选项是否可用
- ✅ 上传`data/llm_eval_sample.csv`测试LLM支持
- ✅ 结果显示置信区间和p值
- ✅ 数据验证报告是否显示

---

## 🔧 常见问题排查

### 问题1：Git push失败

**错误信息：**
```
fatal: Authentication failed
```

**解决方案：**
1. 检查GitHub Personal Access Token是否有效
2. 重新配置凭据：
   ```bash
   git config --global user.name "hongping-zh"
   git config --global user.email "yujjam@uest.edu.gr"
   ```
3. 使用SSH替代HTTPS：
   ```bash
   git remote set-url origin git@github.com:hongping-zh/circular-bias-detection.git
   ```

---

### 问题2：npm install失败

**错误信息：**
```
npm ERR! network timeout
```

**解决方案：**
1. 使用国内镜像：
   ```bash
   npm config set registry https://registry.npmmirror.com
   ```
2. 或使用cnpm：
   ```bash
   npm install -g cnpm --registry=https://registry.npmmirror.com
   cnpm install
   ```

---

### 问题3：部署后网站没更新

**可能原因：**
- GitHub Pages缓存未清除
- 浏览器缓存
- 构建文件未正确上传

**解决方案：**
1. 检查gh-pages分支：
   ```bash
   git checkout gh-pages
   git log -1  # 查看最新提交时间
   git checkout main
   ```

2. 清除浏览器缓存：
   - Chrome: Ctrl+Shift+Delete
   - 选择"全部时间"
   - 勾选"缓存的图像和文件"
   - 点击"清除数据"

3. 强制重新部署：
   ```bash
   cd web-app
   npm run deploy -- -f  # 强制部署
   ```

---

### 问题4：构建失败

**错误信息：**
```
[vite]: Rollup failed to resolve import
```

**解决方案：**
1. 删除node_modules和重新安装：
   ```bash
   cd web-app
   rmdir /s /q node_modules
   npm install
   npm run build
   ```

2. 检查package.json版本兼容性：
   ```bash
   npm outdated
   npm update
   ```

---

## 📊 部署检查清单

部署前确认：

- [ ] 所有新文件已添加到Git
- [ ] 代码已在本地测试通过
- [ ] README.md已更新
- [ ] Web App依赖已安装（node_modules存在）
- [ ] 有GitHub仓库push权限

部署后验证：

- [ ] GitHub main分支包含最新提交
- [ ] gh-pages分支已更新（检查最新提交时间）
- [ ] 网站可访问（https://hongping-zh.github.io/circular-bias-detection/）
- [ ] 新功能在网站上正常工作
- [ ] 控制台无JavaScript错误

---

## 🎯 版本标签（可选）

为v1.1版本打标签以便追踪：

```bash
# 创建标签
git tag -a v1.1.0 -m "Version 1.1.0: Bootstrap, LLM support, visualizations"

# 推送标签
git push origin v1.1.0

# 查看所有标签
git tag -l
```

---

## 📞 获取帮助

如果遇到其他问题：

1. **查看GitHub Actions日志**
   - 访问: https://github.com/hongping-zh/circular-bias-detection/actions
   - 查看部署失败原因

2. **检查GitHub Pages设置**
   - Settings → Pages
   - Source应为"gh-pages分支"
   - Custom domain（如果有）应正确配置

3. **联系支持**
   - GitHub Issues: https://github.com/hongping-zh/circular-bias-detection/issues
   - Email: yujjam@uest.edu.gr

---

## 🎉 部署成功！

完成所有步骤后，您的v1.1增强版本将在以下位置可用：

- 🌐 **网站**: https://hongping-zh.github.io/circular-bias-detection/
- 📦 **代码**: https://github.com/hongping-zh/circular-bias-detection
- 📊 **数据**: https://doi.org/10.5281/zenodo.17201032

---

## 📈 后续步骤

部署完成后，考虑：

1. **分享更新**
   - 在Twitter/LinkedIn宣布v1.1发布
   - 更新论文预印本链接
   - 通知之前使用过的研究者

2. **监控使用**
   - GitHub Stars/Forks
   - 网站访问量（GitHub Insights）
   - 用户反馈（Issues）

3. **收集反馈**
   - 添加反馈表单到网站
   - 监控GitHub Issues
   - 与用户互动

---

**祝部署顺利！🚀**
