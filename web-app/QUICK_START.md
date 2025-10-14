# 🚀 Quick Start Guide | 快速入门指南

## English | 英文

### What is this? | 这是什么？
A free web tool to detect circular reasoning bias in AI algorithm evaluation.

### How to use? | 如何使用？
1. **Visit:** https://hongping-zh.github.io/circular-bias-detection/
2. **Load data:** Upload CSV, try example, or generate synthetic data
3. **Click "Scan for Bias"**
4. **View results:** PSI, CCS, ρ_PC indicators + overall decision

### CSV Format | CSV格式
```csv
time_period,algorithm,performance,constraint_compute,constraint_memory,constraint_dataset_size,evaluation_protocol
1,ResNet,0.72,300,8.0,50000,v1.0
1,VGG,0.68,450,12.0,50000,v1.0
2,ResNet,0.73,305,8.2,51000,v1.0
2,VGG,0.69,455,12.1,51000,v1.0
```

### Key Features | 主要特性
- ✅ **No installation** - Browser-based | 无需安装 - 浏览器运行
- ✅ **Privacy-first** - Data stays local | 隐私优先 - 数据本地处理
- ✅ **Fast results** - < 30 seconds | 快速结果 - 30秒内
- ✅ **Free & open-source** | 免费开源

### Documentation | 文档
- **Full User Guide (EN):** [USER_GUIDE_EN.md](./USER_GUIDE_EN.md)
- **完整用户指南（中文）：** [USER_GUIDE_CN.md](./USER_GUIDE_CN.md)
- **GitHub:** https://github.com/hongping-zh/circular-bias-detection

---

## 中文 | Chinese

### 这是什么工具？
免费的网页工具，用于检测AI算法评估中的循环推理偏差。

### 如何使用？
1. **访问：** https://hongping-zh.github.io/circular-bias-detection/
2. **加载数据：** 上传CSV、试用示例或生成合成数据
3. **点击"Scan for Bias"**
4. **查看结果：** PSI、CCS、ρ_PC指标 + 总体判定

### 数据格式要求
您的CSV文件需要包含7列：

| 列名 | 类型 | 说明 |
|------|------|------|
| `time_period` | int | 评估周期（1, 2, 3...） |
| `algorithm` | str | 算法名称 |
| `performance` | float | 性能[0-1] |
| `constraint_compute` | float | 计算约束 |
| `constraint_memory` | float | 内存约束(GB) |
| `constraint_dataset_size` | int | 数据集大小 |
| `evaluation_protocol` | str | 协议版本 |

### 结果解释

#### PSI (性能-结构独立性)
- **< 0.10:** ✅ 稳定
- **0.10-0.15:** ⚠️ 中等
- **≥ 0.15:** ❌ 不稳定（潜在偏差）

#### CCS (约束一致性)
- **≥ 0.90:** ✅ 高度一致
- **0.85-0.90:** ⚠️ 中等
- **< 0.85:** ❌ 不一致（潜在偏差）

#### ρ_PC (性能-约束相关性)
- **|ρ| < 0.3:** ✅ 弱相关
- **0.3-0.5:** ⚠️ 中等
- **|ρ| ≥ 0.5:** ❌ 强相关（潜在偏差）

### 总体判定
- **检测到偏差：** 3个指标中≥2个触发
- **无偏差：** <2个指标触发

---

## Support | 支持

### Issues | 问题反馈
https://github.com/hongping-zh/circular-bias-detection/issues

### Email | 邮箱
yujjam@uest.edu.gr

### Dataset | 数据集
DOI: [10.5281/zenodo.17201032](https://doi.org/10.5281/zenodo.17201032)

---

## Citation | 引用

```bibtex
@software{zhang2024biasscanner,
  author = {Zhang, Hongping},
  title = {Circular Bias Scanner},
  year = {2024},
  url = {https://hongping-zh.github.io/circular-bias-detection/}
}
```

---

**Version:** 1.0.0 (MVP)  
**License:** CC BY 4.0  
**Updated:** October 2024
