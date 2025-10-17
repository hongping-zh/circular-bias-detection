# 🎯 Sleuth Phase 1 行动计划

## 目标：v1.0打磨 + 学术推广 + 早期用户

**时间线：** 2025年10月15日 - 2025年11月15日（1个月）  
**当前状态：** v1.0已发布（mock模式）  
**核心目标：** 真实可用 + 建立口碑

---

## 📊 三大任务

### 任务1: 完成真实Python后端 (60% 工作量)
### 任务2: 学术推广 (25% 工作量)
### 任务3: 获得早期用户 (15% 工作量)

---

## 🛠️ 任务1: 完成真实Python后端

### 目标
将当前的**mock detection**替换为**真实的Python统计计算**

### 子任务分解

#### 1.1 Python后端实现 (估时: 2天)

**文件结构：**
```
backend/
├── app.py                 # Flask/FastAPI主服务
├── core/
│   ├── __init__.py
│   ├── psi_calculator.py  # PSI计算
│   ├── ccs_calculator.py  # CCS计算
│   ├── rho_pc_calculator.py  # ρ_PC计算
│   ├── bootstrap.py       # Bootstrap重采样
│   └── bias_scorer.py     # CBS综合评分
├── utils/
│   ├── data_parser.py     # CSV解析
│   ├── validator.py       # 数据验证
│   └── stats.py           # 统计辅助函数
├── requirements.txt
└── tests/
    ├── test_psi.py
    ├── test_ccs.py
    └── test_rho_pc.py
```

**核心算法实现：**

**PSI (Performance-Structure Independence):**
```python
# backend/core/psi_calculator.py
import numpy as np
from scipy.spatial.distance import euclidean

def compute_psi(data):
    """
    PSI = (1/T) Σ ||θᵢ - θᵢ₋₁||₂
    
    Args:
        data: DataFrame with columns [time_period, algorithm, performance, constraints...]
    
    Returns:
        psi_score: float
        psi_by_period: list[float]
    """
    # 按时间段分组
    periods = sorted(data['time_period'].unique())
    
    parameter_vectors = []
    for period in periods:
        period_data = data[data['time_period'] == period]
        # 构建参数向量（所有约束列）
        constraint_cols = [col for col in data.columns if col.startswith('constraint_')]
        param_vector = period_data[constraint_cols].mean().values
        parameter_vectors.append(param_vector)
    
    # 计算相邻时间段的L2距离
    distances = []
    for i in range(1, len(parameter_vectors)):
        dist = euclidean(parameter_vectors[i], parameter_vectors[i-1])
        distances.append(dist)
    
    psi_score = np.mean(distances) if distances else 0.0
    
    return psi_score, distances
```

**CCS (Constraint-Consistency Score):**
```python
# backend/core/ccs_calculator.py
import numpy as np

def compute_ccs(data):
    """
    CCS = 1 - (1/p) Σ CV(cⱼ)
    
    CV(cⱼ) = coefficient of variation for constraint j
    """
    constraint_cols = [col for col in data.columns if col.startswith('constraint_')]
    
    cvs = []
    for col in constraint_cols:
        values = data[col].dropna()
        if len(values) > 0 and values.mean() != 0:
            cv = values.std() / values.mean()
            cvs.append(cv)
    
    avg_cv = np.mean(cvs) if cvs else 0.0
    ccs_score = max(0, 1 - avg_cv)
    
    return ccs_score, cvs
```

**ρ_PC (Performance-Constraint Correlation):**
```python
# backend/core/rho_pc_calculator.py
import numpy as np
from scipy.stats import pearsonr

def compute_rho_pc(data):
    """
    ρ_PC = Pearson(P, C̄)
    """
    # 按时间段和算法分组
    grouped = data.groupby(['time_period', 'algorithm']).agg({
        'performance': 'mean',
        **{col: 'mean' for col in data.columns if col.startswith('constraint_')}
    }).reset_index()
    
    performance = grouped['performance'].values
    
    # 计算平均约束值
    constraint_cols = [col for col in grouped.columns if col.startswith('constraint_')]
    mean_constraints = grouped[constraint_cols].mean(axis=1).values
    
    if len(performance) > 2:
        rho_pc, p_value = pearsonr(performance, mean_constraints)
    else:
        rho_pc, p_value = 0.0, 1.0
    
    return rho_pc, p_value
```

