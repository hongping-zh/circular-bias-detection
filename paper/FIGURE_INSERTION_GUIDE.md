# 图片插入指南 - Circular Bias Survey Paper

## 图片对应位置

### Figure 1: Feedback Loops in Deployed AI Systems
**插入位置**: Section 1.1 或 Section 3.1 开头
**Markdown代码**:
```markdown
![Figure 1: Feedback Loops in Deployed AI Systems](./figures/figure1_feedback_loops.png)

**Figure 1 | Three-layer circular bias architecture.** Circular bias propagates through interconnected feedback loops across Data Layer (training data → model → predictions → new data), Decision Layer (predictions → algorithmic recommendations → behavioral adaptation → preference distortion), and Societal Layer (aggregate AI influence → population-level shifts → training distribution changes). Dotted lines indicate feedback paths that create self-reinforcing cycles.
```

### Figure 2: Unified Detection-Mitigation Framework  
**插入位置**: Section 4.4 (替换现有 placeholder)
**Markdown代码**:
```markdown
![Figure 2: Unified Detection-Mitigation Framework](./figures/figure2_framework.png)

**Figure 2 | Four-phase governance lifecycle for circular bias.** The framework integrates Prevention (causal graph analysis, data diversity planning, exploration strategy design), Validation (temporal holdout, multi-center evaluation, adversarial audits), Monitoring (real-time PSI/fairness tracking), and Intervention (context-specific responses: data drift → resampling; performance drift → model update; fairness violation → exploration boost; critical issues → human escalation).
```

### Figure 3: Domain-Specific Bias Amplification Timelines
**插入位置**: Section 5.4 (替换现有 placeholder)
**Markdown代码**:
```markdown
![Figure 3: Domain-Specific Bias Amplification Timelines](./figures/figure3_timelines.png)

**Figure 3 | Temporal evolution of circular bias across domains.** **(A) Healthcare**: Diagnostic sensitivity diverges between majority/minority groups over 24 months; multi-center data introduction (green line) reduces bias. **(B) RecSys**: Content diversity (Shannon entropy) declines under pure exploitation (orange); 15% exploration policy (green) mitigates loss. **(C) Credit Scoring**: Approval rate gap between White/Black applicants widens over 5 years; adversarial debiasing (purple line) partially closes gap. **(D) Generative AI**: Output entropy and vocabulary size exhibit exponential decay across 5 model generations, demonstrating mode collapse.
```

### Figure 4: Research Timeline and Citation Trends (2021-2025)
**插入位置**: Section 2.1 或 Section 3.1 (作为补充)
**Markdown代码**:
```markdown
![Figure 4: Research Timeline and Citation Trends](./figures/figure4_research_trends.png)

**Figure 4 | Field evolution and key milestones (2021-2025).** Annual publications (blue bars) grew from 40 (2021) to 250+ (2025). Cumulative citations (orange line) reached 35,000 by October 2025, with average citations per paper (purple dashed line) increasing from ~30 to 115. Key milestones: Mehrabi survey framework (2021), ChatGPT launch accelerating synthetic data concerns (2023), EU AI Act and ISO standards finalization (2024), Nature empirical proofs (2024-2025).
```

## 关键修订点

### 1. 完成 Section 2.4 (CRITICAL)
```markdown
### 2.4 Limitations

This survey has several constraints:

**Temporal Scope**: Literature search concluded October 2025. Given rapid generative AI evolution, findings may require updates within 6-12 months.

**Linguistic Bias**: English-language focus potentially misses non-Anglophone research, limiting global perspective claims.

**Sample Size**: In-depth analysis of 15 seminal works (from 305 reviewed) prioritizes high-impact research but may underrepresent emerging perspectives.

**Geographic Concentration**: Citation-based selection likely overrepresents North American/European research, limiting Global South insights.

**Publication Bias**: ≥10 citation threshold excludes recent preprints and may favor positive results.

We address these through forward-looking analysis (Section 6) and explicit research gap identification (Section 6.4).
```

### 2. 修复 Section 5.1 引用错误 (CRITICAL)
将 "Vokinger et al. [5]" 改为 "Obermeyer et al. [14]"

### 3. 缩短摘要至 150-200 词
### 4. 添加缺失的参考文献 [12] Nestor et al.
### 5. 定义 NMI = Nature Machine Intelligence (首次使用时)

## 下一步操作
1. 将4张图片保存到 `./figures/` 目录
2. 应用以上修订
3. 验证所有引用完整性
