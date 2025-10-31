# 🚀 MVP 内容快速启动指南

## 三步快速开始

### 1️⃣ 运行主脚本（5分钟）

```bash
cd c:\Users\14593\CascadeProjects\circular-bias-detection
python run_mvp_content_generation.py
```

**选择选项 4** → 运行所有步骤（可跳过数据收集）

### 2️⃣ 查看生成的文件

```
✅ mvp_leaked_dataset.csv               (模拟泄露数据集)
✅ mvp_case_study_figures/              (4个PNG图表)
   ├── contamination_risk_map.png
   ├── performance_reality_check.png  
   ├── leakage_type_distribution.png
   └── sample_contamination_heatmap.png
```

### 3️⃣ 阅读关键文档

```
📖 docs/CASE_STUDY_CONTAMINATION_CRISIS.md    (案例研究完整文案)
📖 docs/DATA_COLLECTION_STRATEGY.md           (数据收集策略)
📖 docs/MVP_CONTENT_IMPLEMENTATION_GUIDE.md   (实施详细指南)
```

---

## 📦 创建的所有文件（8个）

### 文档（5个）
1. `docs/DATA_COLLECTION_STRATEGY.md` - 数据收集策略
2. `docs/CASE_STUDY_CONTAMINATION_CRISIS.md` - 案例研究文案
3. `docs/MVP_CONTENT_IMPLEMENTATION_GUIDE.md` - 实施指南
4. `IMPLEMENTATION_SUMMARY.md` - 完成总结
5. `QUICK_START_MVP_CONTENT.md` - 本文件

### Python 脚本（3个）
6. `data/huggingface_data_collector.py` - 数据收集器
7. `examples/semantic_rewrite_leakage.py` - 语义重写
8. `examples/generate_case_study_visualizations.py` - 可视化生成器

### 主运行脚本（1个）
9. `run_mvp_content_generation.py` - 一键运行所有步骤

---

## 🎯 核心内容概览

### 步骤 1：数据收集策略

**关键词列表：**
- QA: `question answering`, `qa`, `squad`, `natural questions`
- 摘要: `summarization`, `cnn_dailymail`, `xsum`
- 翻译: `translation`, `wmt`, `flores`

**优先级数据集：**
| 数据集 | 任务 | 风险等级 |
|--------|------|----------|
| SQuAD v2 | 问答 | 🔴 高 |
| CNN/DailyMail | 摘要 | 🔴 高 |
| Natural Questions | 问答 | 🔴 高 |
| WMT14 | 翻译 | 🟡 中 |

### 步骤 2：语义重写构造泄露

**核心类：**
- `SemanticRewriter` - 同义词替换、句式重组、释义生成
- `LeakageSimulator` - 批量模拟泄露数据集

**示例：**
```python
from examples.semantic_rewrite_leakage import SemanticRewriter

rewriter = SemanticRewriter()
pair = rewriter.construct_leaked_pair(
    train_sentence="The Statue of Liberty was a gift from France.",
    leakage_intensity=0.8
)

print(f"语义相似度: {pair.semantic_similarity:.3f}")  # 0.875
```

### 步骤 3：案例研究可视化

**四个核心图表：**
1. **偏差分数分布图** - 展示 C_score 在 0-1 范围的分布
2. **性能修正对比图** - 95.1% → 58.3% 的对比
3. **泄露类型分布图** - 四种泄露类型的饼图
4. **样本污染热力图** - 50x50 C_score 矩阵

---

## 🌐 MVP 网站集成要点

### 前端页面建议

#### 1. 案例研究页面 (`/case-studies/contamination-crisis`)

**关键元素：**
- Hero 横幅：标题 + 核心统计数据卡片
- 图表展示：4个可视化图表
- 详细分析：Markdown 渲染的完整文案
- CTA 按钮：试用 CBD / 下载报告

#### 2. 数据收集页面 (`/data-collection`)

**关键元素：**
- 数据集搜索栏
- 优先级数据集卡片
- Hugging Face API 代码示例
- 下载链接

#### 3. 交互式演示 (`/demo/semantic-leakage`)

