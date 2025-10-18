# Sleuth v1.2 Development Roadmap

**Version:** 1.2.0  
**Target Release:** Q1 2026  
**Status:** Planning Phase

---

## 🎯 Overview

v1.2将Sleuth从静态分析工具升级为**动态AI评估平台**，集成实时LLM测试、贝叶斯统计推断、多模态支持和PWA部署。

### 核心目标

- 🚀 **市场定位**: 从"偏差检测工具" → "全栈AI审计平台"
- 📈 **用户增长**: 预计+20%使用量（LLM自动化）
- 🏆 **竞争优势**: 超越AIF360等静态工具
- 📝 **学术价值**: 发表ACL/NeurIPS workshop论文

---

## 🔴 高优先级功能

### 1. 自动化LLM管道集成 ⭐⭐⭐⭐⭐

**工作量:** 1周 (40小时)  
**技术栈:** Hugging Face Transformers, FastAPI, React  
**难度:** 🔥🔥🔥 High

#### 功能描述

用户在Web App中点击"Quick LLM Scan"，输入：
- Model ID (e.g., `gpt2`, `bert-base-uncased`)
- Prompt template (e.g., `"Classify: {text}"`)
- Few-shot examples (可选)

系统自动：
1. 从Hugging Face加载模型
2. 在GLUE子集上运行评估
3. 生成性能/约束时间序列
4. 计算循环偏差指标
5. 实时显示结果

#### 技术架构

```
Frontend (React)
    ↓ HTTP POST
Backend API (FastAPI/Flask)
    ↓
Hugging Face Pipeline
    ↓
GLUE Dataset
    ↓
Bias Detection Core
    ↓
Results → Frontend
```

#### 实施步骤

**Week 1: Days 1-2**
- [ ] 创建FastAPI后端服务
- [ ] 实现`/api/llm-scan`端点
- [ ] 集成Hugging Face Transformers
- [ ] 测试基础模型加载（gpt2, bert）

**Week 1: Days 3-4**
- [ ] 实现GLUE子集评估逻辑
- [ ] 生成时间序列数据（模拟多次运行）
- [ ] 集成到`BiasDetector`
- [ ] 添加进度条和日志

**Week 1: Days 5**
- [ ] 前端UI："Quick LLM Scan"按钮
- [ ] 模型ID输入框 + 提示模板编辑器
- [ ] 实时进度显示
- [ ] 结果可视化

#### 技术规范

**API接口设计:**
```python
POST /api/llm-scan
{
  "model_id": "gpt2",
  "prompt_template": "Classify: {text}",
  "dataset": "glue/sst2",
  "n_iterations": 5,
  "few_shot_examples": [...],
  "constraints": {
    "max_tokens": 512,
    "temperature": 0.7
  }
}

Response:
{
  "performance_matrix": [[0.72, 0.74, ...], ...],
  "constraint_matrix": [[512, 512, ...], ...],
  "bias_results": {
    "psi_score": 0.0238,
    "ccs_score": 0.8860,
    "rho_pc_score": 0.9983,
    ...
  },
  "execution_time": 42.3
}
```

**依赖:**
```bash
pip install transformers torch datasets fastapi uvicorn
```

#### 竞争优势

| 功能 | Sleuth v1.2 | AIF360 | Fairlearn |
|------|-------------|--------|-----------|
| LLM自动评估 | ✅ | ❌ | ❌ |
| 实时偏差检测 | ✅ | ❌ | ❌ |
| Hugging Face集成 | ✅ | ❌ | ❌ |
| 动态测试 | ✅ | ❌ 静态 | ❌ 静态 |

#### 风险与缓解

**风险1:** 模型加载时间长（大模型如GPT-3）  
**缓解:** 
- 提供模型缓存
- 支持量化版本（4-bit, 8-bit）
- 异步处理 + WebSocket实时更新

**风险2:** 计算资源需求  
**缓解:**
- 限制模型大小（<1B参数）
- 提供云端API选项
- 本地小模型优先（distilbert）

**风险3:** API限流（Hugging Face）  
**缓解:**
- 缓存常用模型
- 支持本地模型路径
- 错误提示和重试机制

---

### 2. 贝叶斯不确定性量化 ⭐⭐⭐⭐⭐