**Bootstrap Confidence Intervals:**
```python
# backend/core/bootstrap.py
import numpy as np
from .psi_calculator import compute_psi
from .ccs_calculator import compute_ccs
from .rho_pc_calculator import compute_rho_pc

def bootstrap_ci(data, n_iterations=1000, confidence=0.95):
    """
    Bootstrap resampling for confidence intervals
    """
    n_samples = len(data)
    
    psi_samples = []
    ccs_samples = []
    rho_pc_samples = []
    
    for _ in range(n_iterations):
        # Resample with replacement
        sample_indices = np.random.choice(n_samples, size=n_samples, replace=True)
        sample_data = data.iloc[sample_indices]
        
        psi, _ = compute_psi(sample_data)
        ccs, _ = compute_ccs(sample_data)
        rho_pc, _ = compute_rho_pc(sample_data)
        
        psi_samples.append(psi)
        ccs_samples.append(ccs)
        rho_pc_samples.append(rho_pc)
    
    alpha = 1 - confidence
    lower_percentile = (alpha / 2) * 100
    upper_percentile = (1 - alpha / 2) * 100
    
    return {
        'psi': {
            'ci_lower': np.percentile(psi_samples, lower_percentile),
            'ci_upper': np.percentile(psi_samples, upper_percentile),
            'samples': psi_samples
        },
        'ccs': {
            'ci_lower': np.percentile(ccs_samples, lower_percentile),
            'ci_upper': np.percentile(ccs_samples, upper_percentile),
            'samples': ccs_samples
        },
        'rho_pc': {
            'ci_lower': np.percentile(rho_pc_samples, lower_percentile),
            'ci_upper': np.percentile(rho_pc_samples, upper_percentile),
            'samples': rho_pc_samples
        }
    }
```

**API接口 (Flask):**
```python
# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from core.bias_scorer import detect_circular_bias

app = Flask(__name__)
CORS(app)

@app.route('/api/detect', methods=['POST'])
def detect_bias():
    try:
        # 接收CSV数据
        csv_data = request.json['csv_data']
        
        # 解析为DataFrame
        from io import StringIO
        df = pd.read_csv(StringIO(csv_data))
        
        # 执行检测
        results = detect_circular_bias(df)
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

#### 1.2 前端集成 (估时: 1天)

**修改前端调用方式：**

```javascript
// web-app/src/utils/apiClient.js
export async function detectBias(csvData) {
  const response = await fetch('http://localhost:5000/api/detect', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ csv_data: csvData })
  });
  
  if (!response.ok) {
    throw new Error('Detection failed');
  }
  
  return await response.json();
}
```

**更新App.jsx:**
```javascript
// 替换mock detection
import { detectBias } from './utils/apiClient';

