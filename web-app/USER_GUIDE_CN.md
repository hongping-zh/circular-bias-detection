# 🔍 循环偏差扫描器 - 用户指南

**在线体验：** https://hongping-zh.github.io/circular-bias-detection/

## 📖 什么是循环偏差扫描器？

循环偏差扫描器是一个免费的、基于浏览器的工具，用于检测AI算法评估中的循环推理偏差。它能识别评估协议是否被操纵以偏袒特定算法，确保研究诚信和公平比较。

### 为什么使用这个工具？

**传统的偏差检测工具关注模型输出**（如预测中的公平性），而**本工具关注评估过程本身**——检测评估规则是否在中途被改变以产生期望的结果。

**使用场景：**
- 📄 审查算法比较论文
- 🔍 审计已发表的评估方法
- ✅ 发表前验证研究诚信
- 🎓 教授研究方法最佳实践

---

## ✨ 核心特性

### 🚀 零安装
- 无需注册
- 无需软件安装
- 直接在浏览器中运行
- 兼容Chrome、Firefox、Safari、Edge

### 🔒 隐私优先
- **100%客户端处理**
- 数据不会离开您的计算机
- 无服务器上传
- 不收集或跟踪数据

### ⚡ 快速结果
- 检测在30秒内完成
- 即时可视化反馈
- 三个统计指标（PSI、CCS、ρ_PC）
- 清晰的解释和置信度评分

### 📊 多种数据源
- **上传自己的CSV** - 分析您的评估数据
- **使用示例数据** - 使用Zenodo数据集样本试用
- **生成合成数据** - 使用模拟场景测试

### 📥 导出与分享
- 下载JSON格式结果
- 一键复制引用
- 与合作者分享结果

---

## 🎯 使用方法

### 第1步：访问工具

访问：**https://hongping-zh.github.io/circular-bias-detection/**

**首次加载：** Python引擎（PyOdide）可能需要30-60秒加载。这只会发生一次——后续访问将立即显示。

**注意：** 当前版本使用测试模式和模拟数据。完整的Python检测即将推出。

---

### 第2步：加载数据

您有三个选项：

#### 选项A：上传自己的数据 📁

1. 点击 **"📁 Upload Your Data"** 或拖放您的CSV文件
2. 确保您的CSV包含以下必需列：

| 列名 | 类型 | 描述 | 示例 |
|------|------|------|------|
| `time_period` | int | 评估周期（1, 2, 3...） | 1, 2, 3... |
| `algorithm` | string | 算法名称 | ResNet, VGG |
| `performance` | float | 性能得分 [0-1] | 0.72, 0.85 |
| `constraint_compute` | float | 计算约束 | 300, 450 |
| `constraint_memory` | float | 内存限制（GB） | 8.0, 12.0 |
| `constraint_dataset_size` | int | 数据集大小 | 50000, 100000 |
| `evaluation_protocol` | string | 协议版本 | v1.0, v1.1 |

3. 上传后，您将看到：**✓ your_file.csv**

**CSV格式示例：**
```csv
time_period,algorithm,performance,constraint_compute,constraint_memory,constraint_dataset_size,evaluation_protocol
1,ResNet,0.72,300,8.0,50000,ImageNet-v1.0
1,VGG,0.68,450,12.0,50000,ImageNet-v1.0
2,ResNet,0.73,305,8.2,51000,ImageNet-v1.0
2,VGG,0.69,455,12.1,51000,ImageNet-v1.0
```

#### 选项B：使用示例数据 📊

1. 点击 **"📊 Try Example from Zenodo"**
2. 预加载来自我们研究数据集的数据（DOI: 10.5281/zenodo.17201032）
3. 非常适合首次用户了解工具

#### 选项C：生成合成数据 🎲

1. 点击 **"🎲 Generate Synthetic Data"**
2. 自动创建随机评估数据
3. 用于测试和演示

---

### 第3步：运行检测

1. 加载数据后，**"🔍 Scan for Bias"** 按钮变为可用（绿色）
2. 点击按钮开始分析
3. 处理时按钮变为 **"Scanning..."**（橙色）
4. 等待1-2秒获取结果

---

### 第4步：解读结果

结果仪表板显示三个关键指标：

#### 📊 PSI得分（性能-结构独立性）
- **测量内容：** 参数随时间的稳定性
- **阈值：** 0.15
- **解释：**
  - PSI < 0.10：✅ 稳定（良好）
  - 0.10 ≤ PSI < 0.15：⚠️ 中等
  - PSI ≥ 0.15：❌ 不稳定（潜在偏差）

