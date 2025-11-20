# Social Media Posts for v1.2.0 Release

## Twitter/X Posts

### Post 1: Main Announcement
```
🎉 Circular Bias Detection v1.2.0 is here!

Three major features:
✅ One-line CLI: circular-bias detect zenodo://17637303
✅ Web app "Try Latest Dataset" button
✅ Lightweight Python package for easy integration

Try now: https://is.gd/check_sleuth?dataset=latest

#MachineLearning #AI #OpenScience #ResearchIntegrity
```

### Post 2: CLI Focus
```
🚀 New in CBD v1.2.0: Zero-config CLI

Just one command to analyze the latest real-world AI evaluation dataset:

$ circular-bias detect zenodo://17637303

Features:
• Auto-selects largest CSV
• Smart caching
• Results in < 1 min

Docs: https://github.com/hongping-zh/circular-bias-detection

#DevTools #CLI
```

### Post 3: Web App Feature
```
🆕 Try our latest dataset with one click!

Visit https://is.gd/check_sleuth?dataset=latest

New banner on homepage lets you:
• Load CBD Dataset v3/v3.1 instantly
• Test bias detection on real-world scenarios
• Share pre-loaded demos

No signup. No upload. Just science. 🧪

#WebDev #DataScience
```

### Post 4: Python Package
```
📦 New lightweight Python package!

from cbd import detect_bias, SklearnCBDModel

# Wrap your sklearn model
model = SklearnCBDModel(clf)

# Detect bias
result = detect_bias(model, X, y, metric=accuracy_score)

Perfect for MLOps pipelines 🔧

Docs: https://github.com/hongping-zh/circular-bias-detection

#Python #MLOps
```

### Post 5: Dataset Highlight
```
📊 CBD Dataset v3/v3.1 now integrated!

Real-world AI evaluation scenarios:
• Computer vision benchmarks
• NLP evaluations
• LLM prompt engineering

Access via:
• CLI: circular-bias detect zenodo://17637303
• Web: https://is.gd/check_sleuth?dataset=latest
• DOI: 10.5281/zenodo.17637303

#OpenData #Zenodo
```

## LinkedIn Post

### Professional Announcement
```
Excited to announce Circular Bias Detection v1.2.0! 🎉

After months of development, we're releasing three major features that make bias detection more accessible than ever:

🔹 One-Line CLI Command
No more complex setup. Just run:
circular-bias detect zenodo://17637303

🔹 Interactive Web Demo
Visit https://is.gd/check_sleuth?dataset=latest to try our latest real-world dataset with one click. Perfect for sharing with colleagues or using in presentations.

🔹 Lightweight Python Package
Integrate bias detection into your ML pipelines:

from cbd import detect_bias, SklearnCBDModel
model = SklearnCBDModel(your_sklearn_model)
result = detect_bias(model, X_test, y_test, metric=accuracy_score)

Why This Matters:
Circular reasoning bias is a critical issue in AI evaluation. When we inadvertently leak information from training or evaluation back into our models, we get overly optimistic results that don't hold up in production.

Our framework uses permutation testing to detect these issues before publication or deployment, helping researchers and practitioners maintain research integrity.

Key Stats:
✅ 2,669+ lines of new code
✅ 14 documentation files
✅ 100% backward compatible
✅ Fully tested and CI/CD ready

Try it yourself:
🔗 GitHub: https://github.com/hongping-zh/circular-bias-detection
🌐 Web App: https://is.gd/check_sleuth?dataset=latest
📊 Dataset: https://doi.org/10.5281/zenodo.17637303

We'd love your feedback! What features would you like to see next?

#ArtificialIntelligence #MachineLearning #DataScience #ResearchIntegrity #OpenScience #MLOps #Python
```

## Reddit Posts

### r/MachineLearning
**Title**: [P] Circular Bias Detection v1.2.0 - One-line command, web demo, and Python package

