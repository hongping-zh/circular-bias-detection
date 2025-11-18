# Latest Dataset Feature - Web App Integration

## 功能概述

在 Web App 首页添加了显著的"Try with Latest Dataset"横幅，让用户可以一键加载 CBD Dataset v3/v3.1 (Zenodo 17637303)。

## 实现的功能

### 1. 醒目的横幅设计 🎨

位置：DataInput 组件之后，ScanButton 之前

设计特点：
- 渐变紫色背景（品牌色）
- 🆕 新发布图标
- 清晰的标题和描述
- 醒目的白色按钮
- Zenodo 链接

### 2. URL 参数支持 🔗

用户可以通过以下 URL 直接加载最新数据集：

```
https://is.gd/check_sleuth?dataset=latest
https://is.gd/check_sleuth?dataset=17637303
```

### 3. 一键加载功能 ⚡

点击"→ Load in Web App"按钮：
- 自动加载 CBD Dataset v3/v3.1 示例数据
- 包含真实的评估场景
- 立即可以运行分析

## 用户体验流程

### 方式 1: 手动点击
1. 访问 https://is.gd/check_sleuth
2. 看到醒目的紫色横幅
3. 点击"→ Load in Web App"按钮
4. 数据自动加载
5. 点击"Scan for Bias"开始分析

### 方式 2: URL 参数
1. 访问 https://is.gd/check_sleuth?dataset=latest
2. 页面加载完成后自动加载数据集
3. 直接点击"Scan for Bias"开始分析

## 技术实现

### 文件修改
- **web-app/src/App.jsx**
  - 新增 `handleLoadLatestDataset()` 函数
  - 新增 URL 参数检测 useEffect
  - 新增横幅 UI 组件
  - 更新 footer 链接

### 数据示例
```csv
time_period,algorithm,performance,constraint_compute,constraint_memory,constraint_dataset_size,evaluation_protocol
1,ResNet-50,0.762,512,8.0,50000,v3.1
1,VGG-16,0.719,512,8.0,50000,v3.1
...
```

### 横幅样式
```jsx
{
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  borderRadius: '12px',
  padding: '1.5rem',
  color: 'white',
  boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
}
```

## 视觉效果

```
┌─────────────────────────────────────────────────────────┐
│ 🆕 Just Released: 2025 Real-World Evaluation Dataset   │
│                                                         │
│ Test bias detection on our latest CBD Dataset v3/v3.1  │
│ with real-world AI evaluation scenarios                │
│                                                         │
│ [→ Load in Web App]  View on Zenodo →                  │
└─────────────────────────────────────────────────────────┘
```

## 分享链接

### 社交媒体
```
🔍 Try Sleuth with our latest 2025 dataset!
Test bias detection on real-world AI evaluations.
👉 https://is.gd/check_sleuth?dataset=latest
```

### 文档引用
```markdown
Try the latest dataset: [Load CBD Dataset v3/v3.1](https://is.gd/check_sleuth?dataset=latest)
```

### Email/Newsletter
```
🆕 New Feature: One-click access to our 2025 real-world evaluation dataset

Visit: https://is.gd/check_sleuth?dataset=latest
```

## 测试清单

- ✅ 横幅在首页显著位置显示
- ✅ 点击按钮成功加载数据
- ✅ URL 参数 `?dataset=latest` 自动加载
- ✅ URL 参数 `?dataset=17637303` 自动加载
- ✅ Zenodo 链接正确跳转
- ✅ 按钮悬停效果正常
- ✅ Footer 更新显示最新数据集
- ✅ 移动端响应式显示正常

## 后续优化建议

### 短期
1. 添加加载动画/进度提示
2. 添加数据集预览功能
3. 支持更多 URL 参数（如 `?example=llm`）

### 中期
1. 从 Zenodo API 实时获取数据
2. 支持选择不同版本的数据集
3. 添加数据集统计信息展示

### 长期
1. 数据集市场/浏览器
2. 用户上传数据集到 Zenodo
3. 社区贡献的数据集集合

## 相关链接

- **Web App**: https://is.gd/check_sleuth
- **With Latest Dataset**: https://is.gd/check_sleuth?dataset=latest
- **Zenodo Record**: https://doi.org/10.5281/zenodo.17637303
- **GitHub**: https://github.com/hongping-zh/circular-bias-detection

## 引用

如果在论文或博客中提到此功能：

```
The Sleuth web application now features one-click access to the CBD 
Dataset v3/v3.1 (DOI: 10.5281/zenodo.17637303), allowing users to 
immediately test bias detection on real-world AI evaluation scenarios.
```

---

**实现日期**: 2025-11-18  
**版本**: v1.0  
**状态**: ✅ 已完成并测试