**示例：** PSI = 0.0158 → 参数非常稳定，评估一致。

#### 📊 CCS得分（约束一致性得分）
- **测量内容：** 约束规范的一致性
- **阈值：** 0.85
- **解释：**
  - CCS ≥ 0.90：✅ 高度一致（良好）
  - 0.85 ≤ CCS < 0.90：⚠️ 中等
  - CCS < 0.85：❌ 不一致（潜在偏差）

**示例：** CCS = 0.9422 → 约束在各个周期中高度一致。

#### 📊 ρ_PC得分（性能-约束相关性）
- **测量内容：** 性能与约束之间的相关性
- **阈值：** ±0.5
- **解释：**
  - |ρ_PC| < 0.3：✅ 弱相关（良好）
  - 0.3 ≤ |ρ_PC| < 0.5：⚠️ 中等
  - |ρ_PC| ≥ 0.5：❌ 强相关（潜在偏差）

**示例：** ρ_PC = +0.9921 → 非常强的正相关，约束可能根据性能进行了调整。

#### 🎯 总体判定

工具结合所有三个指标：

- **检测到偏差：** 3个指标中≥2个被触发
- **无偏差：** <2个指标被触发
- **置信度：** 触发指标的百分比（33.3%、66.7%或100%）

**结果示例：**
```
Overall Bias Detected: NO ✓
Confidence: 33.3%

Interpretation:
未检测到循环偏差（置信度：33.3%）。
评估似乎是可靠的。
```

---

### 第5步：导出与分享

#### 下载报告 📥
1. 点击 **"📥 Download Report (JSON)"**
2. 下载包含完整结果的JSON文件
3. 与审稿人分享或存档记录

**JSON格式：**
```json
{
  "psi": 0.0158,
  "ccs": 0.9422,
  "rho_pc": 0.9921,
  "overall_bias": false,
  "confidence": 0.333,
  "details": {
    "algorithms_evaluated": ["ResNet", "VGG", "DenseNet", "EfficientNet"],
    "time_periods": 5,
    "indicators_triggered": 1
  }
}
```

#### 复制引用 📋
1. 点击 **"📋 Copy Citation"**
2. BibTeX引用已复制到剪贴板
3. 粘贴到论文的参考文献中

#### 开始新分析 ↻
- 点击 **"← New Scan"** 返回数据输入
- 分析不同的数据集

---

## 🔬 技术规格

### 统计方法

#### PSI（性能-结构独立性）
```
PSI = mean(|Δθ_t|)
```
测量参数在时间周期内的绝对变化。

#### CCS（约束一致性得分）
```
CCS = mean(corr(C_i, C_j)) 对于所有周期对
```
计算时间上约束向量之间的平均相关性。

#### ρ_PC（性能-约束相关性）
```
ρ_PC = Pearson(mean(P_t), mean(C_t))
```
计算平均性能与约束强度之间的相关性。

### 决策框架

```
overall_bias = (PSI > 0.15) + (CCS < 0.85) + (|ρ_PC| > 0.5) ≥ 2
confidence = (indicators_triggered / 3) × 100%
```

---

## 💡 最佳实践

### 数据准备

1. **最低数据要求：**
   - 至少3个时间周期（T ≥ 3）
   - 至少2个算法（K ≥ 2）
   - 至少2种约束类型（p ≥ 2）

2. **确保数据质量：**
   - 无缺失值
   - 各周期算法名称一致
   - 性能值在[0, 1]范围内
   - 约束值为正数

3. **时间周期定义：**
   - 每行代表一个周期中的一个算法
   - 周期应连续（1, 2, 3, ...）
   - 所有算法应出现在每个周期

### 解释指南

1. **单个指标被触发：**
   - 需要进一步调查但不确定
   - 可能由于自然变异
   - 检查数据质量

2. **两个指标被触发：**
   - 潜在偏差的强有力证据
   - 建议详细的人工审查
   - 考虑额外验证

3. **所有三个指标被触发：**
   - 循环偏差的高置信度
   - 评估方法可能被操纵
   - 结果不应被信任

### 常见陷阱

❌ **不要：**
- 使用少于3个时间周期的数据
- 混合不同的评估任务
- 包含缺失值
- 跨不同基准比较

