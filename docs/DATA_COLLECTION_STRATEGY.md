# 数据收集策略：Hugging Face 数据�?
## 目标

寻找高风险数据集或易于构造泄露的基石数据集，以验�?CBD 框架在检测训练数据与评估数据交叉污染方面的能力�?
---

## 策略 A：目标寻�?交叉污染"的评估基�?
我们寻找那些基于大型通用语料库（�?Wikipedia、C4）构建，且存在高重叠风险的评估数据集�?
### 1. 机器翻译评估�?
**关键�?筛选条件：**
```
translation + en-zh
translation + wmt
translation + flores
```

**目标数据集：**
- `wmt14`, `wmt19` - WMT 机器翻译竞赛数据�?- `flores` - Facebook 多语言翻译基准
- `iwslt2017` - 国际口语翻译研讨会数�?
**潜在风险�?*
- 句子结构重用，特别是经典或官方术语的重用
- 训练语料与评估语料可能来自相同的新闻源或维基百科版本

**为什么重要：**
- 易于检测表面和中度泄露
- 语义相似度高，适合测试 CBD 的语义重写检测能�?
**Hugging Face 查询命令�?*
```python
from datasets import load_dataset

# 示例：加�?WMT14 英德翻译数据�?dataset = load_dataset("wmt14", "de-en")

# 示例：加�?FLORES-200 多语言数据�?dataset = load_dataset("facebook/flores", "eng_Latn-zho_Hans")
```

---

### 2. 摘要数据�?
**关键�?筛选条件：**
```
summarization + cnn_dailymail
summarization + xsum
abstractive summarization
```

**目标数据集：**
- `cnn_dailymail` - CNN/DailyMail 新闻摘要
- `xsum` - BBC 新闻极端摘要
- `multi_news` - 多文档摘�?
**潜在风险�?*
- 评估问题（提示）与源文档中的句子高度相似
- 训练数据与评估数据的源头相同（新闻文章），风险极�?- 模型可能记忆了特定新闻事件的描述

**为什么重要：**
- 摘要任务天然容易产生泄露，因为输入和输出都来自同一文档
- 可以测试 CBD 在检�?部分文本重叠"方面的能�?
**Hugging Face 查询命令�?*
```python
# CNN/DailyMail 摘要数据�?dataset = load_dataset("cnn_dailymail", "3.0.0")

# XSum 极端摘要数据�?dataset = load_dataset("xsum")
```

---

### 3. 开放域问答

**关键�?筛选条件：**
```
qa + open-domain
question-answering + wikipedia
natural questions
trivia qa
```

**目标数据集：**
- `natural_questions` - Google Natural Questions
- `trivia_qa` - TriviaQA 问答基准
- `squad` - Stanford Question Answering Dataset
- `hotpot_qa` - 多跳推理问答

**潜在风险�?*
- 问题和参考答案可能直接来�?Wikipedia 的某个版�?- 与训练数据源（如 Common Crawl、Wikipedia dumps）重叠极�?- 知识型泄露的经典来源

**为什么重要：**
- 开放域问答�?LLM 评估的核心场�?- 可以直接测试 CBD �?知识记忆型泄�?的检测能�?
**Hugging Face 查询命令�?*
```python
# Natural Questions
dataset = load_dataset("natural_questions")

# TriviaQA
dataset = load_dataset("trivia_qa", "unfiltered")

# SQuAD v2.0
dataset = load_dataset("squad_v2")
```

---

### 4. 检索增强生�?(RAG) 评估�?
**关键�?筛选条件：**
```
retrieval + wikipedia
rag + evaluation
ms_marco
```

