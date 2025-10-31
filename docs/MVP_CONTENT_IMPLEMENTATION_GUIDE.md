# MVP 网站内容实施指南

## 🎯 概述

本指南详细说明了如何实施�?CBD 项目�?MVP 网站准备的三个关键步骤：

1. **数据收集策略** - Hugging Face 数据集关键词和筛�?2. **语义重写构造泄�?* - Python 实现和演�?3. **案例研究文案** - "污染危机"完整内容和可视化

---

## 📁 新创建的文件结构

```
circular-bias-detection/
�?├── docs/
�?  ├── DATA_COLLECTION_STRATEGY.md          # 数据收集策略文档
�?  ├── CASE_STUDY_CONTAMINATION_CRISIS.md   # 案例研究完整文案
�?  └── MVP_CONTENT_IMPLEMENTATION_GUIDE.md  # 本指�?�?├── data/
�?  └── huggingface_data_collector.py        # HF 数据收集脚本
�?└── examples/
    ├── semantic_rewrite_leakage.py          # 语义重写实现
    └── generate_case_study_visualizations.py # 可视化生成器
```

---

## 🚀 快速开�?
### 步骤 1：安装依�?
```bash
# 基础依赖（已�?requirements.txt 中）
pip install numpy pandas matplotlib seaborn

# Hugging Face 数据集库
pip install datasets

# 语义嵌入模型（用于高级泄露检测）
pip install sentence-transformers

# 可选：加速计�?pip install scikit-learn
```

### 步骤 2：运行数据收�?
```bash
cd data
python huggingface_data_collector.py
```

**预期输出�?*
- `./collected_data/` 目录中的数据集文�?- `dataset_inventory.csv` - 数据集清�?- `collection_report.txt` - 收集报告

**运行时间�?* �?30-60 分钟（取决于网络速度和数据集大小�?
### 步骤 3：生成语义重写泄露示�?
```bash
cd examples
python semantic_rewrite_leakage.py
```

**预期输出�?*
```
============================================================
语义重写构造泄�?- 演示
============================================================

【示�?1】构造单个泄露对
----------------------------------------------------------------------
训练数据:
  The Statue of Liberty was a gift from the people of France...

泄露评估问题:
  The people of which nation presented the Statue of Liberty...

语义相似�? 0.875
表面相似�? 0.342
预期 C_score: 0.875 (🔴 CRITICAL)

【示�?2】批量模拟泄露数据集
----------------------------------------------------------------------
生成的数据集样本:
...

�?泄露数据集已保存�? leaked_dataset_sample.csv
```

### 步骤 4：生成案例研究可视化

```bash
cd examples
python generate_case_study_visualizations.py
```

**预期输出�?*
- `./case_study_figures/` 目录中的 PNG 图表
  - `contamination_risk_map.png`
  - `performance_reality_check.png`
  - `leakage_type_distribution.png`
  - `sample_contamination_heatmap.png`
- `contamination_data.csv` - 模拟数据

---

## 📊 详细实施步骤

### 一、数据收集关键词和策�?
#### 1.1 查看策略文档

打开并阅�?`docs/DATA_COLLECTION_STRATEGY.md`，该文档包含�?
- �?**策略 A**：交叉污染评估基准（机器翻译、摘要、问答、RAG�?- �?**策略 B**：训练集代表性样本（Wikipedia、C4/The Pile�?- �?**关键词列�?*：用�?Hugging Face 搜索
- �?**优先级数据集**：可直接下载的数据集列表

#### 1.2 自定义数据收�?
编辑 `data/huggingface_data_collector.py` 中的优先级数据集配置�?
```python
PRIORITY_DATASETS = {
    "qa": [
        {"id": "squad_v2", "name": "SQuAD v2.0", "risk": "high", ...},
        # 添加您自己的数据�?        {"id": "your_dataset_id", "name": "Your Dataset", "risk": "high", ...},
    ],
    ...
}
```

#### 1.3 执行收集

