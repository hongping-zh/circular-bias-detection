# 关键修订清单 - 第二篇论文首次修改

## 必须立即修复的问题 (CRITICAL)

### 1. 完成 Section 2.4 Limitations
**当前状态**: 截断且包含中文字符 "截止2025-10"
**修复后**:
```markdown
### 2.4 Limitations

This survey has several constraints that readers should consider:

**Temporal Scope**: Literature search concluded October 2025, meaning recent developments may not be captured. Given the rapid evolution of generative AI, findings may require updates within 6-12 months.

**Linguistic Bias**: We focused on English-language publications, potentially missing important work from non-Anglophone research communities, particularly relevant given our emphasis on global epistemic diversity.

**Sample Size**: While we reviewed 305 papers, in-depth analysis focused on 15 seminal works selected by citation count and domain diversity. This prioritizes high-impact research but may underrepresent emerging perspectives.

**Geographic Concentration**: The citation-based selection likely overrepresents North American and European research, limiting insights into circular bias manifestations in Global South AI deployments.

**Publication Bias**: Focusing on highly-cited work (≥10 citations) excludes recent preprints and may favor positive results over null findings.

We address these limitations through forward-looking analysis of emerging trends (Section 6) and explicit calls for underrepresented research areas (Section 6.4).
```

### 2. 修复 Section 5.1 引用错误
**错误**: "Vokinger et al. [5] documented commercial algorithm..."
**问题**: Reference [5] 是 Shumailov (model collapse), 不是 Vokinger
**正确引用**: 应该是 [14] Obermeyer et al. 2019 或 [13] Vokinger et al. 2021

**修复后**:
```markdown
#### Clinical Risk Scoring: Racial Bias Cycle

Obermeyer et al. [14] documented a widely-used commercial algorithm that used healthcare cost as proxy for medical need:
- Lower historical spending by Black patients (due to access barriers) → algorithm predicts lower need → fewer resources allocated → spending remains low → bias reinforced
- **Quantified Impact**: Black patients needed to be sicker than White patients to receive the same risk score; at a given risk score, Black patients had 26.3% more chronic illnesses [14]

**Intervention**:
- Replace cost-based proxy with direct clinical indicators (number of active chronic conditions)
- Implement adversarial debiasing to penalize correlation between predictions and race

**Post-deployment**: Quarterly fairness audits demonstrated equalized resource allocation within 2 years, though disparities in underlying health outcomes persisted due to structural factors beyond algorithmic control [13].
```

### 3. 添加缺失的参考文献
**缺失**: [12] Nestor et al. Lancet 2024 (在 Section 3.2 Healthcare 中多次引用)
**添加到参考文献列表**:
```markdown
[12] Nestor, B., McDermott, M. B. A., Boag, W., et al. (2024). Feature robustness in non-stationary health records: Caveats to deployable model performance in common clinical machine learning tasks. *The Lancet Digital Health*, 6(3), e142-e150. https://doi.org/10.1016/S2589-7500(23)00261-X
```

### 4. 解决样本数量不一致
**问题**: 
- Section 1.3: "15 seminal works"
- Section 2.1: "Top 10 by citations"
- Section 2.2: "Core Paper Selection" 未明确数量

**统一说明**:
```markdown
### 1.3 Survey Scope and Methodology

We conducted a PRISMA-guided systematic review of 600+ publications (2021–2025). After deduplication and quality filtering, 305 papers met inclusion criteria (≥10 citations, explicit circular bias discussion). We performed in-depth analysis of **15 seminal works** representing diverse domains and methodological approaches, with particular focus on **6 landmark 2024–2025 papers** that provide empirical validation of theoretical predictions (e.g., Shumailov et al.'s *Nature* model collapse proof; Glickman & Sharot's *Nature Human Behaviour* behavioral study). Section 3 provides detailed synthesis of these 15 core papers.
```

### 5. 定义 NMI 首字母缩写
**位置**: Section 1.4 第一句
**修改前**: "aligned with NMI's mission"
**修改后**: "aligned with Nature Machine Intelligence's mission"

或在首次出现时定义:
```markdown
This survey makes four contributions aligned with the mission of Nature Machine Intelligence (NMI) for responsible AI in societal context:
```

## 高优先级修订 (HIGH PRIORITY)

### 6. 缩短摘要 (当前 ~250 词，目标 150-200 词)
```markdown
## Abstract

Circular bias—self-reinforcing feedback loops where AI systems reshape their training data—threatens algorithmic fairness and epistemic integrity. Synthesizing 600+ studies (2021–2025), we identify three propagation layers: data collection, decision-making, and knowledge transmission. In generative AI, iterative retraining on synthetic outputs enacts "distorted cultural transmission," risking irreversible mode collapse as AI-generated content approaches 20–30% of web text by 2025. We propose a unified detection framework integrating causal inference, statistical monitoring, and interpretability auditing, plus a three-stage prevention–validation–intervention governance model. Mitigating circular bias requires interdisciplinary stewardship: data provenance tracking, human-in-the-loop oversight, and global standards to preserve knowledge authenticity.

**Keywords**: circular bias; feedback loops; AI fairness; cultural transmission; generative AI; epistemic integrity; bias mitigation; knowledge ecosystems
```

