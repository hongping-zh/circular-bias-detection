# 🚀 Google Colab 使用指南

## 📋 快速开始（5 分钟）

### 步骤 1：上传 Notebook

1. 访问 [Google Colab](https://colab.research.google.com/)
2. 点击 **文件 → 上传笔记本**
3. 选择 `CBD_GPU_Colab.ipynb`

### 步骤 2：启用 GPU

1. 点击菜单：**运行时 → 更改运行时类型**
2. 硬件加速器：选择 **GPU**
3. 点击 **保存**

### 步骤 3：运行测试

1. 点击 **运行时 → 全部运行**
2. 或者按 `Ctrl+F9`（全部运行）
3. 等待约 3-5 分钟完成

### 步骤 4：查看结果

测试完成后会显示：
- GPU 加速比（预计 10-15x）
- 吞吐量提升（预计 ~400k 样本/秒）
- 性能图表

---

## 📊 预期结果（Colab T4 GPU）

### 性能指标

| 数据集规模 | 时间 | 吞吐量 |
|-----------|------|--------|
| 1k 样本 | ~0.01 秒 | ~100k/秒 |
| 10k 样本 | ~0.025 秒 | ~400k/秒 |
| 50k 样本 | ~0.12 秒 | ~420k/秒 |

### GPU 信息

```
GPU: Tesla T4
VRAM: 15.0 GB
CUDA: 11.8
```

---

## 🎯 Notebook 结构

本 Notebook 包含 8 个主要步骤：

### 1️⃣ 验证 GPU 环境
检查 GPU 是否可用和配置信息

### 2️⃣ 安装依赖
自动安装所需的 Python 包

### 3️⃣ 定义检测器
加载 CBD GPU 检测器代码

### 4️⃣ 初始化
创建检测器实例

### 5️⃣ 性能测试
运行 1k, 10k, 50k 样本的基准测试

### 6️⃣ 可视化结果
生成性能对比图表

### 7️⃣ 下载结果
下载 JSON 数据和图表

### 8️⃣ GPU vs CPU 对比（可选）
对比 GPU 和 CPU 性能差异

---

## 💡 使用技巧

### 分步运行

如果想逐步查看结果：
1. 点击每个 Cell 左侧的播放按钮
2. 或使用 `Shift+Enter` 逐个运行

### 修改测试规模

在步骤 5 中修改：
```python
sample_sizes = [1000, 10000, 50000]  # 可以改为 [100, 500, 1000]
```

### 调整批处理大小

如果遇到内存不足：
```python
config = GPUConfig(
    device="cuda",
    batch_size=256,  # 从 512 降到 256
    use_fp16=True
)
```

---

## ⚠️ 常见问题

### Q1: "GPU 未启用" 错误

**解决方案：**
1. 菜单 → 运行时 → 更改运行时类型
2. 硬件加速器 → GPU
3. 保存并重新运行

### Q2: Cell 运行很慢

**可能原因：**
- 首次运行需要下载模型（~100MB）
- 正常，预热后会更快
- Colab 免费版有时会限速

### Q3: 会话断开

**解决方案：**
- Colab 免费版会话限制 12 小时
- 保存结果后可重新运行
- 考虑升级到 Colab Pro

### Q4: Out of Memory 错误

**解决方案：**
```python
# 减小批处理大小
config = GPUConfig(batch_size=256)

# 或减小测试规模
sample_sizes = [1000, 5000]  # 不要测试 50k
```

---

## 📥 下载文件

Notebook 会生成以下文件：

1. **`cbd_gpu_results.json`**
   - 性能测试的原始数据
   - 包含时间、吞吐量等指标

2. **`cbd_gpu_performance.png`**
   - 性能对比图表
   - 可用于报告和演示

**下载方式：**
- 自动下载（步骤 7）
- 或在文件浏览器中右键 → 下载

---

## 🔄 保存和分享

### 保存到 Google Drive

1. 点击 **文件 → 在云端硬盘中保存副本**
2. 下次可直接从 Drive 打开

### 分享 Notebook

1. 点击右上角 **共享**
2. 设置权限（查看/编辑）
3. 复制链接分享

### 导出为其他格式

1. **文件 → 下载 → 下载 .ipynb**（Notebook 格式）
2. **文件 → 下载 → 下载 .py**（Python 脚本）
3. **文件 → 打印**（PDF 格式）

---

## 📈 升级选项

### Colab Pro（$9.99/月）

**优势：**
- 更快的 V100 GPU
- 更长的运行时间（24 小时）
- 更少的使用限制
- 更快的速度

**适合：**
- 频繁使用（每周 > 3 次）
- 需要处理更大数据集
- 开发和实验阶段

### Colab Pro+（$49.99/月）

**优势：**
- A100 GPU（最快）
- 40 GB VRAM
- 更高优先级
- 后台执行

**适合：**
- 大规模数据处理
- 生产级测试
- 专业研究

---

## 🎓 下一步学习

### 如果测试成功

1. ✅ 了解完整的 GPU 加速方案：`docs/GPU_ACCELERATION_GUIDE.md`
2. ✅ 查看部署选项：`GPU_ACCELERATION_SUMMARY.md`
3. ✅ 考虑升级到 GCP 生产环境

### 如果想深入了解

1. 📚 阅读 CBD 完整文档
2. 💻 查看完整源码：`examples/cbd_detector_gpu.py`
3. 🔧 自定义和扩展功能

---

## 📞 支持

### 遇到问题？

1. **查看文档**
   - `GPU_QUICK_START.md` - 快速开始
   - `docs/GPU_ACCELERATION_GUIDE.md` - 完整指南

2. **检查常见问题**
   - 本文档的"常见问题"章节

3. **联系支持**
   - GitHub Issues
   - 项目文档

---

## ✅ 检查清单

使用前确认：

- [ ] 已上传 Notebook 到 Colab
- [ ] 已启用 GPU 运行时
- [ ] 网络连接正常
- [ ] 有 Google 账号登录

运行后验证：

- [ ] GPU 检查通过（显示 T4 或其他 GPU）
- [ ] 所有 Cell 运行成功（无红色错误）
- [ ] 看到性能测试结果
- [ ] 生成了性能图表
- [ ] 可以下载结果文件

---

## 🎉 预期成果

完成本 Notebook 后，您将：

1. ✅ **验证 GPU 加速效果** - 实际测量 10-15x 提升
2. ✅ **获得性能数据** - 详细的时间和吞吐量指标
3. ✅ **生成可视化图表** - 用于报告和演示
4. ✅ **掌握使用方法** - 可以应用到实际项目

**典型结果：**
```
GPU (T4): 10k 样本 → 0.025 秒
CPU: 10k 样本 → 0.33 秒
加速比: 13x
吞吐量: 400k 样本/秒
```

---

## 📚 相关资源

### 本项目

- `CBD_GPU_Colab.ipynb` - 本 Notebook
- `GPU_QUICK_START.md` - 快速启动指南
- `GPU_ACCELERATION_SUMMARY.md` - 完整方案总结
- `docs/GPU_ACCELERATION_GUIDE.md` - 详细技术指南

### 外部资源

- [Google Colab 官方文档](https://colab.research.google.com/notebooks/welcome.ipynb)
- [PyTorch 教程](https://pytorch.org/tutorials/)
- [Sentence-Transformers](https://www.sbert.net/)

---

**准备好了吗？现在就上传 Notebook 到 Colab 开始测试！** 🚀

**预计耗时：** 5 分钟设置 + 3 分钟运行 = **8 分钟**

**难度：** ⭐ 简单（无需编程经验）
