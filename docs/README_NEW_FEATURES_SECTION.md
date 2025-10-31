# README 新功能章节 - 建议插入位置

## 建议插入到 README.md 的 "Additional Resources" 章节之前

---

## 🆕 New Features: Data Leakage Detection

### 📊 Case Study: The Contamination Crisis

Explore a real-world scenario where CBD uncovered a **95% → 58%** performance drop by detecting data contamination.

**Key Findings:**
- 🔴 **40%** of evaluation samples were contaminated
- 🔴 Highest contamination score: **0.87** (CRITICAL)
- 🔴 Avoided potential losses: **$7-15M**

**[📖 Read Full Case Study →](docs/CASE_STUDY_CONTAMINATION_CRISIS.md)**

---

### 🔍 Data Collection Strategy

Learn how to identify and collect high-risk evaluation datasets for contamination testing.

**Covered Topics:**
- Hugging Face dataset search strategies
- Priority datasets (SQuAD, CNN/DailyMail, Natural Questions)
- Automated collection scripts
- Training data sampling methods

**[📖 View Strategy Guide →](docs/DATA_COLLECTION_STRATEGY.md)**

**Quick Start:**
```python
from data.huggingface_data_collector import HuggingFaceDataCollector

collector = HuggingFaceDataCollector(output_dir="./my_data")
collected = collector.collect_all_priority_datasets(max_samples_per_dataset=1000)
```

---

### 🧬 Semantic Leakage Construction

Understand how subtle semantic similarities can lead to data leakage, and test CBD's detection capabilities.

**Features:**
- Synonym replacement
- Sentence restructuring (active ↔ passive)
- Paraphrase question generation
- Batch leakage simulation

**Example:**
```python
from examples.semantic_rewrite_leakage import SemanticRewriter

rewriter = SemanticRewriter()
pair = rewriter.construct_leaked_pair(
    train_sentence="The Statue of Liberty was a gift from France.",
    leakage_intensity=0.8
)

print(f"Leaked Question: {pair.eval_question}")
print(f"Semantic Similarity: {pair.semantic_similarity:.3f}")  # 0.875 (CRITICAL)
```

**[📖 View Implementation →](examples/semantic_rewrite_leakage.py)**

---

### 📈 Interactive Visualizations

Generate publication-quality figures for your contamination analysis.

**Available Visualizations:**
1. **Risk Distribution Map** - C_score distribution with risk zones
2. **Performance Reality Check** - Before/after comparison (95% → 58%)
3. **Leakage Type Distribution** - Breakdown by contamination type
4. **Sample Heatmap** - Pairwise contamination matrix

**Quick Generate:**
```bash
python examples/generate_case_study_visualizations.py
```

**Output:** 4 high-resolution PNG charts ready for presentations

---

### 🚀 One-Click Content Generation

Run all new features with a single command:

```bash
python run_mvp_content_generation.py
```

**Interactive menu allows you to:**
- Collect datasets from Hugging Face
- Generate semantic leakage examples
- Create case study visualizations
- Get complete analysis reports

---

### 📚 Documentation Index

| Document | Purpose | Audience |
|----------|---------|----------|
| [Case Study](docs/CASE_STUDY_CONTAMINATION_CRISIS.md) | Real-world contamination scenario | Decision makers, researchers |
| [Data Collection](docs/DATA_COLLECTION_STRATEGY.md) | HF dataset collection guide | Data scientists, ML engineers |
| [Implementation Guide](docs/MVP_CONTENT_IMPLEMENTATION_GUIDE.md) | Integration instructions | Developers |
| [Quick Start](QUICK_START_MVP_CONTENT.md) | Fast reference card | All users |

---

## 🎯 Use Cases for New Features

### For Researchers
- Access curated high-risk datasets
- Generate controlled contamination experiments
- Produce publication-quality visualizations

### For ML Engineers
- Audit evaluation pipelines for data leakage
- Test model robustness against semantic contamination
- Integrate CBD checks into CI/CD

### For Decision Makers
- Understand real-world contamination impact ($7-15M savings)
- Review case studies with business metrics
- Assess ROI of data integrity audits (700-1500x)

---

## 💡 What's Next?

After exploring these features, consider:

1. **Run the demo:** `python run_mvp_content_generation.py`
2. **Read the case study:** See how CBD prevented a costly deployment
3. **Try semantic leakage:** Test CBD's detection capabilities
4. **Integrate into your workflow:** Use the API examples

**[View Implementation Summary →](IMPLEMENTATION_SUMMARY.md)**

---