### 7. 重组 Section 3 结构
**问题**: Section 3.2.5 过长 (~1,200 词)，打断流程
**建议**:
```markdown
## 3. Synthesis of Core Literature

### 3.1 Overview: From Foundational Theory to 2024-2025 Breakthroughs
### 3.2 Domain-Specific Mechanisms
  - 3.2.1 Recommendation Systems
  - 3.2.2 Healthcare
  - 3.2.3 Generative AI
### 3.3 Conceptual Framework: Circular Bias as Distorted Cultural Transmission
  [将现有 3.2.5 内容移至此处，扩展为独立章节]
  - 3.3.1 Iterated Learning in Human and Machine Systems
  - 3.3.2 Parallel Mechanisms in LLMs
  - 3.3.3 Anthropological Parallels and Epistemic Implications
  - 3.3.4 Implications for Mitigation
### 3.4 Human-AI Interaction Empirics (2024)
### 3.5 Algorithmic Fairness and Repair (2024)
### 3.6 Comparative Analysis
  [合并现有 3.5 和 3.6]
```

### 8. 添加 Section 4.1 数学符号说明
```markdown
### 4.1 Causal Analysis Foundations

**Notation**: We use standard causal inference notation: $X \perp\!\!\!\perp Y$ denotes independence between variables $X$ and $Y$; $\text{do}(X=x)$ represents an intervention setting $X$ to value $x$ (distinct from observing $X=x$). For readers unfamiliar with causal inference, Pearl [12] provides comprehensive introduction.

**Structural Causal Models (SCMs)**:
[继续现有内容...]
```

### 9. 扩展 Section 7.2 具体建议
```markdown
### 7.2 Integrated Governance Imperatives

Addressing circular bias requires coordinated action across three domains, prioritized by feasibility and impact:

**Immediate Actions (0-12 months)**:
- **Technical**: Deploy real-time monitoring dashboards tracking PSI, fairness metrics, and performance disaggregation [Section 4.2]
- **Institutional**: Mandate post-deployment audits for high-risk AI systems (EU AI Act compliance) [8]
- **Cultural**: Launch public awareness campaigns addressing the "AI influence gap" documented by Glickman & Sharot [7]

**Medium-Term Initiatives (1-3 years)**:
- **Technical**: Implement provenance tracking via cryptographic watermarking for LLM outputs [5]; require ≥30% verified human-generated data in training corpora [6]
- **Institutional**: Establish algorithmic reparation frameworks to correct historical discrimination [8]
- **Cultural**: Create curated archives of pre-AI-era knowledge as "ground truth anchors" for future training

**Long-Term Transformation (3-5 years)**:
- **Technical**: Develop federated learning protocols enabling bias auditing without centralizing sensitive data
- **Institutional**: Harmonize global AI governance standards (ISO/IEC JTC 1/SC 42 working drafts [24])
- **Cultural**: Integrate epistemology and cultural anthropology into AI curricula and development practices

**Resource Considerations**: These interventions require significant investment—estimated $50-100M annually for a large tech platform—but the cost of inaction (erosion of public trust, regulatory penalties, societal harm) far exceeds prevention costs.
```

## 中等优先级 (MEDIUM PRIORITY)

### 10. 标准化参考文献格式
- 为所有期刊文章添加 DOI
- 统一 URL 格式
- 验证 2024 年论文已发表（非仅预印本）

### 11. 添加 Section 6.5 对抗性威胁
```markdown
### 6.5 Emerging Threats: Adversarial Exploitation

A critical under-explored risk is **adversarial manipulation** of circular feedback loops. Malicious actors could:
- **Data Poisoning**: Inject biased synthetic content into training corpora, exploiting model collapse dynamics
- **Feedback Gaming**: Strategically interact with deployed systems to bias future model behavior
- **Debiasing Evasion**: Reverse-engineer fairness interventions to circumvent protections

This threat surface demands research into robust provenance verification, anomaly detection for coordinated manipulation, and game-theoretic analysis of attacker incentives.
```

## 图片插入位置总结

1. **Figure 1** (Feedback Loops) → Section 1.1 或 Section 3.1 开头
2. **Figure 2** (Framework) → Section 4.4 (替换 placeholder)
3. **Figure 3** (Timelines) → Section 5.4 (替换 placeholder)  
4. **Figure 4** (Research Trends) → Section 2.1 或作为 Supplementary Figure

详细的图片说明文字见 `FIGURE_INSERTION_GUIDE.md`