```python
from data.huggingface_data_collector import HuggingFaceDataCollector

# 初始�?collector = HuggingFaceDataCollector(output_dir="./my_collected_data")

# 创建清单
inventory = collector.create_dataset_inventory()

# 收集数据�?collected = collector.collect_all_priority_datasets(
    max_samples_per_dataset=1000,  # 每个数据集采样数�?    save_format="csv"
)

# 生成报告
report = collector.generate_collection_report(collected)
print(report)
```

---

### 二、语义重写构造泄�?
#### 2.1 理解核心概念

**目标�?* 构造表面不同但语义相似的数据对，以测试 CBD 的检测能力�?
**关键技术：**
- 同义词替�?- 句式重组（主�?�?被动�?- 释义生成

#### 2.2 使用语义重写�?
```python
from examples.semantic_rewrite_leakage import SemanticRewriter, LeakageSimulator

# 初始化重写器
rewriter = SemanticRewriter()

# 构造单个泄露对
train_text = "Your training data sentence here."
pair = rewriter.construct_leaked_pair(
    train_sentence=train_text,
    leakage_intensity=0.8  # 0=完全不同, 1=完全相同
)

print(f"训练文本: {pair.train_text}")
print(f"泄露问题: {pair.eval_question}")
print(f"语义相似�? {pair.semantic_similarity:.3f}")
print(f"表面相似�? {pair.surface_similarity:.3f}")
```

#### 2.3 批量模拟泄露数据�?
```python
# 初始化模拟器
simulator = LeakageSimulator()

# 模拟泄露数据�?df_leaked = simulator.simulate_leakage_dataset(
    num_samples=100,        # 样本数量
    leakage_ratio=0.4,      # 泄露样本比例�?0%�?    leakage_intensity=0.75  # 泄露强度
)

# 分析泄露分布
analysis = simulator.analyze_leakage_distribution(df_leaked)
print(f"泄露样本: {analysis['leaked_samples']}")
print(f"平均语义相似度（泄露�? {analysis['avg_semantic_sim_leaked']:.3f}")

# 保存数据�?df_leaked.to_csv("my_leaked_dataset.csv", index=False)
```

#### 2.4 �?CBD 框架集成

```python
from circular_bias_detector import BiasDetector

# 使用生成的泄露数据集测试 CBD
detector = BiasDetector()

# 准备数据矩阵（示例）
# 这里需要根据您的具体数据格式进行调�?performance_matrix = ...  # �?df_leaked 构建
constraint_matrix = ...    # 约束条件

# 检测偏�?results = detector.detect_bias(
    performance_matrix=performance_matrix,
    constraint_matrix=constraint_matrix
)

print(f"检测到偏差: {results['overall_bias']}")
```

---

### 三、案例研究文案和可视�?
#### 3.1 查看案例研究文档

打开 `docs/CASE_STUDY_CONTAMINATION_CRISIS.md`，该文档包含�?
- �?**执行摘要**：关键发现和商业影响
- �?**背景与动�?*：评估场景和初步结果
- �?**CBD 分析流程**：完整的 Python 代码示例
- �?**核心发现**：三大发现和数据支持
- �?**图表描述**：两个核心图表的详细规格
- �?**修正措施**：基�?CBD 发现的行动计�?
#### 3.2 生成可视�?
```python
from examples.generate_case_study_visualizations import CaseStudyVisualizer

# 初始化可视化�?visualizer = CaseStudyVisualizer(output_dir="./my_figures")

# 图表 1: 偏差分数分布
c_scores = np.random.beta(2, 5, 10000)  # 替换为您的真实数�?visualizer.generate_contamination_risk_map(
    c_scores=c_scores,
    save_path="risk_map.png"
)

# 图表 2: 性能修正对比
visualizer.generate_performance_reality_check(
    original_acc=95.1,
    corrected_acc=58.3,
    save_path="performance_check.png"
)

# 图表 3: 泄露类型分布
leakage_types = {
    'Exact Match': 120,
    'Paraphrase': 850,
    'Partial Overlap': 1530,
    'Semantic Similar': 1500
}
visualizer.generate_leakage_type_distribution(
    leakage_types=leakage_types,
    save_path="leakage_types.png"
)
```

