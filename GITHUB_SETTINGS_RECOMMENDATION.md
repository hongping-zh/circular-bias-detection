# GitHub 仓库设置建议

## 📝 Repository Settings

为了与品牌统一策略保持一致，建议更新以下GitHub仓库设置：

---

## 1. About Section (关于部分)

### 当前设置位置
GitHub仓库页面右上角 → Settings → 或直接在仓库首页点击 ⚙️ 编辑

### 建议内容

**Description (描述)**：
```
Sleuth - Detect circular bias in AI evaluations. 30-second automated testing with PSI, CCS, ρ_PC indicators.
```

**Website (网站)**：
```
https://is.gd/check_sleuth
```

**Topics (主题标签)**：
```
bias-detection
ai-evaluation
machine-learning
reproducibility
fairness
benchmark-integrity
llm-evaluation
algorithm-fairness
python
web-app
```

---

## 2. Social Preview (社交预览卡片)

### 设置路径
Settings → General → Social Preview

### 建议内容

**Title**: Sleuth - AI Bias Detector  
**Description**: Detect circular bias in AI evaluations instantly. Free web app + Python SDK.

如果有设计资源，可以创建 1200x630 的预览图，包含：
- 🔍 Logo/Icon
- "Sleuth" 品牌名
- 核心功能点（PSI, CCS, ρ_PC）
- "30-Second Bias Detection"

---

## 3. README Badges (徽章)

### 当前徽章 ✅
已经包含了关键徽章，位置合理

### 可选额外徽章
```markdown
[![Downloads](https://static.pepy.tech/badge/circular-bias-detector)](https://pepy.tech/project/circular-bias-detector)
[![Powered by Sleuth](https://img.shields.io/badge/🔍-Powered%20by%20Sleuth-brightgreen)](https://is.gd/check_sleuth)
```

---

## 4. Repository Labels (问题标签)

建议添加以下标签以更好地组织Issues：

| Label | Color | Description |
|-------|-------|-------------|
| `enhancement` | #a2eeef | New feature request |
| `bug` | #d73a4a | Something isn't working |
| `documentation` | #0075ca | Documentation improvements |
| `web-app` | #1d76db | Related to web application |
| `python-sdk` | #3572A5 | Related to Python library |
| `cli` | #000000 | Command-line interface |
| `good first issue` | #7057ff | Good for newcomers |
| `help wanted` | #008672 | Extra attention needed |
| `question` | #d876e3 | Further information requested |
| `bias-detection` | #fbca04 | Core detection algorithm |

---

## 5. Repository Features

### 在 Settings → General 中启用：

- ✅ **Issues** (已启用)
- ✅ **Discussions** (考虑启用 - 用于社区讨论)
- ✅ **Wiki** (可选 - 如果需要更详细的文档)
- ❌ Projects (可选 - 项目管理)
- ❌ Sponsorships (可选 - 如果接受赞助)

---

## 6. Pull Request Template

### 创建文件：`.github/PULL_REQUEST_TEMPLATE.md`

```markdown
## Description
<!-- 描述你的更改 -->

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass

## Related Issues
Closes #

## Screenshots (if applicable)
```

---

## 7. Issue Templates

### 创建文件：`.github/ISSUE_TEMPLATE/bug_report.md`

```markdown
---
name: Bug Report
about: Report a bug in Sleuth
title: '[BUG] '
labels: bug
---

## Bug Description
<!-- 清晰描述bug -->

## Steps to Reproduce
1. 
2. 
3. 

## Expected Behavior
<!-- 预期的行为 -->

## Actual Behavior
<!-- 实际发生的情况 -->

## Environment
- OS: [e.g., Windows 11]
- Python Version: [e.g., 3.9]
- Package Version: [e.g., 1.2.0]
- Installation Method: [pip / source / web app]

## Additional Context
<!-- 截图、日志等 -->
```

### 创建文件：`.github/ISSUE_TEMPLATE/feature_request.md`

```markdown
---
name: Feature Request
about: Suggest a feature for Sleuth
title: '[FEATURE] '
labels: enhancement
---

## Feature Description
<!-- 描述你想要的功能 -->

## Use Case
<!-- 为什么需要这个功能？谁会受益？ -->

## Proposed Solution
<!-- 你认为应该如何实现？ -->

## Alternatives Considered
<!-- 你考虑过其他方案吗？ -->

## Additional Context
<!-- 其他相关信息 -->
```

---

## 8. GitHub Actions (CI/CD)

### 当前状态
已有 CI workflow (看到了 CI badge)

### 建议增强
检查 `.github/workflows/ci.yml` 是否包含：
- ✅ 自动化测试
- ✅ 代码覆盖率报告
- ⚠️ 自动发布到PyPI (release时)
- ⚠️ 文档自动构建

---

## 9. Zenodo集成

### 当前状态 ✅
- 已有 `.zenodo.json`
- 已有DOI徽章

### 建议
确保每次release时Zenodo自动归档：
- 在Zenodo中启用GitHub集成
- 每次打tag时自动创建新版本

---

## 10. README Sections建议

### 当前README ✅ 已经很完善

### 可选改进
考虑添加：
```markdown
## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=hongping-zh/circular-bias-detection&type=Date)](https://star-history.com/#hongping-zh/circular-bias-detection&Date)
```

---

## 快速操作清单

### 立即可做（5分钟）
- [ ] 更新Repository About描述
- [ ] 添加Website链接
- [ ] 添加Topics标签

### 近期可做（30分钟）
- [ ] 创建Issue模板
- [ ] 创建PR模板
- [ ] 添加Labels

### 长期考虑
- [ ] 设计社交预览图
- [ ] 启用Discussions
- [ ] 完善CI/CD流程

---

## 注意事项

1. **Repository名称**：建议保持 `circular-bias-detection` 不变
   - GitHub允许多次重命名，但会影响：
     - 现有的Git clones
     - 外部链接（文章、论文引用）
     - DOI记录
   
2. **About描述**：这是最容易修改且影响最大的
   - 出现在搜索结果中
   - 出现在社交分享中
   - 0破坏性

3. **Topics标签**：帮助项目被发现
   - 用户搜索 `bias-detection` 时能找到
   - 推荐到相关用户

---

**优先级排序**：
1. 🔥 **高**: About描述 + Topics（5分钟，高影响）
2. 📝 **中**: Issue/PR模板（提升贡献者体验）
3. 🎨 **低**: 社交预览图（需要设计资源）

---

**实施建议**：从About描述和Topics开始，这是最简单且最有效的改进。