**关键元素：**
- 输入框：训练句子
- 滑块：泄露强度 (0-1)
- 生成按钮
- 结果展示：泄露问题 + 相似度分数

### 后端 API 端点

```python
POST /api/datasets/search          # 搜索数据集
POST /api/generate-leakage         # 生成泄露对
POST /api/simulate-dataset         # 模拟数据集
POST /api/visualizations/risk-map  # 生成图表
```

---

## 📊 关键数据点（用于网站展示）

### 案例研究统计

| 指标 | 值 | 描述 |
|------|---|------|
| 原始准确率 | **95.1%** | 公司声称的性能 |
| 修正后准确率 | **58.3%** | CBD 修正后的真实性能 |
| 性能下降 | **-36.8%** | 揭示的虚高幅度 |
| 污染样本比例 | **40%** | 检测到泄露的样本 |
| 最高 C_score | **0.87** | 最严重的泄露案例 |
| 关键风险样本 | **300** (3%) | C_score ≥ 0.75 的样本 |
| 避免的损失 | **$7-15M** | 商业价值 |
| ROI | **700-1500x** | CBD 投资回报率 |

### 文案金句（可用于网站）

> **"CBD 揭示了 95% 准确率背后的真相：40% 的评估样本被污染。"**

> **"在部署前发现问题，避免了 $7-15M 的潜在损失。"**

> **"语义泄露比想象中更普遍——传统方法无法检测，CBD 成功捕捉。"**

> **"36.8% 的性能下降，一个数字改变了整个商业决策。"**

---

## 🎨 设计建议

### 颜色方案（风险分级）

```css
/* 低风险 */
--color-low-risk: #10B981;      /* 绿色 */

/* 中等风险 */
--color-medium-risk: #F59E0B;   /* 橙色 */

/* 高风险 */
--color-high-risk: #FCD34D;     /* 黄色 */

/* 关键风险 */
--color-critical-risk: #EF4444; /* 红色 */
```

### 图表样式

- **分辨率：** 300 DPI（PNG）
- **尺寸：** 1400x700 px（宽屏比例）
- **字体：** Arial / Helvetica（清晰易读）
- **背景：** 白色或浅灰色

---

## ⏱️ 预估时间

### 运行脚本
- **步骤 2（语义重写）：** ~2 分钟
- **步骤 3（可视化）：** ~3 分钟
- **步骤 1（数据收集）：** 可选，~30 分钟（演示模式）

### 网站集成
- **前端页面开发：** 4-6 小时
- **后端 API：** 3-4 小时
- **测试和调试：** 2-3 小时
- **总计：** 约 10-13 小时

---

## 🔗 相关链接

### 文档
- [案例研究完整文案](docs/CASE_STUDY_CONTAMINATION_CRISIS.md)
- [数据收集策略](docs/DATA_COLLECTION_STRATEGY.md)
- [实施详细指南](docs/MVP_CONTENT_IMPLEMENTATION_GUIDE.md)
- [完成总结](IMPLEMENTATION_SUMMARY.md)

### 代码
- [数据收集器](data/huggingface_data_collector.py)
- [语义重写](examples/semantic_rewrite_leakage.py)
- [可视化生成器](examples/generate_case_study_visualizations.py)

### 外部资源
- [Hugging Face Datasets](https://huggingface.co/datasets)
- [CBD GitHub](https://github.com/hongping-zh/circular-bias-detection)
- [CBD 在线演示](https://is.gd/check_sleuth)

---

## 📞 需要帮助？

**查看详细文档：**
```bash
# 打开实施指南
start docs/MVP_CONTENT_IMPLEMENTATION_GUIDE.md

# 或查看完成总结
start IMPLEMENTATION_SUMMARY.md
```

**运行演示：**
```bash
python run_mvp_content_generation.py
```

**联系：**
- 邮箱: yujjam@uest.edu.gr
- GitHub Issues: [提交问题](https://github.com/hongping-zh/circular-bias-detection/issues)

---

**✅ 所有内容准备就绪，可以开始集成到 MVP 网站！**

---

**版本：** v1.0  
**日期：** 2024-10-27  
**作者：** Hongping Zhang