#### 3.3 自定义可视化

编辑 `examples/generate_case_study_visualizations.py` 中的绘图函数，调整：

- 颜色方案
- 字体大小
- 标签文本
- 图例位置
- DPI 分辨�?
---

## 🌐 MVP 网站集成

### 将内容集成到网站的建�?
#### 1. 数据收集页面

**位置�?* `/data-collection` �?`/datasets`

**内容�?*
- 嵌入 `DATA_COLLECTION_STRATEGY.md` 的主要内�?- 添加交互式数据集搜索功能
- 提供数据集下载链�?
**代码示例（React）：**
```jsx
import React from 'react';

const DataCollectionPage = () => {
  return (
    <div className="container">
      <h1>Data Collection Strategy</h1>
      <section>
        <h2>Priority Datasets</h2>
        <DatasetTable datasets={priorityDatasets} />
      </section>
      <section>
        <h2>Quick Start</h2>
        <CodeBlock language="python">
          {`from datasets import load_dataset
dataset = load_dataset("squad_v2")`}
        </CodeBlock>
      </section>
    </div>
  );
};
```

#### 2. 案例研究页面

**位置�?* `/case-studies/contamination-crisis`

**内容�?*
- 显示 `CASE_STUDY_CONTAMINATION_CRISIS.md` 的内�?- 嵌入生成的可视化图表
- 添加交互式元素（如悬停显示详细信息）

**代码示例（React）：**
```jsx
const CaseStudyPage = () => {
  return (
    <div className="case-study">
      <h1>Contamination Crisis</h1>
      
      {/* 执行摘要 */}
      <section className="summary">
        <StatCard 
          title="Performance Drop"
          value="36.8%"
          icon={<TrendingDownIcon />}
        />
        <StatCard 
          title="Contaminated Samples"
          value="40%"
          icon={<AlertIcon />}
        />
      </section>
      
      {/* 图表 */}
      <section className="visualizations">
        <img 
          src="/figures/contamination_risk_map.png"
          alt="Risk Map"
          className="responsive-chart"
        />
        <img 
          src="/figures/performance_reality_check.png"
          alt="Performance Check"
          className="responsive-chart"
        />
      </section>
      
      {/* 详细分析 */}
      <section className="analysis">
        <Markdown content={caseStudyContent} />
      </section>
    </div>
  );
};
```

#### 3. 交互式演示页�?
**位置�?* `/demo/semantic-leakage`

**功能�?*
- 用户输入训练句子
- 实时生成泄露问题
- 显示相似度分�?- 可视化语义重写过�?
**代码示例（React）：**
```jsx
const SemanticLeakageDemo = () => {
  const [trainText, setTrainText] = useState('');
  const [leakedPair, setLeakedPair] = useState(null);
  
  const handleGenerate = async () => {
    const response = await fetch('/api/generate-leakage', {
      method: 'POST',
      body: JSON.stringify({ train_text: trainText }),
      headers: { 'Content-Type': 'application/json' }
    });
    const data = await response.json();
    setLeakedPair(data);
  };
  
  return (
    <div className="demo-container">
      <h2>Semantic Rewrite Demo</h2>
      
      <textarea
        value={trainText}
        onChange={(e) => setTrainText(e.target.value)}
        placeholder="Enter training data sentence..."
        rows={4}
      />
      
      <button onClick={handleGenerate}>Generate Leaked Question</button>
      
      {leakedPair && (
        <div className="results">
          <div className="result-card">
            <h3>Leaked Question</h3>
            <p>{leakedPair.eval_question}</p>
          </div>
          
          <div className="similarity-scores">
            <ScoreBar 
              label="Semantic Similarity"
              value={leakedPair.semantic_similarity}
              color={leakedPair.semantic_similarity > 0.75 ? 'red' : 'green'}
            />
            <ScoreBar 
              label="Surface Similarity"
              value={leakedPair.surface_similarity}
              color="blue"
            />
          </div>
        </div>
      )}
    </div>
  );
};
```