**目标数据集：**
- `ms_marco` - Microsoft Machine Reading Comprehension
- `beir` - Benchmarking IR (信息检索基�?
- `wiki_qa` - Wikipedia 问答�?
**潜在风险�?*
- 检索到的文档片段本身可能就是训练数据的一部分
- 上下文泄露：模型可能已经"看过"检索文�?- 检索器和生成器的双重泄露风�?
**为什么重要：**
- 验证 CBD �?RAG 场景下的能力
- 测试多阶段系统（检�?+ 生成）的泄露检�?
**Hugging Face 查询命令�?*
```python
# MS MARCO
dataset = load_dataset("ms_marco", "v2.1")

# BEIR 基准
# 注意：BEIR 需要单独安�?beir �?from beir import util, datasets as beir_datasets
dataset = "nfcorpus"
data_path = util.download_and_unzip(f"https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{dataset}.zip", "datasets")
```

---

## 策略 B：获�?训练�?代表性样�?
为了进行真实的交叉检测，我们需要一�?*"通用训练�?的代表性样�?*�?
### 1. 通用知识语料

**目标数据：Wikipedia**

**建议来源�?*
- `wikipedia` (2022/2023 versions)
- 特定语言版本：`20220301.en`, `20230301.en`

**筛选策略：**
- 筛选出包含特定知识实体的文章（例如：历史事件、名人传记、科学概念）
- 按类别采样：科技、历史、地理、艺术等
- 提取关键段落（而非全文），模拟训练数据的片段化特�?
**用途：**
- 作为模拟�?LLM 训练集输�?- 构建"已知泄露"的基准数据集

**Hugging Face 查询命令�?*
```python
# Wikipedia 2022�?月版本（英文�?dataset = load_dataset("wikipedia", "20220301.en")

# 随机采样 10,000 个文�?sampled_docs = dataset["train"].shuffle(seed=42).select(range(10000))
```

---

### 2. 对话/网络文本

**目标数据：C4 �?The Pile**

**建议来源�?*
- `c4` - Colossal Clean Crawled Corpus
- `the_pile` - EleutherAI 的大规模训练语料（需特殊访问�?- `openwebtext` - Reddit 提取的网络文�?
**筛选策略：**
- 随机采样 10,000 个文档片�?- 按领域分层采样：新闻、论坛、博客、问答网�?- 保留原始噪音（拼写错误、口语化表达），使模拟更真实

**用途：**
- 增加训练集的多样性和噪音
- 模拟真实 LLM 预训练语料的多样�?- 测试 CBD 在低质量、高噪音数据上的鲁棒�?
**Hugging Face 查询命令�?*
```python
# C4 数据集（en 版本�?dataset = load_dataset("c4", "en", streaming=True)

# 采样 10,000 个样本（由于数据集巨大，使用流式加载�?sampled = []
for i, item in enumerate(dataset["train"]):
    if i >= 10000:
        break
    sampled.append(item)

# OpenWebText
dataset = load_dataset("openwebtext")
sampled_docs = dataset["train"].shuffle(seed=42).select(range(10000))
```

---

## 可实施的下一步行�?
### 步骤 1：初步数据搜索与下载
```python
# 使用 datasets 库搜索关键词
from datasets import list_datasets

# 搜索相关数据�?translation_datasets = [d for d in list_datasets() if "translation" in d.lower()]
qa_datasets = [d for d in list_datasets() if "qa" in d.lower() or "question" in d.lower()]
summarization_datasets = [d for d in list_datasets() if "summarization" in d.lower() or "summary" in d.lower()]

print("Translation datasets:", translation_datasets[:10])
print("QA datasets:", qa_datasets[:10])
print("Summarization datasets:", summarization_datasets[:10])
```

### 步骤 2：下�?2-3 个小型数据集进行初筛
```python
# 下载优先级列表（按易用性和代表性排序）
priority_datasets = [
    ("squad_v2", "问答", "�?),
    ("cnn_dailymail", "摘要", "�?),
    ("wmt14", "翻译", "�?),
    ("natural_questions", "问答", "�?),
    ("wikipedia", "训练集代�?, "�?)
]

# 示例：下�?SQuAD v2.0
from datasets import load_dataset
squad = load_dataset("squad_v2")
print(f"SQuAD v2 train size: {len(squad['train'])}")
print(f"Sample: {squad['train'][0]}")
```

### 步骤 3：数据预处理与格式化
```python
# 将下载的数据集转换为 CBD 框架所需的格�?# 提取三元组：(训练样本, 评估问题, 标签)

def extract_qa_pairs(dataset, split="train", max_samples=1000):
    """从问答数据集提取样本"""
    samples = []
    for i, item in enumerate(dataset[split]):
        if i >= max_samples:
            break
        samples.append({
            "context": item["context"],
            "question": item["question"],
            "answers": item["answers"]
        })
    return samples

# 示例使用
qa_pairs = extract_qa_pairs(squad, split="validation", max_samples=500)
```

---

## 数据质量评估标准

在下载和使用数据集之前，我们需要评估以下标准：

| 标准 | 描述 | 评分方法 |
|------|------|----------|
| **相关�?* | 数据集与"交叉污染"主题的相关度 | �?�?�?|
| **数据�?* | 数据集大小是否适合实验 | < 10K: �? 10K-100K: �? > 100K: �?|
| **下载难度** | 是否易于通过 HF datasets 下载 | �?�?�?|
| **文档质量** | 数据集是否有清晰的文档说�?| �?一�?�?|
| **许可�?* | 数据集的使用许可 | 开�?限制/未知 |

---

## 预期输出

完成数据收集后，我们将得到：

1. **高风险评估数据集列表** (5-10 个数据集)
   - 每个数据集包含元信息：名称、大小、用途、风险等�?   
2. **训练集代表性样�?* (10,000-50,000 个文�?
   - Wikipedia 文章片段
   - C4/OpenWebText 网络文本片段

3. **数据集目录文�?* (`DATASET_INVENTORY.csv`)
   ```csv
   dataset_name,task_type,size,risk_level,hf_id,notes
   squad_v2,qa,150K,high,squad_v2,Wikipedia-based QA
   cnn_dailymail,summarization,300K,high,cnn_dailymail,News summarization
   wmt14,translation,4.5M,medium,wmt14,Machine translation
   ...
   ```

4. **初步泄露检测报�?*
   - 对下载的数据集运�?CBD 框架的初步分�?   - 识别哪些数据集最适合构建案例研究

---

## 时间�?
- **�?1 天：** 数据集搜索与评估（完成数据集目录�?- **�?2-3 天：** 下载和预处理优先级数据集
- **�?4-5 天：** 构建"训练集代表性样�?
- **�?6-7 天：** 初步泄露检测实验，筛选最佳案�?
---

## 参考资�?
### Hugging Face 数据集搜索页�?- https://huggingface.co/datasets

### 关键数据集链�?- SQuAD v2: https://huggingface.co/datasets/squad_v2
- CNN/DailyMail: https://huggingface.co/datasets/cnn_dailymail
- Natural Questions: https://huggingface.co/datasets/natural_questions
- Wikipedia: https://huggingface.co/datasets/wikipedia
- C4: https://huggingface.co/datasets/c4

---

**最后更新：** 2024-10-27
**负责人：** Hongping Zhang
**状态：** 待实�?