**工作量:** 2周 (80小时)  
**技术栈:** PyMC3, ArviZ, Plotly  
**难度:** 🔥🔥🔥🔥 Very High

#### 功能描述

从频率主义Bootstrap → 贝叶斯后验推断：

**输入:** 性能矩阵 + 约束矩阵  
**输出:** `P(circular_bias | data) = 0.72 [0.65-0.79]`

**优势:**
- 超越p值：直接回答"偏差概率是多少？"
- 先验知识整合：基于领域专家经验
- 不确定性传播：全贝叶斯推断
- 学术价值：ACL/NeurIPS投稿亮点

#### 数学模型

**似然函数:**
```
PSI ~ Normal(μ_psi, σ_psi)
CCS ~ Beta(α_ccs, β_ccs)
ρ_PC ~ Normal(μ_rho, σ_rho)
```

**先验分布:**
```
μ_psi ~ HalfNormal(0.1)
σ_psi ~ HalfNormal(0.05)
α_ccs, β_ccs ~ Gamma(2, 2)
μ_rho ~ Normal(0, 0.3)
σ_rho ~ HalfNormal(0.2)
```

**后验推断:**
```
P(bias | PSI, CCS, ρ_PC) ∝ P(PSI, CCS, ρ_PC | bias) × P(bias)
```

#### 实施步骤

**Week 1: 数学建模**
- [ ] Day 1-2: 设计贝叶斯模型架构
- [ ] Day 3-4: PyMC3模型实现
- [ ] Day 5: MCMC采样和收敛诊断

**Week 2: 集成和可视化**
- [ ] Day 1-2: 集成到`core.py`
- [ ] Day 3: ArviZ诊断图
- [ ] Day 4: Plotly概率密度图
- [ ] Day 5: Web UI集成

#### 技术规范

**API设计:**
```python
def bayesian_bias_prob(
    performance_matrix: np.ndarray,
    constraint_matrix: np.ndarray,
    prior_params: Optional[dict] = None,
    n_samples: int = 2000,
    n_chains: int = 4
) -> dict:
    """
    贝叶斯偏差概率推断
    
    Returns:
    {
        'bias_probability': 0.72,  # P(bias | data)
        'ci_lower': 0.65,
        'ci_upper': 0.79,
        'posterior_samples': [...],  # MCMC样本
        'diagnostics': {
            'rhat': 1.01,  # 收敛诊断
            'ess_bulk': 1850,  # 有效样本量
            'divergences': 0
        }
    }
    """
```

**可视化:**
```python
from circular_bias_detector.visualization import plot_posterior_density

plot_posterior_density(
    posterior_samples=results['posterior_samples'],
    save_path='posterior_density.png'
)
```

**依赖:**
```bash
pip install pymc3 arviz theano-pymc
```

#### 学术价值

**投稿目标:**
- ACL 2026 Workshop on Responsible NLP
- NeurIPS 2026 Workshop on Bayesian Methods
- AAAI 2027 Main Conference

**论文标题建议:**
"Bayesian Inference for Circular Reasoning Bias Detection in AI Evaluation: A Probabilistic Framework"

**核心贡献:**
1. 首个贝叶斯偏差检测框架
2. 不确定性量化方法
3. 先验知识整合机制
4. 实证验证（LLM数据集）

---

## 🟡 中优先级功能

### 3. 多模态 & 基准扩展 ⭐⭐⭐⭐

**工作量:** 2周 (80小时)  
**技术栈:** CLIP, HELM, MMLU  
**难度:** 🔥🔥🔥 High

#### 功能描述

支持视觉-语言模型（VLM）评估：
- CLIP分数作为性能指标
- 图像分辨率、推理时间作为约束
- HELM/MMLU基准数据集预载
- GPT-4V/LLaVA偏差检测示例

#### 技术架构

**扩展约束矩阵:**
```python
# 传统约束
constraint_matrix_text = [[512, 0.7, 8GB], ...]

# 多模态约束
constraint_matrix_multimodal = [
    [512, 0.7, 8GB, 224x224, 1.2s],  # text_tokens, temp, mem, img_res, latency
    ...
]
```

**新增指标:**
- CLIP Score (vision-language alignment)
- Image Resolution (constraint)
- Inference Time (constraint)
- Memory Footprint (constraint)

#### 实施步骤

