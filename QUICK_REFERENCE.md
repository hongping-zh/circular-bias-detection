# 🚀 CBD Dataset v3/v3.1 快速参考

## 一行命令 ⚡
```bash
circular-bias detect zenodo://17637303
```

## 常用命令 📋

| 命令 | 说明 |
|------|------|
| `circular-bias detect zenodo://17637303` | 分析数据集（自动选择最大 CSV） |
| `circular-bias info zenodo://17637303` | 查看数据集信息 |
| `circular-bias cache list` | 查看缓存列表 |
| `circular-bias cache clear --record-id 17637303` | 清除缓存 |

## 输出格式 📊

```bash
# 文本格式（默认）
circular-bias detect zenodo://17637303

# JSON 格式
circular-bias detect zenodo://17637303 --format json --output results.json

# CSV 格式
circular-bias detect zenodo://17637303 --format csv --output results.csv
```

## 自定义参数 ⚙️

```bash
circular-bias detect zenodo://17637303 \
    --algorithm decision \
    --psi-threshold 0.15 \
    --ccs-threshold 0.85 \
    --rho-threshold 0.5 \
    --verbose
```

## Python API 🐍

```python
from circular_bias_cli.utils.zenodo_loader import ZenodoLoader

# 加载数据
loader = ZenodoLoader()
df = loader.load('zenodo://17637303')

# 查看缓存
cached = loader.list_cached()

# 清除缓存
loader.clear_cache('17637303')
```

## 缓存位置 📁
```
~/.circular-bias/cache/
├── metadata.json          # 缓存元数据
└── *.csv                  # 缓存的数据文件
```

## 支持的 URI 格式 🔗

| URI | 说明 |
|-----|------|
| `zenodo://17637303` | 自动选择最大 CSV |
| `zenodo://17637303/file.csv` | 指定文件 |
| `zenodo://17637303/v3.1` | 指定版本 |
| `zenodo://17637303/v3.1/file.csv` | 指定版本和文件 |

## 引用格式 📚

```bibtex
@dataset{zhang2024_cbd_v3,
  author    = {Zhang, Hongping and CBD Project Team},
  title     = {Circular Bias Detection (CBD) dataset (v3/v3.1)},
  year      = {2025},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.17637303}
}
```

## 相关链接 🔗

- **Zenodo**: https://doi.org/10.5281/zenodo.17637303
- **GitHub**: https://github.com/hongping-zh/circular-bias-detection
- **Web App**: https://is.gd/check_sleuth
- **详细文档**: [ZENODO_17637303_USAGE.md](ZENODO_17637303_USAGE.md)

---

💡 **提示**: 首次运行会下载数据并缓存，后续运行直接使用缓存，速度更快！
