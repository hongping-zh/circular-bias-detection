# Changelog - Zenodo 17637303 Support

## [2025-11-18] - CBD Dataset v3/v3.1 Integration

### ✨ Added

#### Core Features
- **智能文件选择**: Zenodo loader 现在自动选择最大的 CSV 文件（当未指定文件名时）
  - 适用于包含多个 CSV 文件的 Zenodo 记录
  - 特别优化了 `zenodo://17637303` (CBD Dataset v3/v3.1) 的支持
  - 保持向后兼容性

#### Documentation
- **README.md**: 添加了 `zenodo://17637303` 使用示例
  - Quick Start 部分新增示例
  - CLI 数据源列表新增条目
- **CLI Help**: 更新了 `circular-bias --help` 输出
  - 新增 CBD Dataset v3/v3.1 使用示例
- **ZENODO_17637303_USAGE.md**: 创建详细使用指南
  - 一行命令使用
  - 缓存管理
  - 高级用法
  - Python API 示例
  - 技术细节
- **QUICK_REFERENCE.md**: 创建快速参考卡片
- **OPTIMIZATION_SUMMARY.md**: 完整的优化总结文档

#### Testing
- **tests/test_cli.py**: 新增 3 个单元测试
  - `test_zenodo_loader_selects_largest_csv()`: 验证最大文件选择逻辑
  - `test_zenodo_cache_mechanism()`: 验证缓存机制
  - `test_cli_detect_zenodo_17637303()`: 验证 CLI 集成
- **test_zenodo_17637303.py**: 创建独立测试脚本
  - 可独立运行的完整测试套件
  - 包含详细的输出和验证

### 🔧 Changed

#### circular_bias_cli/utils/zenodo_loader.py
- **Line 158-160**: 修改默认文件选择逻辑
  ```python
  # Before:
  target_file = csv_files[0]
  
  # After:
  target_file = max(csv_files, key=lambda f: f.get('size', 0))
  ```
- **Line 6**: 添加 `zenodo://17637303` 到支持的 URI 格式文档

#### circular_bias_cli/main.py
- **Line 56-57**: 添加 CBD Dataset v3/v3.1 使用示例到 CLI help

#### README.md
- **Line 650-651**: 添加 Quick Start 示例
- **Line 670**: 添加数据源说明

### 📊 Test Results

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

### 🎯 Impact

#### User Experience
- ✅ 用户现在可以通过一行命令分析 CBD Dataset v3/v3.1
- ✅ 自动选择最合适的数据文件，无需手动指定
- ✅ 智能缓存机制提升后续使用速度

#### Code Quality
- ✅ 新增 3 个单元测试，提升测试覆盖率
- ✅ 代码逻辑更加智能和健壮
- ✅ 保持向后兼容性

#### Documentation
- ✅ 完整的使用文档和示例
- ✅ 清晰的快速参考指南
- ✅ 详细的技术说明

### 🔄 Backward Compatibility

所有改进完全向后兼容：
- ✅ 现有的 `zenodo://17201032` 继续正常工作
- ✅ 指定文件名的语法保持不变
- ✅ API 接口未发生变化
- ✅ 缓存机制保持一致

### 📝 Usage Examples

#### Before (需要手动指定文件)
```bash
# 用户需要先查看有哪些文件
circular-bias info zenodo://17637303

# 然后手动选择文件
circular-bias detect zenodo://17637303/specific_file.csv
```

#### After (一行命令搞定)
```bash
# 自动选择最大的 CSV 文件
circular-bias detect zenodo://17637303
```

### 🚀 Performance

- **首次加载**: 下载 + 缓存 + 分析
- **后续加载**: 直接从缓存读取（跳过下载）
- **缓存命中率**: 100%（相同 record_id + version + filename）

### 📦 Files Changed

#### Modified
- `circular_bias_cli/utils/zenodo_loader.py`
- `circular_bias_cli/main.py`
- `tests/test_cli.py`
- `README.md`

#### Created
- `test_zenodo_17637303.py`
- `ZENODO_17637303_USAGE.md`
- `QUICK_REFERENCE.md`
- `OPTIMIZATION_SUMMARY.md`
- `CHANGELOG_ZENODO_17637303.md` (this file)

### 🎓 Citation

如果使用此功能，请引用：

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

### 🔗 Related Links

- **Zenodo Record**: https://doi.org/10.5281/zenodo.17637303
- **Concept DOI**: https://doi.org/10.5281/zenodo.17637302
- **GitHub**: https://github.com/hongping-zh/circular-bias-detection
- **Web App**: https://is.gd/check_sleuth

---

**Note**: This optimization was implemented on 2025-11-18 to enhance user experience and support the new CBD Dataset v3/v3.1 release.