---

## 📈 后端 API 集成

### API 端点建议

#### 1. 数据收集 API

```python
# backend/routes/data_collection.py
from flask import Blueprint, request, jsonify
from data.huggingface_data_collector import HuggingFaceDataCollector

data_bp = Blueprint('data', __name__)

@data_bp.route('/api/datasets/search', methods=['POST'])
def search_datasets():
    """搜索 Hugging Face 数据�?""
    keywords = request.json.get('keywords', [])
    collector = HuggingFaceDataCollector()
    results = collector.search_datasets_by_keyword(keywords, limit=50)
    return jsonify({'datasets': results})

@data_bp.route('/api/datasets/inventory', methods=['GET'])
def get_inventory():
    """获取数据集清�?""
    collector = HuggingFaceDataCollector()
    inventory = collector.create_dataset_inventory()
    return jsonify(inventory.to_dict('records'))
```

#### 2. 语义重写 API

```python
# backend/routes/semantic_rewrite.py
from flask import Blueprint, request, jsonify
from examples.semantic_rewrite_leakage import SemanticRewriter

rewrite_bp = Blueprint('rewrite', __name__)

@rewrite_bp.route('/api/generate-leakage', methods=['POST'])
def generate_leakage():
    """生成泄露数据�?""
    train_text = request.json.get('train_text', '')
    intensity = request.json.get('intensity', 0.75)
    
    rewriter = SemanticRewriter()
    pair = rewriter.construct_leaked_pair(train_text, intensity)
    
    return jsonify({
        'train_text': pair.train_text,
        'eval_question': pair.eval_question,
        'eval_question_clean': pair.eval_question_clean,
        'semantic_similarity': float(pair.semantic_similarity),
        'surface_similarity': float(pair.surface_similarity),
        'leakage_type': pair.leakage_type
    })

@rewrite_bp.route('/api/simulate-dataset', methods=['POST'])
def simulate_dataset():
    """模拟泄露数据�?""
    num_samples = request.json.get('num_samples', 100)
    leakage_ratio = request.json.get('leakage_ratio', 0.4)
    
    simulator = LeakageSimulator()
    df = simulator.simulate_leakage_dataset(num_samples, leakage_ratio)
    
    return jsonify(df.to_dict('records'))
```

#### 3. 可视化生�?API

```python
# backend/routes/visualizations.py
from flask import Blueprint, send_file, request
from examples.generate_case_study_visualizations import CaseStudyVisualizer
import io

viz_bp = Blueprint('viz', __name__)

@viz_bp.route('/api/visualizations/risk-map', methods=['POST'])
def generate_risk_map():
    """生成风险分布�?""
    c_scores = request.json.get('c_scores', [])
    
    visualizer = CaseStudyVisualizer(output_dir="./temp")
    visualizer.generate_contamination_risk_map(
        c_scores=np.array(c_scores),
        save_path="risk_map.png"
    )
    
    return send_file(
        "./temp/risk_map.png",
        mimetype='image/png',
        as_attachment=False
    )
```

---

## 🧪 测试和验�?
### 单元测试

创建 `tests/test_new_features.py`�?
```python
import unittest
import numpy as np
from data.huggingface_data_collector import HuggingFaceDataCollector
from examples.semantic_rewrite_leakage import SemanticRewriter, LeakageSimulator
from examples.generate_case_study_visualizations import CaseStudyVisualizer

class TestDataCollection(unittest.TestCase):
    
    def setUp(self):
        self.collector = HuggingFaceDataCollector(output_dir="./test_data")
    
    def test_search_datasets(self):
        results = self.collector.search_datasets_by_keyword(['qa'], limit=5)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
    
    def test_create_inventory(self):
        inventory = self.collector.create_dataset_inventory()
        self.assertGreater(len(inventory), 0)

class TestSemanticRewrite(unittest.TestCase):
    
    def setUp(self):
        self.rewriter = SemanticRewriter()
    
    def test_construct_leaked_pair(self):
        train_text = "Test sentence for rewriting."
        pair = self.rewriter.construct_leaked_pair(train_text, 0.7)
        
        self.assertIsNotNone(pair.eval_question)
        self.assertGreater(pair.semantic_similarity, 0)
        self.assertLess(pair.surface_similarity, 1)

class TestVisualizations(unittest.TestCase):
    
    def setUp(self):
        self.visualizer = CaseStudyVisualizer(output_dir="./test_figures")
    
    def test_generate_risk_map(self):
        c_scores = np.random.beta(2, 5, 100)
        self.visualizer.generate_contamination_risk_map(c_scores, "test_map.png")
        
        # 验证文件生成
        import os
        self.assertTrue(os.path.exists("./test_figures/test_map.png"))

if __name__ == '__main__':
    unittest.main()
```

