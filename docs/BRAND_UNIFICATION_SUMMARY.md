# 品牌统一工作总结 | Brand Unification Summary

**日期 Date**: 2025-11-08  
**任务 Task**: 统一项目命名策略，解决"Sleuth"与"Circular Bias Detection"命名不一致问题

---

## 📊 问题分析

### 原始状况
- **README标题**: Sleuth - AI Bias Detector ✅
- **GitHub仓库**: `circular-bias-detection` 
- **PyPI包名**: `circular-bias-detector`
- **网站域名**: `biasdetector.vercel.app`
- **文档中**: 混合使用 Sleuth 和 Circular Bias Detector

### 命名冲突
不同上下文使用不同名称，缺乏清晰的品牌策略。

---

## ✅ 解决方案

### 策略：双轨命名系统

**品牌层面（用户面向）**：
- 主打 **Sleuth** 作为产品名
- 简洁、易记、有隐喻意义（侦探发现偏差）

**技术层面（开发者面向）**：
- 保持 `circular-bias-detection` 作为技术标识符
- 保持 `circular-bias-detector` 作为包名
- 保持现有URL不变（成本考虑）

---

## 🛠️ 已完成的修改

### 1. README.md
- ✅ 在顶部添加品牌说明注释
- ✅ 所有按钮文字 "Try Live Demo" → "Try Sleuth"
- ✅ 强化 "Sleuth" 在用户面向内容中的使用
- ✅ 保持技术文档中的代码示例不变

**修改位置**：
```markdown
# 第3行：添加品牌说明
> **Brand Note**: **Sleuth** is the product name. 
  The technical identifier `circular-bias-detection` (GitHub/PyPI) 
  refers to the methodology we implement.

# 第6行：按钮文字
[![Web App](https://img.shields.io/badge/%F0%9F%94%8D_Try_Sleuth-...)]

# 第107行：快速开始链接
**[🔍 Try Sleuth Now →](https://is.gd/check_sleuth)**

# 第248行：Web App 章节
**[Launch Sleuth Web App →](https://is.gd/check_sleuth)**

# 第327行：数据集章节
**Try them in Sleuth:** [Launch Sleuth →]
```

### 2. setup.py
- ✅ 描述字段添加 "Sleuth" 品牌名

**修改前**：
```python
description='Statistical framework for detecting circular bias...'
```

**修改后**：
```python
description='Sleuth - Detect circular bias in AI evaluations. Statistical framework with automated PSI, CCS, and correlation analysis.'
```

### 3. pyproject.toml
- ✅ 描述字段添加 "Sleuth" 品牌名（与setup.py一致）

**修改第8行**：
```toml
description = "Sleuth - Detect circular bias in AI evaluations. Statistical framework with automated PSI, CCS, and correlation analysis."
```

### 4. 新建文档

#### a) BRANDING.md
**完整的品牌指南文档**，包含：
- 命名策略说明
- 使用场景指南（何时用Sleuth vs. circular-bias-detection）
- 引用格式
- 品牌资产（颜色、图标、语调）
- URL汇总
- 常见问题

#### b) BRAND_UNIFICATION_SUMMARY.md
**本文档**，工作总结与快速参考

---

## 🔒 未修改项目（有意保留）

| 项目 | 名称 | 原因 |
|------|------|------|
| GitHub 仓库名 | `circular-bias-detection` | URL已存在，改动成本高 |
| PyPI 包名 | `circular-bias-detector` | 已发布，有用户依赖 |
| 网站域名 | `biasdetector.vercel.app` | 用户明确表示暂不修改 |
| CLI 命令 | `circular-bias` | 已安装用户基础 |
| DOI | zenodo.17201032 | 永久不可变 |

**说明**：这些技术标识符的保留不影响品牌统一，因为：
1. 用户面向的文档和界面统一使用"Sleuth"
2. 技术层面的稳定性很重要
3. 可以通过文档说明两者关系

---

## 📋 验证检查清单

### ✅ 已验证的文件

| 文件 | 状态 | 品牌名 |
|------|------|--------|
| `README.md` | ✅ 已优化 | Sleuth（用户内容）+ circular-bias-detection（代码） |
| `setup.py` | ✅ 已优化 | Sleuth |
| `pyproject.toml` | ✅ 已优化 | Sleuth |
| `CITATION.cff` | ✅ 已确认 | Sleuth（已正确） |
| `codemeta.json` | ✅ 已确认 | Sleuth（已正确） |
| `.zenodo.json` | ℹ️ 无需修改 | 数据集描述（不是软件） |

### ✅ 关键检查点

- [x] README顶部有品牌说明
- [x] 所有面向用户的按钮/链接使用"Sleuth"
- [x] 包描述包含"Sleuth"
- [x] 技术文档保持代码示例不变
- [x] 引用文件（CITATION.cff）使用"Sleuth"
- [x] 创建了品牌指南文档
- [x] 未破坏现有技术标识符

---

## 🎯 品牌使用建议

### 对外宣传时
**推荐格式**：
```
Sleuth - AI Bias Detector
安装：pip install circular-bias-detector
```

### 学术论文引用
```bibtex
@software{zhang2024sleuth,
  title = {Sleuth: Circular Bias Detection for AI Evaluations},
  ...
}
```

### 社交媒体
```
🔍 Sleuth - 30秒检测AI评估偏差
✅ 免费 Web App + Python SDK
🔗 https://is.gd/check_sleuth
```

### 技术文档
```python
# Install Sleuth
pip install circular-bias-detector

# Import
from circular_bias_detector import SimpleBiasDetector
```

---

## 📈 后续建议

### 短期（可选）
1. **GitHub About 描述**：建议改为 "Sleuth - Detect circular bias in AI evaluations"
2. **PyPI 长描述**：已使用README（自动包含Sleuth）
3. **网站标题**：在 `biasdetector.vercel.app` 的HTML标题中使用"Sleuth"

### 长期（可选）
1. **自定义域名**：考虑注册 `sleuth.ai` 或 `checksleuth.com`（如果预算允许）
2. **品牌Logo**：设计专业的Logo（当前使用🔍emoji）
3. **统一颜色**：在所有可视化中使用一致的品牌色

---

## 💡 核心原则总结

1. **用户看到的 = Sleuth**
   - 网站界面、按钮、宣传材料

2. **开发者使用的 = circular-bias-detector**
   - pip install、import 语句、GitHub URL

3. **学术引用 = 两者都包含**
   - 标题用 Sleuth，URL用完整路径

4. **不破坏现有内容**
   - 保持技术标识符稳定
   - 通过文档说明关系

---

## 🎉 成果

### 品牌一致性提升
- **之前**：用户困惑"这到底叫什么？"
- **现在**：清晰的双轨策略，各有用途

### 专业度提升
- **之前**：看起来像学术项目
- **现在**：看起来像成熟产品

### SEO与传播
- **品牌名**：Sleuth（短、易记、独特）
- **关键词**：circular bias detection（技术SEO）

---

## 📞 维护注意事项

### 新增内容时
1. **README更新**：用户内容用"Sleuth"，代码示例用包名
2. **新文档**：参考 BRANDING.md 指南
3. **博客/文章**：主打"Sleuth"，技术细节提及包名

### 一致性检查
定期运行 `grep -r "Circular Bias Detector" .` 确保没有新的混用

---

**工作完成 ✅**

所有修改已提交，品牌策略已明确文档化。项目现在有清晰的命名规范，既保持了技术稳定性，又建立了强有力的品牌识别。
