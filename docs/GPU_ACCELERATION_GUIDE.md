# CBD GPU 加速实施方�?
## 📋 概述

本文档详细说明如何在 GPU 加速框架下部署和运�?CBD (Circular Bias Detection)，以实现更高的吞吐量和更短的处理时间�?
**目标性能提升�?*
- 🎯 吞吐量提升：**10-50x**（取决于 GPU 型号�?- �?处理时间�?0k 样本�?**0.33�?�?0.01-0.03�?*
- 📊 支持规模：百万级样本的实时检�?
---

## 🎯 GPU 加速的适用场景

### 适合 GPU 加速的情况 �?
| 场景 | 数据规模 | 推荐 |
|------|----------|------|
| **生产环境部署** | > 100k 样本/�?| ⭐⭐⭐⭐�?|
| **实时检测服�?* | 低延迟要�?| ⭐⭐⭐⭐�?|
| **大规模数据集评估** | > 1M 样本 | ⭐⭐⭐⭐�?|
| **批量处理** | 多个数据集并�?| ⭐⭐⭐⭐ |
| **研究和实�?* | 频繁迭代测试 | ⭐⭐⭐⭐ |

### 不需�?GPU 的情�?�?
- 数据�?< 10k 样本
- 不频繁的一次性检�?- 开发和调试阶段
- MVP 初期验证

---

## 🔧 技术方�?
### 方案 A：基�?PyTorch �?GPU 加速（推荐�?
**优势�?*
- �?生态系统成�?- �?�?sentence-transformers 无缝集成
- �?支持�?GPU 并行
- �?丰富的优化工�?
**适用于：** 语义相似度计算（C_score 的核心）

### 方案 B：基�?CuPy �?GPU 加�?
**优势�?*
- �?NumPy-like API，迁移简�?- �?适合矩阵运算
- �?轻量�?
**适用于：** 统计计算和矩阵操�?
### 方案 C：混合加速方案（最优）

**组合使用�?*
- PyTorch + CUDA：嵌入向量计�?- CuPy：统计和矩阵运算
- 多进程：数据加载和预处理

---

## 🖥�?硬件要求

### 推荐 GPU 配置

| 使用场景 | GPU 型号 | VRAM | 预期性能 |
|----------|----------|------|----------|
| **入门�?* | NVIDIA GTX 1660 Ti | 6 GB | 10-15x 提升 |
| **标准配置** | NVIDIA RTX 3060/3070 | 8-12 GB | 20-30x 提升 |
| **高性能** | NVIDIA RTX 4090 | 24 GB | 40-50x 提升 |
| **专业�?* | NVIDIA A100/H100 | 40-80 GB | 50-100x 提升 |

### 最低要�?
- **GPU:** CUDA 计算能力 �?6.1
- **VRAM:** �?4 GB（推�?8 GB+�?- **CUDA:** 版本 11.0+
- **驱动:** 最新的 NVIDIA 驱动程序

---

## 📦 软件环境准备

### 1. 安装 CUDA Toolkit

```bash
# Windows
# 下载并安�?CUDA Toolkit 11.8 �?12.x
# https://developer.nvidia.com/cuda-downloads

# 验证安装
nvcc --version
nvidia-smi
```

### 2. 安装 PyTorch (GPU 版本)

```bash
# CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 验证 GPU 可用
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

### 3. 安装其他依赖

```bash
# sentence-transformers (GPU 版本)
pip install sentence-transformers

# CuPy (可选，用于矩阵运算加�?
pip install cupy-cuda11x  # �?cupy-cuda12x

# 其他工具
pip install nvidia-ml-py3  # GPU 监控
```

### 4. 创建 GPU 环境配置文件

```bash
# requirements-gpu.txt
torch>=2.0.0
torchvision>=0.15.0
sentence-transformers>=2.2.0
cupy-cuda11x>=12.0.0
nvidia-ml-py3>=11.0.0
transformers>=4.30.0
accelerate>=0.20.0
```

---

## 💻 代码实现

### 1. GPU 加速的 CBD 检测器

创建 `examples/cbd_detector_gpu.py`�?
```python
"""
CBD GPU 加速检测器

使用 PyTorch + CUDA 实现高性能污染检�?"""