✅ **要：**
- 使用一致的评估协议
- 包含所有约束类型
- 记录任何协议变更
- 归档原始数据以保证可重现性

---

## ❓ 常见问题

### 一般问题

**Q：这个工具是免费的吗？**  
A：是的，完全免费且开源（CC BY 4.0）。

**Q：我需要创建账户吗？**  
A：不需要，无需注册或登录。

**Q：我的数据安全吗？**  
A：是的，所有处理都在您的浏览器本地进行。数据永远不会离开您的计算机。

**Q：支持哪些浏览器？**  
A：Chrome、Firefox、Safari、Edge——任何支持JavaScript的现代浏览器。

### 技术问题

**Q：检测的准确性如何？**  
A：在合成场景中准确率为93.2%，在真实案例研究中为87-91%（见论文）。

**Q：我可以调整阈值吗？**  
A：Web应用使用默认阈值。使用CLI工具自定义阈值：
```bash
circular-bias detect data.csv --psi-threshold 0.2 --ccs-threshold 0.8
```

**Q：如果我只有2个时间周期怎么办？**  
A：可靠检测需要至少3个周期。使用2个周期，结果可能不可靠。

**Q：我可以分析多个评估任务吗？**  
A：分别分析每个任务。不要在一次分析中混合ImageNet和GLUE评估。

### 数据格式问题

**Q：我的CSV有不同的列名。可以使用吗？**  
A：列名必须完全匹配。上传前在电子表格中重命名列。

**Q：如果我有超过3个约束怎么办？**  
A：包含所有约束列（constraint_*）。工具将分析所有这些。

**Q：我可以使用准确率而不是性能吗？**  
A：可以，但要标准化到[0, 1]范围并将列重命名为`performance`。

**Q：evaluation_protocol应该填什么？**  
A：任何版本标识符（如"v1.0"、"baseline"、"protocol_A"）。协议变更时应更改。

### 结果解释

**Q：所有三个指标都是绿色，但我怀疑有偏差。为什么？**  
A：工具检测统计模式。对于关键决策，始终建议人工审查。

**Q：一个指标是红色，我应该担心吗？**  
A：单个指标可能是误报。需要调查但不确定。关注2+个指标。

**Q：工具能检测其他类型的偏差吗？**  
A：不能，此工具专门检测评估协议中的**循环推理偏差**。对于模型输出偏差，使用AIF360或Fairlearn等工具。

### 故障排除

**Q：页面卡在"Loading Python engine..."**  
A：首次加载需要30-60秒。如果卡住超过2分钟，请刷新页面。当前测试版本跳过此步骤。

**Q：上传按钮不工作**  
A：确保文件是CSV格式且<10MB。如果问题持续，尝试不同的浏览器。

**Q：结果显示"NaN"或错误**  
A：检查数据格式，确保没有缺失值，验证所有必需列都存在。

---

## 📚 其他资源

### 文档
- **GitHub仓库：** https://github.com/hongping-zh/circular-bias-detection
- **研究论文：**（已提交至JASA）
- **数据集：** https://doi.org/10.5281/zenodo.17201032

### CLI工具
面向高级用户和自动化：
```bash
pip install circular-bias-detector[cli]
circular-bias detect data.csv --format json
```

### Python API
集成到您的工作流程：
```python
from circular_bias_detector import BiasDetector
detector = BiasDetector()
results = detector.detect_bias(performance_matrix, constraint_matrix)
```

### 支持
- **问题反馈：** https://github.com/hongping-zh/circular-bias-detection/issues
- **邮箱：** yujjam@uest.edu.gr

---

## 📄 引用

如果您在研究中使用此工具，请引用：

```bibtex
@software{zhang2024biasscanner,
  author = {Zhang, Hongping},
  title = {Circular Bias Scanner: Web Tool for Evaluation Bias Detection},
  year = {2024},
  url = {https://hongping-zh.github.io/circular-bias-detection/}
}

@dataset{zhang2024dataset,
  author = {Zhang, Hongping},
  title = {Algorithm Benchmark Suite v2.0: Synthetic Dataset for Circular Bias Detection},
  year = {2024},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.17201032}
}
```

---

## 📝 许可证

CC BY 4.0 - 可自由使用、分享和改编，但需注明出处。

---

**版本：** 1.0.0（MVP - 测试模式）  
**最后更新：** 2024年10月  
**反馈：** https://github.com/hongping-zh/circular-bias-detection/issues