```
Hi r/MachineLearning!

We just released v1.2.0 of our circular bias detection framework. Three major features:

**1. One-Line CLI Command**
```bash
circular-bias detect zenodo://17637303
```
Analyzes the latest real-world AI evaluation dataset. Auto-selects the largest CSV, caches it, and gives you results in under a minute.

**2. Interactive Web Demo**
https://is.gd/check_sleuth?dataset=latest

New banner on homepage lets you try the latest dataset with one click. Great for sharing with colleagues or using in tutorials.

**3. Lightweight Python Package**
```python
from cbd import detect_bias, SklearnCBDModel

model = SklearnCBDModel(LogisticRegression().fit(X_train, y_train))
result = detect_bias(model, X_test, y_test, metric=accuracy_score)

print(result["p_value"])  # 0.002
print(result["conclusion"])  # "Suspicious: potential circular bias"
```

**What it does:**
Detects circular reasoning bias in model evaluation using permutation testing. Helps catch cases where you've inadvertently leaked information from training/evaluation back into your model.

**Why it matters:**
- Pre-publication checks (avoid reviewer comments)
- Pre-production audits (ensure performance is real)
- Teaching/research integrity

**Tech stack:**
- Python 3.9+
- Scikit-learn integration (PyTorch/TF adapters coming)
- GitHub Actions CI/CD
- 100% client-side web app (Pyodide/WebAssembly)

**Dataset:**
CBD v3/v3.1 with real-world scenarios (DOI: 10.5281/zenodo.17637303)

**Links:**
- GitHub: https://github.com/hongping-zh/circular-bias-detection
- Web App: https://is.gd/check_sleuth?dataset=latest
- Docs: https://github.com/hongping-zh/circular-bias-detection#readme

**What's new in v1.2.0:**
- Smart file selection for Zenodo records
- URL parameter support for shareable demos
- Type-safe Python API with Protocol-based design
- Complete documentation and examples

Would love feedback from the community! What features would you like to see?

**Installation:**
```bash
git clone https://github.com/hongping-zh/circular-bias-detection.git
cd circular-bias-detection
pip install -e .
```

**Quick test:**
```bash
circular-bias detect zenodo://17637303
# or
python examples/quickstart.py
```
```

### r/Python
**Title**: [Project] CBD v1.2.0 - Lightweight package for detecting bias in ML models

```
Released a new Python package for detecting circular reasoning bias in machine learning evaluation.

**Quick example:**
```python
from cbd import detect_bias, SklearnCBDModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Train model
clf = LogisticRegression().fit(X_train, y_train)

# Wrap and test
model = SklearnCBDModel(clf)
result = detect_bias(
    model, X_test, y_test,
    metric=accuracy_score,
    n_permutations=1000
)

print(f"p-value: {result['p_value']}")
print(f"Conclusion: {result['conclusion']}")
```

**Features:**
- Protocol-based design (works with any model implementing `predict()`)
- Type-safe with full type hints
- Sklearn adapter included
- Permutation testing for statistical rigor
- Easy MLOps integration (MLflow, W&B examples included)

**Use cases:**
- Validate evaluation protocols before publication
- Audit models before production deployment
- Teaching research integrity

**Installation:**
```bash
pip install -e git+https://github.com/hongping-zh/circular-bias-detection.git#egg=circular-bias-detector
```

**Links:**
- GitHub: https://github.com/hongping-zh/circular-bias-detection
- Docs: https://github.com/hongping-zh/circular-bias-detection/blob/main/cbd/README.md
- Web demo: https://is.gd/check_sleuth

Feedback welcome!
```

## Hacker News

**Title**: Circular Bias Detection v1.2.0 – Detect evaluation bias in ML models

```
We just released v1.2.0 of our circular bias detection framework.

The problem: When developing ML models, it's easy to inadvertently leak information from your training or evaluation process back into the model (e.g., through hyperparameter tuning, prompt engineering, or dataset selection). This produces overly optimistic metrics that don't hold up in production.

Our solution: Statistical permutation testing to detect when your model's performance is suspiciously high relative to a null distribution.

New in v1.2.0:
- One-line CLI: `circular-bias detect zenodo://17637303`
- Interactive web demo with URL parameters
- Lightweight Python package with sklearn adapter

