# CBD Dataset v3/v3.1 (Zenodo 17637303) 使用指南

## 一行命令分析

```bash
circular-bias detect zenodo://17637303
```

## 功能特性

### 1. 自动选择最大 CSV 文件
当 Zenodo 记录包含多个 CSV 文件时，加载器会自动选择最大的文件进行分析。

### 2. 智能缓存机制
- **首次运行**：从 Zenodo 下载数据并缓存到 `~/.circular-bias/cache/`
- **后续运行**：直接从缓存加载，无需重新下载
- **缓存管理**：
  ```bash
  # 查看缓存列表
  circular-bias cache list
  
  # 清除所有缓存
  circular-bias cache clear
  
  # 清除特定记录缓存
  circular-bias cache clear --record-id 17637303
  ```

### 3. 查看数据集信息
```bash
circular-bias info zenodo://17637303
```

输出示例：
```
============================================================
Zenodo Record: 17637303
============================================================
Title: Circular Bias Detection (CBD) dataset and evaluation protocols (v3 / v3.1)
DOI: 10.5281/zenodo.17637303
Version: v3.1
Publication Date: 2025-01-15

CSV Files (3):
  - large_dataset.csv (15.23 MB)
  - medium_dataset.csv (8.45 MB)
  - small_dataset.csv (2.10 MB)
============================================================
```

## 高级用法

### 指定特定文件
```bash
# 如果你想分析特定的 CSV 文件而不是最大的
circular-bias detect zenodo://17637303/medium_dataset.csv
```

### 自定义算法和阈值
```bash
circular-bias detect zenodo://17637303 \
    --algorithm decision \
    --psi-threshold 0.15 \
    --ccs-threshold 0.85 \
    --rho-threshold 0.5
```

### 导出结果
```bash
# JSON 格式
circular-bias detect zenodo://17637303 --format json --output results.json

# CSV 格式
circular-bias detect zenodo://17637303 --format csv --output results.csv

# 文本格式（默认）
circular-bias detect zenodo://17637303 --output results.txt
```

## Python API 使用

```python
from circular_bias_cli.utils.zenodo_loader import ZenodoLoader
from circular_bias_detector import BiasDetector

# 加载数据
loader = ZenodoLoader()
df = loader.load('zenodo://17637303')

# 运行检测
detector = BiasDetector()
# ... 准备数据矩阵并运行检测
```

## 技术细节

### 缓存键生成
缓存键基于以下信息的 MD5 哈希：
- Record ID: `17637303`
- Version: `latest`（如果未指定版本）
- Filename: `all`（如果未指定文件名）

### 文件选择逻辑
```python
# 伪代码
csv_files = [f for f in record_files if f.endswith('.csv')]
target_file = max(csv_files, key=lambda f: f['size'])
```

### 支持的 URI 格式
- `zenodo://17637303` - 自动选择最大 CSV
- `zenodo://17637303/v3.1` - 指定版本
- `zenodo://17637303/specific_file.csv` - 指定文件
- `zenodo://17637303/v3.1/specific_file.csv` - 指定版本和文件

## 测试验证

运行测试脚本验证功能：
```bash
python test_zenodo_17637303.py
```

预期输出：
```
============================================================
Testing Zenodo Record 17637303 Support
============================================================

=== Test 1: Largest CSV Selection ===
✓ Loader correctly selects largest CSV (10240 bytes)

=== Test 2: Cache Mechanism ===
✓ Cache file created: c30c863aa6cda0a9.csv
✓ First load: 1 read call(s)
✓ Second load: 2 read call(s) (cache hit)

=== Test 3: CLI Integration ===
✓ CLI command executed successfully (exit code: 0)

============================================================
✓ ALL TESTS PASSED
============================================================
```

## 引用

如果在研究中使用此数据集，请引用：

```bibtex
@dataset{zhang2024_cbd_v3,
  author       = {Zhang, Hongping and CBD Project Team},
  title        = {Circular Bias Detection (CBD) dataset and evaluation protocols (v3 / v3.1)},
  year         = {2025},
  publisher    = {Zenodo},
  version      = {v3.1},
  doi          = {10.5281/zenodo.17637303},
  url          = {https://doi.org/10.5281/zenodo.17637303}
}
```

## 相关链接

- **Concept DOI (所有版本)**: https://doi.org/10.5281/zenodo.17637302
- **Version DOI (v3/v3.1)**: https://doi.org/10.5281/zenodo.17637303
- **GitHub 仓库**: https://github.com/hongping-zh/circular-bias-detection
- **Web App**: https://is.gd/check_sleuth
