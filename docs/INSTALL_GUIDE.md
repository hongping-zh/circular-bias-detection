# 安装指南

## 快速安装

### 1. 安装核心依赖

```bash
cd C:\Users\14593\CascadeProjects\circular-bias-detection

# 安装核心包（开发模式）
pip install -e .

# 安装测试依赖
pip install pytest pytest-cov
```

### 2. 验证安装

```bash
# 测试导入
python -c "from circular_bias_detector import BiasDetector; print('✓ 安装成功')"

# 运行验证脚本
python test_phase1.py
```

### 3. 运行测试（可选）

```bash
# 运行所有测试
pytest tests/ -v

# 或单独运行各模块测试
pytest tests/test_core_metrics.py -v
pytest tests/test_inference.py -v
```

---

## 完整安装选项

### 选项A: 基础安装（推荐新手）

仅安装核心功能，不包含LLM推理：

```bash
pip install -e .
pip install pytest pytest-cov
```

### 选项B: 完整安装（包含vLLM）

需要NVIDIA GPU和CUDA 11.8+：

```bash
pip install -e .
pip install pytest pytest-cov
pip install vllm  # 需要GPU支持
```

---

## 常见问题

### Q1: `pytest`命令不存在

**解决方案**:
```bash
pip install pytest pytest-cov
```

### Q2: ModuleNotFoundError: No module named 'circular_bias_detector'

**解决方案**:
```bash
# 确保在项目根目录
cd C:\Users\14593\CascadeProjects\circular-bias-detection

# 安装为可编辑模式
pip install -e .
```

### Q3: ImportError: cannot import name 'MockBackend'

**解决方案**: 已修复，重新运行即可

### Q4: vLLM安装失败

vLLM需要GPU和CUDA支持。如果没有GPU：
- 使用`MockBackend`进行测试
- 跳过需要vLLM的功能

---

## 验证安装完整性

运行此脚本检查所有组件：

```bash
python -c "
from circular_bias_detector import (
    BiasDetector,
    compute_psi,
    MockBackend,
    BiasDetectorWithInference
)
print('✓ 所有核心组件导入成功')
"
```