**Week 1: 架构扩展**
- [ ] Day 1-2: 扩展约束矩阵数据结构
- [ ] Day 3: CLIP评估集成
- [ ] Day 4-5: HELM/MMLU数据集加载器

**Week 2: 示例和文档**
- [ ] Day 1-2: GPT-4V偏差检测示例
- [ ] Day 3: "Multi-Modal LLM Example"指南
- [ ] Day 4: 更新Web UI（多模态选项）
- [ ] Day 5: 测试和文档

#### 预载数据集

| 数据集 | 模态 | 大小 | 用途 |
|--------|------|------|------|
| HELM | Text | 42 scenarios | LLM基准 |
| MMLU | Text | 57 subjects | 知识评估 |
| COCO Captions | Vision+Text | 5k images | VLM评估 |
| Flickr30k | Vision+Text | 30k images | 图像描述 |

#### 竞争优势

**市场定位:** "全栈AI审计平台"
- Text-only: ❌ 其他工具
- Text + Vision: ✅ Sleuth v1.2

---

### 4. PWA & 分享功能 ⭐⭐⭐

**工作量:** 1周 (40小时)  
**技术栈:** React PWA, Service Worker, QR Code  
**难度:** 🔥🔥 Medium

#### 功能描述

**PWA特性:**
- 离线使用（缓存数据和模型）
- 移动端优化（响应式设计）
- 桌面安装（添加到主屏幕）

**分享功能:**
- "Share Report"按钮
- 生成QR码链接JSON结果
- 一键上传Zenodo
- 企业级报告导出（PDF）

#### 实施步骤

**Week 1: Days 1-2**
- [ ] 配置React PWA模板
- [ ] Service Worker设置
- [ ] 离线缓存策略

**Week 1: Days 3-4**
- [ ] QR码生成（qrcode.js）
- [ ] JSON报告序列化
- [ ] Zenodo API集成

**Week 1: Day 5**
- [ ] 移动端UI优化
- [ ] 测试和部署

#### 技术规范

**PWA Manifest:**
```json
{
  "name": "Sleuth - AI Bias Detection",
  "short_name": "Sleuth",
  "theme_color": "#2563eb",
  "background_color": "#ffffff",
  "display": "standalone",
  "orientation": "portrait",
  "scope": "/",
  "start_url": "/",
  "icons": [...]
}
```

**Service Worker缓存:**
```javascript
// 缓存静态资源
const CACHE_NAME = 'sleuth-v1.2';
const urlsToCache = [
  '/',
  '/index.html',
  '/assets/index.js',
  '/data/llm_eval_sample.csv'
];
```

**分享功能:**
```javascript
// 生成QR码
import QRCode from 'qrcode';

const shareReport = async (results) => {
  const reportUrl = await uploadToZenodo(results);
  const qrCodeDataUrl = await QRCode.toDataURL(reportUrl);
  // 显示QR码
};
```

#### 商业价值

**目标客户:**
- 企业AI团队（离线审计）
- 移动研究人员（平板/手机）
- 合规部门（报告分享）

**预期增长:**
- 移动端用户: +30%
- 企业采用率: +15%
- 报告生成量: +50%

---

## 📅 开发时间表

### Phase 1: 高优先级（Week 1-3）

| Week | 任务 | 负责人 | 状态 |
|------|------|--------|------|
| W1 | LLM管道后端 | TBD | 📋 Planning |
| W2 | LLM管道前端 | TBD | 📋 Planning |
| W3 | 贝叶斯模型 Week 1 | TBD | 📋 Planning |
| W4 | 贝叶斯模型 Week 2 | TBD | 📋 Planning |

### Phase 2: 中优先级（Week 5-7）

| Week | 任务 | 负责人 | 状态 |
|------|------|--------|------|
| W5 | 多模态架构 | TBD | 📋 Planning |
| W6 | 多模态示例 | TBD | 📋 Planning |
| W7 | PWA转换 | TBD | 📋 Planning |

### Phase 3: 集成测试（Week 8）

- [ ] 端到端测试
- [ ] 性能优化
- [ ] 文档更新
- [ ] 发布v1.2.0

---

## 📊 成功指标

### 技术指标

- [ ] LLM自动评估成功率 > 95%
- [ ] 贝叶斯推断时间 < 10秒
- [ ] PWA离线功能正常率 100%
- [ ] 移动端性能评分 > 90 (Lighthouse)