const handleScan = async () => {
  setLoading(true);
  
  try {
    const results = await detectBias(data.csvData);
    setResults(results);
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};
```

---

#### 1.3 部署方案 (估时: 1天)

**选项A: Pyodide (浏览器内Python) - 推荐**

**优势：**
- ✅ 无需后端服务器
- ✅ 完全客户端运行
- ✅ 保持隐私优势

**实现：**
```javascript
// web-app/src/utils/pyodideRunner.js (已存在，需完善)
export async function runBiasDetection(csvData) {
  if (!window.pyodide) {
    window.pyodide = await loadPyodide();
    await window.pyodide.loadPackage(['numpy', 'pandas', 'scipy']);
  }
  
  // 加载Python代码
  await window.pyodide.runPythonAsync(`
    import pandas as pd
    from io import StringIO
    
    # 你的PSI/CCS/ρ_PC算法
    # ... (完整Python代码)
    
    df = pd.read_csv(StringIO('''${csvData}'''))
    results = detect_circular_bias(df)
  `);
  
  return window.pyodide.globals.get('results').toJs();
}
```

**选项B: 云函数 (Vercel/Netlify)**

**优势：**
- ✅ Serverless，按需付费
- ✅ 自动扩展

**部署：**
```python
# api/detect.py (Vercel Functions)
from flask import Flask, request, jsonify
# ... (同上Flask代码)

def handler(request):
    # Vercel函数入口
    pass
```

**选项C: 独立后端服务器**

**部署到：**
- Railway.app (免费tier)
- Render.com (免费tier)
- Fly.io (免费tier)

---

### 📅 子任务时间表

| 任务 | 时间 | 交付物 |
|------|------|--------|
| Python算法实现 | Day 1-2 | PSI/CCS/ρ_PC完整代码 |
| Bootstrap实现 | Day 2 | 1000次重采样 |
| 单元测试 | Day 3 | 测试覆盖率>80% |
| 前端集成 | Day 4 | API调用替换mock |
| Pyodide打包 | Day 5 | 浏览器内运行 |
| 端到端测试 | Day 6 | 真实数据验证 |
| 性能优化 | Day 7 | 响应时间<5秒 |

---

## 📢 任务2: 学术推广

### 目标
在学术圈建立Sleuth的知名度和credibility

### 2.1 学术论文 (估时: 2周)

**投稿目标：**

**选项A: Workshop (快速，3-6个月出结果)**
- NeurIPS Workshop on ML Safety
- ICML Workshop on Socially Responsible ML
- ICLR Workshop on Debugging ML Models

**选项B: 短会议论文 (中速，6-9个月)**
- AAAI Demo Track
- ACL System Demonstrations
- KDD Applied Data Science Track

**论文结构：**
```
Title: "Sleuth: A Browser-Based Tool for Detecting Circular 
       Reasoning Bias in AI Evaluation"

Abstract (150 words)
1. Introduction (1 page)
   - Motivation: 循环偏见问题
   - Gap: 缺少自动化检测工具
   
2. Methodology (2 pages)
   - PSI, CCS, ρ_PC数学定义
   - Bootstrap统计检验
   - CBS综合评分
   
3. System Design (1 page)
   - 架构图
   - 隐私保护设计
   
4. Evaluation (1.5 pages)
   - 真实数据集实验
   - 检测准确率
   - 用户研究
   
5. Demo & Availability (0.5 page)
   - Live demo链接
   - 开源代码
   
6. Conclusion (0.5 page)

References
```

**时间线：**
- Week 1-2: 写初稿
- Week 3: 实验和评估
- Week 4: 修改和投稿

---

### 2.2 技术博客 (估时: 2天)

**平台选择：**
1. **Medium** - 技术人群
2. **Dev.to** - 开发者社区
3. **Towards Data Science** - AI/ML专业
4. **个人博客** - SEO优化

**博客系列（3-4篇）：**

**博客1: "Why Your AI Benchmark Might Be Lying to You"**
- 问题：循环偏见的真实案例
- 影响：错误结论的代价
- 解决：介绍Sleuth
- CTA: Try our tool

**博客2: "Building a Privacy-First ML Audit Tool with React + Python"**
- 技术栈介绍
- Pyodide浏览器内Python
- 架构设计
- CTA: Star on GitHub

**博客3: "Statistical Rigor in Algorithm Evaluation: PSI, CCS, ρ_PC"**
- 数学原理深入
- 为什么bootstrap重要
- 案例分析
- CTA: Use Sleuth

**博客4: "From Academia to Product: Launching an Open Source ML Tool"**
- 开发历程
- 技术挑战
- 用户反馈
- CTA: Contribute

---

### 2.3 社交媒体 (估时: 持续)

**平台策略：**

#### Twitter/X (@SleuthBiasAI)
**内容计划：**
- 每周2-3条推文
- 类型：案例分析、技术讲解、用户反馈、更新日志

**示例推文：**
```
🚨 New research finds 40% of AI papers have evaluation bias

How can you tell if YOUR benchmark is manipulated?

Meet Sleuth 🔍 - Free tool that detects circular reasoning 
in algorithm evaluation

✅ Browser-based
✅ No signup
✅ Privacy-first

Try it: [link]

#MachineLearning #AI #Research
```

#### Reddit
**目标subreddits:**
- r/MachineLearning (1.5M members)
- r/artificial (100K)
- r/datascience (1M)
- r/learnmachinelearning (500K)

**发帖策略：**
- Title: "[P] Sleuth - Open Source Tool for Detecting Circular Bias in AI Evaluation"
- 内容：问题陈述 → 解决方案 → Demo链接 → 开源代码
- 时间：周二或周四（最佳engagement）

#### Hacker News
**标题：**
- "Show HN: Sleuth – Detect circular bias in AI benchmarks"
- "Ask HN: How do you verify algorithm evaluation fairness?"

---

### 2.4 学术社区 (估时: 持续)

**参与渠道：**

1. **ResearchGate** - 创建项目页面
2. **Google Scholar** - 创建profile，上传预印本
3. **arXiv** - 提交技术报告
4. **Papers with Code** - 添加实现

**会议参与：**
- 投稿poster（NeurIPS/ICML/ICLR）
- 参加workshop讨论
- 与审稿人建立联系

---

## 👥 任务3: 获得早期用户

### 目标
获得**50-100个真实用户**并收集反馈

### 3.1 目标用户画像

**用户群1: 博士生 (最容易获取)**
- 正在写论文
- 需要验证evaluation
- 时间紧迫，愿意尝试新工具

**用户群2: 审稿人**
- 评审算法比较论文
- 需要快速检测问题
- 影响力大

**用户群3: 期刊编辑**
- 维护期刊质量
- 需要系统化审查工具
- 可能推荐给投稿人

---

### 3.2 用户获取策略

#### 策略1: 直接外联 (Direct Outreach)

**邮件模板：**
```
Subject: Free Tool for Detecting Evaluation Bias in Your Research

Hi [Name],

I noticed your recent paper on [topic] in [venue]. Great work on [specific contribution]!

I'm reaching out because I built a tool that might help with evaluation validation - it's called Sleuth.

Many researchers face circular reasoning bias (evaluation protocols manipulated based on preliminary results). Sleuth automatically detects this using statistical analysis.

Would you be interested in trying it on your evaluation data? It's:
✅ Free and open source
✅ Browser-based (no installation)
✅ Privacy-preserving (data stays local)

Live demo: [link]

Would love your feedback as an early user!

Best,
Hongping Zhang
```

**目标：**
- 10-15封邮件/周
- 选择最近发表算法比较论文的作者
- 预期回复率：10-20%

---

#### 策略2: 学术社区渗透

**方法：**
1. 加入ML Slack/Discord群组
2. 回答evaluation相关问题
3. 顺便提到Sleuth

**示例：**
```
User: "How do I know if my baseline is fair?"

You: "Great question! A few things to check:
1. Same hyperparameter tuning budget
2. Same validation set
3. No data leakage

Also, there's a new tool called Sleuth that can automatically 
detect if evaluation protocols were manipulated. Might be worth 
a try: [link]"
```

---

#### 策略3: GitHub/开源社区

**Actions:**
1. 在GitHub trending上推广
2. 添加topics标签（machine-learning, bias-detection, evaluation）
3. 完善README with badges
4. 回复相关issues（其他项目）

**README改进：**
- 添加GIF演示
- "Star and share"按钮
- 使用案例展示

---

#### 策略4: 教授/实验室合作

**目标：**
- 联系5-10个AI实验室
- 提供免费workshop/演示
- 请求在lab meeting介绍

**Pitch:**
```
"Would your lab be interested in a 30-min demo of an 
evaluation bias detection tool? 

It's particularly useful for:
- PhD students validating their experiments
- Ensuring reproducibility
- Catching evaluation flaws early

Free tool, just looking for feedback from expert users."
```

---

### 3.3 用户反馈收集

**方法：**

1. **In-App Survey** (弹窗)
   ```
   "How likely are you to recommend Sleuth? (0-10)"
   "What would make Sleuth more useful?"
   [Submit]
   ```

2. **深度访谈** (5-10个用户)
   - 30分钟Zoom
   - 观察使用过程
   - 收集改进建议

3. **GitHub Issues**
   - 鼓励提交feature requests
   - 快速响应

4. **Email Follow-up**
   - 使用后2天发送
   - "How was your experience?"

---

### 3.4 成功指标

**定量指标：**
- GitHub Stars: 50+
- 网站访问: 500+ unique visitors
- 活跃用户: 50+
- 论文引用: 5+ (6个月后)

**定性指标：**
- 用户反馈正面率 > 80%
- NPS (Net Promoter Score) > 30
- 至少1个实验室/团队采用

---

## 📊 1个月甘特图

```
Week 1 (Oct 15-21)
├── Day 1-3: Python后端开发 (PSI/CCS/ρ_PC)
├── Day 4-5: Bootstrap + 测试
└── Day 6-7: 前端集成

Week 2 (Oct 22-28)
├── Day 1-2: Pyodide打包
├── Day 3-4: 端到端测试
├── Day 5: 写博客1 (Medium)
└── Day 6-7: 论文初稿

Week 3 (Oct 29-Nov 4)
├── Day 1-2: 论文实验
├── Day 3: Reddit/HN发帖
├── Day 4-5: Twitter推广开始
└── Day 6-7: 用户外联 (10-15封邮件)

Week 4 (Nov 5-11)
├── Day 1-2: 论文修改
├── Day 3: 论文投稿
├── Day 4: 写博客2
├── Day 5-7: 用户反馈收集和分析

Week 5 (Nov 12-15)
├── 总结和复盘
├── 准备Phase 2计划
└── 庆祝！
```

---

## ✅ 完成标准

### 任务1: Python后端 ✅
- [ ] PSI/CCS/ρ_PC算法实现并通过测试
- [ ] Bootstrap 1000次重采样运行正常
- [ ] Pyodide浏览器内运行成功
- [ ] 端到端测试通过（5个真实数据集）
- [ ] 响应时间 < 5秒

### 任务2: 学术推广 ✅
- [ ] 1篇论文投稿（workshop/demo track）
- [ ] 2篇技术博客发布（Medium/Dev.to）
- [ ] Reddit/HN至少1篇高质量帖子
- [ ] Twitter账号开通，发布10+条推文
- [ ] arXiv预印本上传

### 任务3: 早期用户 ✅
- [ ] 50+ GitHub stars
- [ ] 30+ 真实用户使用
- [ ] 10+ 用户反馈收集
- [ ] 2+ 深度访谈完成
- [ ] NPS > 20

---

## 🎯 Phase 1结束后的里程碑

**技术里程碑：**
- ✅ 真实Python后端运行
- ✅ 浏览器内完整功能
- ✅ 测试覆盖率 > 80%

**市场里程碑：**
- ✅ 学术圈知名度建立
- ✅ 早期用户验证产品方向
- ✅ 论文投稿完成

**准备Phase 2：**
- PageRank技术储备
- 工业功能调研
- 商业化探索

---

## 💡 风险和应对

### 风险1: Python后端开发时间超预期
**应对：** 先用简化版算法，后续迭代

### 风险2: 用户获取困难
**应对：** 降低目标到20-30个核心用户即可

### 风险3: 论文被拒
**应对：** 同时投2-3个venue，提高命中率

---

**准备好开始Phase 1了吗？** 🚀