Example:
```python
from cbd import detect_bias, SklearnCBDModel
result = detect_bias(model, X_test, y_test, metric=accuracy_score)
# Returns p-value and conclusion
```

The web app runs entirely client-side using Pyodide (Python in WebAssembly), so no data leaves your browser.

Links:
- GitHub: https://github.com/hongping-zh/circular-bias-detection
- Web app: https://is.gd/check_sleuth?dataset=latest
- Dataset: https://doi.org/10.5281/zenodo.17637303

Would love feedback from the HN community!
```

## Dev.to Blog Post Outline

**Title**: Introducing Circular Bias Detection v1.2.0: Three Ways to Detect Bias in Your ML Models

**Sections:**

1. **The Problem**
   - What is circular reasoning bias?
   - Real-world examples
   - Why it matters

2. **Solution 1: CLI Tool**
   - Installation
   - One-line command demo
   - Output interpretation

3. **Solution 2: Web App**
   - No installation needed
   - Interactive demo
   - Shareable links

4. **Solution 3: Python Package**
   - Integration examples
   - MLOps workflows
   - Custom metrics

5. **Under the Hood**
   - Permutation testing explained
   - Statistical rigor
   - Performance considerations

6. **Getting Started**
   - Installation guide
   - First analysis
   - Next steps

7. **Roadmap**
   - Upcoming features
   - Community contributions
   - Feedback welcome

## YouTube Video Script (5 min)

**Title**: Circular Bias Detection v1.2.0 - Detect Bias in ML Models in 3 Ways

**Script:**

[0:00-0:30] Introduction
- What is circular bias?
- Why it matters
- Three ways to use CBD

[0:30-1:30] Demo 1: CLI
- Show terminal
- Run command
- Explain output

[1:30-2:30] Demo 2: Web App
- Open browser
- Click banner
- Show results

[2:30-3:30] Demo 3: Python Package
- Show code editor
- Run example
- Integrate with MLflow

[3:30-4:30] Technical Deep Dive
- Permutation testing
- Statistical interpretation
- Best practices

[4:30-5:00] Call to Action
- Try it yourself
- Star on GitHub
- Join discussions

## Email Newsletter

**Subject**: 🎉 CBD v1.2.0 Released - Three New Ways to Detect Bias

**Body:**

Hi [Name],

Exciting news! We just released Circular Bias Detection v1.2.0 with three major features:

**1. One-Line CLI Command** ⚡
```bash
circular-bias detect zenodo://17637303
```
No setup, no config files. Just run and get results.

**2. Interactive Web Demo** 🌐
Visit: https://is.gd/check_sleuth?dataset=latest
Try our latest dataset with one click. Perfect for demos and teaching.

**3. Python Package** 📦
```python
from cbd import detect_bias, SklearnCBDModel
result = detect_bias(model, X, y, metric=accuracy_score)
```
Integrate bias detection into your ML pipelines.

**What's Included:**
✅ Real-world AI evaluation dataset (CBD v3/v3.1)
✅ Complete documentation and examples
✅ Automated testing and CI/CD
✅ 100% backward compatible

**Try It Now:**
- CLI: Install and run in < 1 minute
- Web: No installation needed
- Package: pip install -e .

**Links:**
- GitHub: https://github.com/hongping-zh/circular-bias-detection
- Web App: https://is.gd/check_sleuth?dataset=latest
- Docs: Full documentation available

Questions? Reply to this email or open an issue on GitHub.

Best,
The CBD Team

---

P.S. We'd love your feedback! What features would you like to see in v1.3.0?
```

---

**Created**: 2025-11-18  
**Purpose**: Social media announcements for v1.2.0 release  
**Platforms**: Twitter/X, LinkedIn, Reddit, Hacker News, Dev.to, YouTube, Email