### 业务指标

- [ ] 用户增长 +20%
- [ ] GitHub Stars +500
- [ ] 论文引用 +10篇
- [ ] 企业用户 +5家

### 学术指标

- [ ] 发表1篇workshop论文
- [ ] 提交1篇顶会论文
- [ ] 受邀1次学术演讲

---

## 🛠️ 技术栈升级

### 新增依赖

**Python后端:**
```
transformers>=4.30.0
torch>=2.0.0
datasets>=2.14.0
fastapi>=0.100.0
pymc3>=5.0.0
arviz>=0.16.0
clip-by-openai>=1.0.0
```

**前端:**
```
react-pwa
qrcode.react
axios
socket.io-client
```

### 基础设施需求

**计算资源:**
- GPU: NVIDIA T4 or better (for LLM inference)
- RAM: 16GB minimum
- Storage: 50GB for model cache

**服务器:**
- Backend API: FastAPI on Uvicorn
- 可选: Docker容器化部署
- 可选: Kubernetes水平扩展

---

## 🚧 风险管理

### 技术风险

| 风险 | 影响 | 概率 | 缓解策略 |
|------|------|------|----------|
| 大模型加载慢 | 高 | 中 | 模型缓存+量化 |
| PyMC3收敛问题 | 中 | 低 | 调整先验+更多采样 |
| PWA兼容性 | 低 | 低 | 渐进增强 |
| Zenodo API限制 | 低 | 中 | 本地存储备份 |

### 资源风险

| 风险 | 影响 | 缓解策略 |
|------|------|----------|
| 开发时间不足 | 高 | 分阶段发布（v1.2.0 → v1.2.1） |
| GPU资源不足 | 中 | 云端API备选方案 |
| 人力不足 | 中 | 社区贡献+外包 |

---

## 📝 下一步行动

### 立即执行（本周）

1. **确认技术栈**
   - [ ] 选择后端框架（FastAPI vs Flask）
   - [ ] 确认PyMC3版本兼容性
   - [ ] 测试Hugging Face API限流

2. **创建开发分支**
   ```bash
   git checkout -b feature/v1.2-llm-pipeline
   git checkout -b feature/v1.2-bayesian
   ```

3. **编写技术规范文档**
   - [ ] LLM Pipeline API Spec
   - [ ] Bayesian Model Math Derivation
   - [ ] Multi-Modal Schema Design

### 短期（2周内）

1. **搭建开发环境**
   - [ ] Docker容器配置
   - [ ] GPU环境测试
   - [ ] CI/CD pipeline更新

2. **原型开发**
   - [ ] LLM pipeline MVP
   - [ ] 贝叶斯toy example
   - [ ] PWA基础配置

### 中期（1个月内）

1. **功能开发**
   - [ ] 完成高优先级功能
   - [ ] 开始中优先级功能
   - [ ] 编写单元测试

2. **文档更新**
   - [ ] API文档
   - [ ] 用户指南
   - [ ] 开发者文档

---

## 💡 社区参与

### 开源贡献机会

欢迎社区贡献以下模块：

1. **LLM评估器** - 支持更多模型（Claude, Gemini）
2. **贝叶斯先验** - 领域专家先验分布
3. **多模态数据集** - 新基准数据集
4. **PWA UI** - 移动端优化

### 赞助和合作

寻求以下合作：

- **GPU赞助**: Hugging Face, Lambda Labs
- **学术合作**: 顶级NLP/ML实验室
- **企业试点**: AI公司早期测试

---

## 📧 联系方式

**项目负责人:** Hongping Zhang  
**Email:** yujjam@uest.edu.gr  
**GitHub:** https://github.com/hongping-zh/circular-bias-detection  
**讨论区:** https://github.com/hongping-zh/circular-bias-detection/discussions

---

## 🎉 总结

v1.2将Sleuth打造成：
- 🚀 **动态AI评估平台**（而非静态工具）
- 🧠 **贝叶斯统计框架**（学术创新）
- 👁️ **多模态支持**（覆盖VLM）
- 📱 **PWA部署**（企业友好）

**预期影响:**
- 用户增长 +20%
- 学术论文 1-2篇
- 市场领先地位巩固

---

**让我们一起构建下一代AI评估工具！** 🚀
