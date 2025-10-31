# CBD 离线数据分析使用指南

本指南展示如何在离线数据（批处理）场景中使用 CBD 对评测流程中的“循环推理偏差（Circular Bias）”进行检测。

## 适用场景
- 已完成/批量生成的评测数据
- 希望对评测流程与模型打分器的相互依赖进行离线审计

## 输入数据约定
- X：评测样本或特征（JSONL/CSV/Parquet 均可，通过加载器适配）
- S：评分器输出（如打分/偏好，按样本对齐）
- Y：可选的参考标签或外部基准（若存在）
- 元数据（可选）：评分器配置、数据来源、提示词版本等

## Python API 最小示例
```python
from circular_bias_detector import SimpleBiasDetector  # 如有不同 API，请按实际替换
import numpy as np

# 示例：行=时间段，列=算法
performance = np.array([[0.85, 0.78], [0.87, 0.80], [0.91, 0.84]])
constraints = np.array([[512, 0.7], [550, 0.75], [600, 0.8]])

detector = SimpleBiasDetector()
result = detector.quick_check(performance, constraints)
print(result)
```

## CLI 示例（如提供）
```bash
circular-bias detect \
  data/sample_data.csv \
  --format json \
  --output artifacts/cbd_report_offline.json
```

## 输出解读
- 依赖/循环性指标：提示数据—评分器—被评对象之间的闭环风险
- 稳健性与显著性：重抽样与统计检验结果
- 建议与风险等级：指导是否需要更换基准或改造流程