运行测试�?```bash
python -m pytest tests/test_new_features.py -v
```

---

## 📝 文档和维�?
### 更新�?README

�?`README.md` 中添加新功能的链接：

```markdown
## 🆕 New Features

### Data Collection Strategy
Learn how to collect high-risk evaluation datasets from Hugging Face. 
[Read the guide →](docs/DATA_COLLECTION_STRATEGY.md)

### Semantic Leakage Construction
Understand how to construct subtle data leakage for testing CBD.
[See examples →](examples/semantic_rewrite_leakage.py)

### Case Study: Contamination Crisis
Explore a real-world case study showing CBD's impact.
[Read the full case study →](docs/CASE_STUDY_CONTAMINATION_CRISIS.md)
```

### 创建变更日志

�?`CHANGELOG.md` 中添加：

```markdown
## [Unreleased]

### Added
- Data collection strategy for Hugging Face datasets
- Semantic rewrite module for leakage construction
- Case study: Contamination Crisis with complete documentation
- Visualization generator for case study figures
- API endpoints for data collection and semantic rewriting

### Documentation
- DATA_COLLECTION_STRATEGY.md - Comprehensive data collection guide
- CASE_STUDY_CONTAMINATION_CRISIS.md - Full case study documentation
- MVP_CONTENT_IMPLEMENTATION_GUIDE.md - Implementation guide
```

---

## 🎯 下一步行�?
### 优先级任务清�?
- [ ] **高优先级**
  - [ ] 运行所有三个脚本，验证输出
  - [ ] 生成真实的可视化图表
  - [ ] 将图表集成到 MVP 网站

- [ ] **中优先级**
  - [ ] 下载 2-3 �?Hugging Face 数据集进行初步测�?  - [ ] 编写 API 端点并进行集成测�?  - [ ] 创建交互式演示页�?
- [ ] **低优先级**
  - [ ] 优化可视化的颜色和样�?  - [ ] 添加多语言支持（中�?英文�?  - [ ] 编写更多单元测试

### 时间估算

| 任务 | 估计时间 |
|------|----------|
| 验证所有脚�?| 2-3 小时 |
| 集成到网站前�?| 4-6 小时 |
| 后端 API 开�?| 3-4 小时 |
| 测试和调�?| 2-3 小时 |
| 文档完善 | 1-2 小时 |
| **总计** | **12-18 小时** |

---

## 🆘 故障排除

### 常见问题

**Q1: Hugging Face 数据集下载失�?*
```bash
# 解决方案：设置代理或使用镜像
export HF_ENDPOINT=https://hf-mirror.com
```

**Q2: 可视化生成时中文显示为方�?*
```python
# 解决方案：安装中文字�?import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
```

**Q3: 内存不足错误（大数据集）**
```python
# 解决方案：使用流式加�?from datasets import load_dataset
dataset = load_dataset("dataset_id", streaming=True)
```

---

## 📞 支持和反�?
如有问题或建议，请联系：

- **邮箱�?* yujjam@uest.edu.gr
- **GitHub Issues�?* [提交问题](https://github.com/hongping-zh/circular-bias-detection/issues)

---

**文档版本�?* v1.0  
**最后更新：** 2024-10-27  
**作者：** Hongping Zhang