import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import time
from dataclasses import dataclass


@dataclass
class GPUConfig:
    """GPU 配置"""
    device: str = "cuda"  # "cuda" �?"cpu"
    batch_size: int = 512  # GPU 批处理大小（根据 VRAM 调整�?    use_fp16: bool = True  # 使用半精度加�?    num_workers: int = 4   # 数据加载线程�?

class CBDDetectorGPU:
    """GPU 加速的 CBD 检测器"""
    
    def __init__(self, config: GPUConfig = None):
        """
        初始�?GPU 检测器
        
        Args:
            config: GPU 配置
        """
        self.config = config or GPUConfig()
        
        # 检�?GPU 可用�?        if self.config.device == "cuda" and not torch.cuda.is_available():
            print("⚠️  CUDA 不可用，回退�?CPU")
            self.config.device = "cpu"
        
        # 加载模型�?GPU
        print(f"加载模型到设�? {self.config.device}")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.model = self.model.to(self.config.device)
        
        # 启用半精度加�?        if self.config.use_fp16 and self.config.device == "cuda":
            self.model = self.model.half()
            print("�?启用 FP16 半精度加�?)
        
        # 打印 GPU 信息
        if self.config.device == "cuda":
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"�?GPU: {gpu_name} ({gpu_memory:.1f} GB)")
    
    def compute_embeddings_batch(
        self, 
        texts: List[str],
        show_progress: bool = True
    ) -> torch.Tensor:
        """
        批量计算文本嵌入向量（GPU 加速）
        
        Args:
            texts: 文本列表
            show_progress: 是否显示进度
            
        Returns:
            嵌入向量张量 (n_texts, embedding_dim)
        """
        embeddings = []
        batch_size = self.config.batch_size
        n_batches = (len(texts) + batch_size - 1) // batch_size
        
        with torch.no_grad():
            for i in range(n_batches):
                batch_start = i * batch_size
                batch_end = min((i + 1) * batch_size, len(texts))
                batch_texts = texts[batch_start:batch_end]
                
                # 计算嵌入
                batch_embeddings = self.model.encode(
                    batch_texts,
                    convert_to_tensor=True,
                    device=self.config.device,
                    show_progress_bar=False
                )
                
                embeddings.append(batch_embeddings)
                
                if show_progress and (i + 1) % 10 == 0:
                    print(f"  进度: {i + 1}/{n_batches} 批次", end='\r')
        
        # 合并所有批�?        return torch.cat(embeddings, dim=0)
    
    def compute_similarity_matrix_gpu(
        self,
        train_embeddings: torch.Tensor,
        eval_embeddings: torch.Tensor
    ) -> torch.Tensor:
        """
        �?GPU 上计算相似度矩阵
        
        Args:
            train_embeddings: 训练集嵌�?(n_train, dim)
            eval_embeddings: 评估集嵌�?(n_eval, dim)
            
        Returns:
            相似度矩�?(n_eval, n_train)
        """
        # 余弦相似�?= 归一化后的点�?        train_norm = train_embeddings / train_embeddings.norm(dim=1, keepdim=True)
        eval_norm = eval_embeddings / eval_embeddings.norm(dim=1, keepdim=True)
        
        # 矩阵乘法�?GPU 上非常快
        similarity_matrix = torch.mm(eval_norm, train_norm.T)
        
        return similarity_matrix
    
    def detect_contamination(
        self,
        train_texts: List[str],
        eval_texts: List[str],
        threshold: float = 0.75
    ) -> Dict:
        """
        检测数据污染（GPU 加速完整流程）
        
        Args:
            train_texts: 训练集文本列�?            eval_texts: 评估集文本列�?            threshold: 污染阈�?            
        Returns:
            检测结果字�?        """
        start_time = time.time()
        
        print(f"\n{'='*60}")
        print(f"CBD GPU 加速检�?)
        print(f"{'='*60}")
        print(f"训练集样�? {len(train_texts):,}")
        print(f"评估集样�? {len(eval_texts):,}")
        print(f"设备: {self.config.device}")
        print(f"批处理大�? {self.config.batch_size}")
        
        # 1. 计算训练集嵌�?        print("\n[1/4] 计算训练集嵌�?..")
        t1 = time.time()
        train_embeddings = self.compute_embeddings_batch(train_texts)
        print(f"�?完成 ({time.time() - t1:.2f}s)")
        
        # 2. 计算评估集嵌�?        print("\n[2/4] 计算评估集嵌�?..")
        t2 = time.time()
        eval_embeddings = self.compute_embeddings_batch(eval_texts)
        print(f"�?完成 ({time.time() - t2:.2f}s)")
        
        # 3. 计算相似度矩�?        print("\n[3/4] 计算相似度矩�?..")
        t3 = time.time()
        similarity_matrix = self.compute_similarity_matrix_gpu(
            train_embeddings, 
            eval_embeddings
        )
        print(f"�?完成 ({time.time() - t3:.2f}s)")
        
        # 4. 分析污染
        print("\n[4/4] 分析污染情况...")
        t4 = time.time()
        
        # 计算每个评估样本的最大相似度（C_score�?        c_scores = similarity_matrix.max(dim=1).values
        
        # 转换�?CPU 用于后续分析
        c_scores_cpu = c_scores.cpu().numpy()
        
        # 统计
        contaminated = (c_scores_cpu >= threshold).sum()
        contamination_rate = contaminated / len(eval_texts)
        
        print(f"�?完成 ({time.time() - t4:.2f}s)")
        
        total_time = time.time() - start_time
        throughput = (len(train_texts) + len(eval_texts)) / total_time
        
        results = {
            'c_scores': c_scores_cpu,
            'contaminated_count': int(contaminated),
            'contamination_rate': float(contamination_rate),
            'total_time': total_time,
            'throughput': throughput,
            'embedding_time': time.time() - t1 - (time.time() - t4),
            'similarity_time': time.time() - t3,
            'device': self.config.device
        }
        
        # 打印总结
        print(f"\n{'='*60}")
        print(f"检测完�?)
        print(f"{'='*60}")
        print(f"总时�? {total_time:.3f} �?)
        print(f"吞吐�? {throughput:.1f} 样本/�?)
        print(f"污染样本: {contaminated:,} ({contamination_rate*100:.1f}%)")
        print(f"{'='*60}\n")
        
        return results
    
    def benchmark_performance(self, sample_sizes: List[int] = None):
        """
        性能基准测试
        
        Args:
            sample_sizes: 要测试的样本规模列表
        """
        if sample_sizes is None:
            sample_sizes = [100, 1000, 10000, 50000]
        
        print(f"\n{'='*70}")
        print(f"GPU 性能基准测试")
        print(f"{'='*70}\n")
        
        results = []
        
        for size in sample_sizes:
            print(f"测试规模: {size:,} 样本...")
            
            # 生成测试数据
            train_texts = [f"Training sample {i}" for i in range(size)]
            eval_texts = [f"Evaluation sample {i}" for i in range(size // 10)]
            
            # 运行检�?            result = self.detect_contamination(
                train_texts, 
                eval_texts, 
                threshold=0.75
            )
            
            results.append({
                'size': size,
                'time': result['total_time'],
                'throughput': result['throughput']
            })
        
        # 打印对比表格
        print(f"\n{'='*70}")
        print(f"性能对比")
        print(f"{'='*70}\n")
        print(f"{'样本�?:>10} | {'时间 (�?':>12} | {'吞吐�?(样本/�?':>20}")
        print(f"{'-'*10}-+-{'-'*12}-+-{'-'*20}")
        for r in results:
            print(f"{r['size']:>10,} | {r['time']:>12.3f} | {r['throughput']:>20,.0f}")
        print(f"{'='*70}\n")
        
        return results


def main():
    """演示 GPU 加速检�?""
    
    # 配置
    config = GPUConfig(
        device="cuda" if torch.cuda.is_available() else "cpu",
        batch_size=512,
        use_fp16=True
    )
    
    # 初始化检测器
    detector = CBDDetectorGPU(config)
    
    # 运行基准测试
    detector.benchmark_performance([100, 1000, 10000, 50000])


if __name__ == "__main__":
    main()
```

---

## 📊 性能对比

### CPU vs GPU 预期性能

| 数据规模 | CPU 时间 | GPU 时间 (RTX 3070) | 加速比 |
|----------|----------|---------------------|--------|
| 1k 样本 | 0.03 �?| 0.01 �?| 3x |
| 10k 样本 | 0.33 �?| 0.02 �?| 16x |
| 100k 样本 | 3.3 �?| 0.15 �?| 22x |
| 1M 样本 | 33 �?| 1.2 �?| 27x |

### 不同 GPU 的性能对比

| GPU 型号 | VRAM | 10k 样本 | 100k 样本 | 吞吐�?|
|----------|------|----------|-----------|--------|
| GTX 1660 Ti | 6 GB | 0.04 �?| 0.35 �?| ~300k/�?|
| RTX 3060 | 12 GB | 0.025 �?| 0.20 �?| ~500k/�?|
| RTX 3070 | 8 GB | 0.02 �?| 0.15 �?| ~650k/�?|
| RTX 4090 | 24 GB | 0.01 �?| 0.08 �?| ~1.2M/�?|
| A100 | 40 GB | 0.008 �?| 0.05 �?| ~2M/�?|

---

## 🚀 部署步骤

### 步骤 1：验�?GPU 环境

```bash
# 检�?GPU
nvidia-smi

# 测试 PyTorch GPU
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0)}')"

# 测试 sentence-transformers
python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2'); print('Model loaded successfully')"
```

### 步骤 2：运�?GPU 检测器

```bash
# 创建 GPU 检测脚�?cd c:\Users\14593\CascadeProjects\circular-bias-detection
python examples/cbd_detector_gpu.py
```

### 步骤 3：集成到现有代码

修改 `examples/performance_benchmark.py`，添�?GPU 选项�?
```python
from cbd_detector_gpu import CBDDetectorGPU, GPUConfig

# �?CBDPerformanceBenchmark 类中添加
def run_gpu_detection(self, use_gpu: bool = True):
    if use_gpu and torch.cuda.is_available():
        config = GPUConfig(device="cuda", batch_size=512)
        detector = CBDDetectorGPU(config)
        # ... 使用 GPU 检测器
    else:
        # 使用原有 CPU 检测器
        pass
```

### 步骤 4：性能基准测试（GPU�?
```bash
python examples/cbd_detector_gpu.py
```

---

## 🔧 优化技�?
### 1. 批处理大小优�?
```python
# 根据 GPU VRAM 调整批处理大�?VRAM_TO_BATCH_SIZE = {
    4: 128,    # 4 GB
    6: 256,    # 6 GB
    8: 512,    # 8 GB
    12: 1024,  # 12 GB
    16: 2048,  # 16 GB
    24: 4096,  # 24 GB
}

# 自动检测并设置
gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
batch_size = VRAM_TO_BATCH_SIZE.get(int(gpu_memory), 512)
```

### 2. 混合精度训练

```python
# 使用 FP16 可以获得 2-3x 加�?model = model.half()  # 转换�?FP16

# 或使�?PyTorch �?autocast
with torch.cuda.amp.autocast():
    embeddings = model.encode(texts)
```

### 3. �?GPU 并行

```python
# 使用 DataParallel
if torch.cuda.device_count() > 1:
    model = torch.nn.DataParallel(model)
    print(f"使用 {torch.cuda.device_count()} �?GPU")
```

### 4. GPU 内存管理

```python
# 定期清理 GPU 缓存
torch.cuda.empty_cache()

# 监控 GPU 内存使用
print(f"GPU 内存已用: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
print(f"GPU 内存缓存: {torch.cuda.memory_reserved() / 1e9:.2f} GB")
```

---

## 📈 成本效益分析

### GPU 云服务成本（按需�?
| 提供�?| GPU 型号 | 价格 | 10M 样本成本 |
|--------|----------|------|--------------|
| AWS | T4 | $0.526/小时 | ~$0.05 |
| AWS | A100 | $4.10/小时 | ~$0.02 |
| Google Cloud | V100 | $2.48/小时 | ~$0.03 |
| Azure | V100 | $3.06/小时 | ~$0.04 |

### ROI 分析

**场景�?* 每天检�?1M 样本

| 方案 | 硬件成本 | 处理时间 | 月成�?| 年成�?|
|------|----------|----------|--------|--------|
| CPU | $0 | 9.2 小时/�?| $0 | $0 |
| GPU (云端) | $0 | 0.4 小时/�?| ~$36 | ~$432 |
| GPU (本地 RTX 3070) | $500 一次�?| 0.5 小时/�?| ~$15 电费 | ~$680 (含硬件摊销) |

**结论�?*
- 少于 100k 样本/�?�?CPU 足够
- 100k - 1M 样本/�?�?云端 GPU 性价比高
- > 1M 样本/�?�?本地 GPU 更经�?
---

## ⚠️ 注意事项

### 常见问题

1. **CUDA Out of Memory**
   ```python
   # 减小批处理大�?   config.batch_size = 256  # �?512 减小
   
   # 或启用梯度检查点
   torch.cuda.empty_cache()
   ```

2. **驱动版本不匹�?*
   ```bash
   # 更新 NVIDIA 驱动
   # 确保 CUDA 版本�?PyTorch 版本兼容
   ```

3. **性能未达预期**
   ```python
   # 检查是否使用了 GPU
   print(next(model.parameters()).device)
   
   # 确保数据�?GPU �?   assert embeddings.is_cuda
   ```

---

## 📚 参考资�?
### 文档

- [PyTorch CUDA 文档](https://pytorch.org/docs/stable/cuda.html)
- [Sentence-Transformers GPU 优化](https://www.sbert.net/docs/usage/computing_sentence_embeddings.html)
- [NVIDIA CUDA 工具包](https://developer.nvidia.com/cuda-toolkit)

### 工具

- `nvidia-smi` - GPU 监控
- `nvtop` - GPU 实时监控
- `torch.profiler` - 性能分析

---

## 🎯 实施时间�?
| 阶段 | 任务 | 时间 |
|------|------|------|
| **�?1 �?* | 环境准备、安�?CUDA �?PyTorch | 2-4 小时 |
| **�?2 �?* | 实现 GPU 检测器代码 | 4-6 小时 |
| **�?3 �?* | 性能测试和优�?| 2-4 小时 |
| **�?4 �?* | 集成到现有系�?| 2-3 小时 |
| **�?5 �?* | 生产环境部署和验�?| 2-3 小时 |

**总计�?* 3-5 天（兼职工作�?
---

## �?检查清�?
### GPU 环境准备

- [ ] 安装 NVIDIA 驱动程序
- [ ] 安装 CUDA Toolkit
- [ ] 安装 PyTorch (GPU 版本)
- [ ] 验证 GPU 可用�?- [ ] 运行基准测试

### 代码实现

- [ ] 创建 GPU 检测器�?- [ ] 实现批量嵌入计算
- [ ] 实现 GPU 相似度矩阵计�?- [ ] 添加性能监控
- [ ] 编写单元测试

### 优化和部�?
- [ ] 调优批处理大�?- [ ] 启用混合精度
- [ ] 实现错误处理
- [ ] 编写部署文档
- [ ] 生产环境测试

---

**文档版本�?* v1.0  
**最后更新：** 2024-10-27  
**作者：** Hongping Zhang
