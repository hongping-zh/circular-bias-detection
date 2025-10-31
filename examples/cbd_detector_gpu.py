"""
CBD GPU 加速检测器

使用 PyTorch + CUDA 实现高性能污染检测。
支持批处理、混合精度和多 GPU 并行。

作者: Hongping Zhang
日期: 2024-10-27
"""

import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple, Optional
import time
from dataclasses import dataclass
import sys
import os


@dataclass
class GPUConfig:
    """GPU 配置"""
    device: str = "cuda"  # "cuda" 或 "cpu"
    batch_size: int = 512  # GPU 批处理大小（根据 VRAM 调整）
    use_fp16: bool = True  # 使用半精度加速
    num_workers: int = 4   # 数据加载线程数
    model_name: str = "all-MiniLM-L6-v2"  # 嵌入模型


class CBDDetectorGPU:
    """GPU 加速的 CBD 检测器"""
    
    def __init__(self, config: GPUConfig = None):
        """
        初始化 GPU 检测器
        
        Args:
            config: GPU 配置
        """
        self.config = config or GPUConfig()
        
        # 检查 GPU 可用性
        self.has_cuda = torch.cuda.is_available()
        if self.config.device == "cuda" and not self.has_cuda:
            print("⚠️  CUDA 不可用，回退到 CPU")
            self.config.device = "cpu"
        
        # 加载模型到 GPU
        print(f"\n初始化 CBD GPU 检测器...")
        print(f"  - 设备: {self.config.device}")
        print(f"  - 模型: {self.config.model_name}")
        
        self.model = SentenceTransformer(self.config.model_name)
        self.model = self.model.to(self.config.device)
        
        # 启用半精度加速
        if self.config.use_fp16 and self.config.device == "cuda":
            self.model = self.model.half()
            print(f"  - 精度: FP16 (半精度)")
        else:
            print(f"  - 精度: FP32 (全精度)")
        
        # 打印 GPU 信息
        if self.config.device == "cuda":
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"  - GPU: {gpu_name}")
            print(f"  - VRAM: {gpu_memory:.1f} GB")
            print(f"  - 批处理大小: {self.config.batch_size}")
        
        print(f"✓ 初始化完成\n")
    
    def compute_embeddings_batch(
        self, 
        texts: List[str],
        show_progress: bool = True,
        description: str = "计算嵌入"
    ) -> torch.Tensor:
        """
        批量计算文本嵌入向量（GPU 加速）
        
        Args:
            texts: 文本列表
            show_progress: 是否显示进度
            description: 进度描述
            
        Returns:
            嵌入向量张量 (n_texts, embedding_dim)
        """
        if len(texts) == 0:
            return torch.zeros((0, 384), device=self.config.device)
        
        embeddings = []
        batch_size = self.config.batch_size
        n_batches = (len(texts) + batch_size - 1) // batch_size
        
        start_time = time.time()
        
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
                    show_progress_bar=False,
                    batch_size=len(batch_texts)
                )
                
                embeddings.append(batch_embeddings)
                
                if show_progress:
                    progress = (i + 1) / n_batches * 100
                    elapsed = time.time() - start_time
                    samples_done = min(batch_end, len(texts))
                    speed = samples_done / elapsed if elapsed > 0 else 0
                    print(f"  {description}: {progress:5.1f}% ({samples_done:>6,}/{len(texts):>6,}) | "
                          f"{speed:>8,.0f} 样本/秒", end='\r')
        
        if show_progress:
            print()  # 换行
        
        # 合并所有批次
        return torch.cat(embeddings, dim=0)
    
    def compute_similarity_matrix_gpu(
        self,
        train_embeddings: torch.Tensor,
        eval_embeddings: torch.Tensor,
        chunk_size: int = 1000
    ) -> torch.Tensor:
        """
        在 GPU 上计算相似度矩阵（分块处理以节省内存）
        
        Args:
            train_embeddings: 训练集嵌入 (n_train, dim)
            eval_embeddings: 评估集嵌入 (n_eval, dim)
            chunk_size: 分块大小
            
        Returns:
            相似度矩阵 (n_eval, n_train)
        """
        n_eval = eval_embeddings.shape[0]
        n_train = train_embeddings.shape[0]
        
        # 归一化
        train_norm = train_embeddings / train_embeddings.norm(dim=1, keepdim=True)
        eval_norm = eval_embeddings / eval_embeddings.norm(dim=1, keepdim=True)
        
        # 如果数据集较小，直接计算
        if n_eval * n_train < 10_000_000:
            return torch.mm(eval_norm, train_norm.T)
        
        # 否则分块计算
        similarity_chunks = []
        n_chunks = (n_eval + chunk_size - 1) // chunk_size
        
        for i in range(n_chunks):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, n_eval)
            chunk = torch.mm(eval_norm[start:end], train_norm.T)
            similarity_chunks.append(chunk)
            
            if (i + 1) % 10 == 0:
                print(f"  计算相似度: {(i+1)/n_chunks*100:.1f}%", end='\r')
        
        return torch.cat(similarity_chunks, dim=0)
    
    def detect_contamination(
        self,
        train_texts: List[str],
        eval_texts: List[str],
        threshold: float = 0.75,
        return_details: bool = False
    ) -> Dict:
        """
        检测数据污染（GPU 加速完整流程）
        
        Args:
            train_texts: 训练集文本列表
            eval_texts: 评估集文本列表
            threshold: 污染阈值
            return_details: 是否返回详细结果
            
        Returns:
            检测结果字典
        """
        start_time = time.time()
        
        print(f"\n{'='*70}")
        print(f"CBD GPU 加速检测")
        print(f"{'='*70}")
        print(f"训练集样本: {len(train_texts):>10,}")
        print(f"评估集样本: {len(eval_texts):>10,}")
        print(f"污染阈值:   {threshold:>10.2f}")
        print(f"设备:       {self.config.device:>10}")
        if self.config.device == "cuda":
            print(f"批处理:     {self.config.batch_size:>10,}")
        print(f"{'='*70}\n")
        
        # 1. 计算训练集嵌入
        print("[1/4] 计算训练集嵌入...")
        t1 = time.time()
        train_embeddings = self.compute_embeddings_batch(
            train_texts, 
            description="训练集"
        )
        t1_duration = time.time() - t1
        print(f"✓ 完成 ({t1_duration:.2f}s, {len(train_texts)/t1_duration:,.0f} 样本/秒)\n")
        
        # 2. 计算评估集嵌入
        print("[2/4] 计算评估集嵌入...")
        t2 = time.time()
        eval_embeddings = self.compute_embeddings_batch(
            eval_texts,
            description="评估集"
        )
        t2_duration = time.time() - t2
        print(f"✓ 完成 ({t2_duration:.2f}s, {len(eval_texts)/t2_duration:,.0f} 样本/秒)\n")
        
        # 3. 计算相似度矩阵
        print("[3/4] 计算相似度矩阵...")
        t3 = time.time()
        similarity_matrix = self.compute_similarity_matrix_gpu(
            train_embeddings, 
            eval_embeddings
        )
        t3_duration = time.time() - t3
        print(f"✓ 完成 ({t3_duration:.2f}s)\n")
        
        # 4. 分析污染
        print("[4/4] 分析污染情况...")
        t4 = time.time()
        
        # 计算每个评估样本的最大相似度（C_score）
        c_scores_tensor = similarity_matrix.max(dim=1).values
        max_indices = similarity_matrix.max(dim=1).indices
        
        # 转换到 CPU 用于后续分析
        c_scores = c_scores_tensor.cpu().numpy()
        max_idx = max_indices.cpu().numpy()
        
        # 统计不同风险等级
        critical = (c_scores >= 0.75).sum()
        high = ((c_scores >= 0.50) & (c_scores < 0.75)).sum()
        medium = ((c_scores >= 0.30) & (c_scores < 0.50)).sum()
        low = (c_scores < 0.30).sum()
        
        contaminated = (c_scores >= threshold).sum()
        contamination_rate = contaminated / len(eval_texts) if len(eval_texts) > 0 else 0
        
        t4_duration = time.time() - t4
        print(f"✓ 完成 ({t4_duration:.2f}s)\n")
        
        total_time = time.time() - start_time
        throughput = (len(train_texts) + len(eval_texts)) / total_time
        
        # 构建结果
        results = {
            'c_scores': c_scores,
            'contaminated_count': int(contaminated),
            'contamination_rate': float(contamination_rate),
            'risk_distribution': {
                'critical': int(critical),
                'high': int(high),
                'medium': int(medium),
                'low': int(low)
            },
            'timing': {
                'total': total_time,
                'train_embedding': t1_duration,
                'eval_embedding': t2_duration,
                'similarity': t3_duration,
                'analysis': t4_duration
            },
            'throughput': throughput,
            'device': self.config.device,
            'n_train': len(train_texts),
            'n_eval': len(eval_texts)
        }
        
        if return_details:
            results['max_train_indices'] = max_idx
            results['similarity_matrix'] = similarity_matrix.cpu().numpy()
        
        # 打印总结
        self._print_results(results)
        
        return results
    
    def _print_results(self, results: Dict):
        """打印检测结果"""
        print(f"{'='*70}")
        print(f"检测完成")
        print(f"{'='*70}")
        
        print(f"\n⚡ 性能指标:")
        print(f"  总时间:         {results['timing']['total']:>10.3f} 秒")
        print(f"  吞吐量:         {results['throughput']:>10,.0f} 样本/秒")
        print(f"  训练集嵌入:     {results['timing']['train_embedding']:>10.3f} 秒")
        print(f"  评估集嵌入:     {results['timing']['eval_embedding']:>10.3f} 秒")
        print(f"  相似度计算:     {results['timing']['similarity']:>10.3f} 秒")
        
        print(f"\n🔍 检测结果:")
        print(f"  污染样本:       {results['contaminated_count']:>10,} "
              f"({results['contamination_rate']*100:>5.1f}%)")
        
        print(f"\n📊 风险分布:")
        dist = results['risk_distribution']
        total = sum(dist.values())
        print(f"  🔴 关键风险:    {dist['critical']:>10,} ({dist['critical']/total*100:>5.1f}%)")
        print(f"  🟡 高风险:      {dist['high']:>10,} ({dist['high']/total*100:>5.1f}%)")
        print(f"  🟠 中等风险:    {dist['medium']:>10,} ({dist['medium']/total*100:>5.1f}%)")
        print(f"  🟢 低风险:      {dist['low']:>10,} ({dist['low']/total*100:>5.1f}%)")
        
        print(f"\n{'='*70}\n")
    
    def benchmark_performance(
        self, 
        sample_sizes: List[int] = None,
        train_eval_ratio: float = 10.0
    ):
        """
        性能基准测试
        
        Args:
            sample_sizes: 要测试的样本规模列表
            train_eval_ratio: 训练集/评估集比例
        """
        if sample_sizes is None:
            sample_sizes = [100, 1000, 10000, 50000]
        
        print(f"\n{'='*70}")
        print(f"GPU 性能基准测试")
        print(f"{'='*70}")
        print(f"设备: {self.config.device}")
        if self.config.device == "cuda":
            print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"训练/评估比例: {train_eval_ratio}:1")
        print(f"{'='*70}\n")
        
        results = []
        
        for size in sample_sizes:
            eval_size = int(size / train_eval_ratio)
            print(f"{'='*70}")
            print(f"测试规模: 训练集 {size:,} 样本, 评估集 {eval_size:,} 样本")
            print(f"{'='*70}")
            
            # 生成测试数据
            train_texts = [f"Training sample {i}: This is a sample text for testing." for i in range(size)]
            eval_texts = [f"Evaluation sample {i}: This is a test sample." for i in range(eval_size)]
            
            # 运行检测
            result = self.detect_contamination(
                train_texts, 
                eval_texts, 
                threshold=0.75
            )
            
            results.append({
                'train_size': size,
                'eval_size': eval_size,
                'total_size': size + eval_size,
                'time': result['timing']['total'],
                'throughput': result['throughput'],
                'contamination_rate': result['contamination_rate']
            })
        
        # 打印对比表格
        print(f"\n{'='*70}")
        print(f"性能对比总结")
        print(f"{'='*70}\n")
        print(f"{'训练集':>10} | {'评估集':>10} | {'总时间 (秒)':>12} | {'吞吐量 (样本/秒)':>20}")
        print(f"{'-'*10}-+-{'-'*10}-+-{'-'*12}-+-{'-'*20}")
        for r in results:
            print(f"{r['train_size']:>10,} | {r['eval_size']:>10,} | "
                  f"{r['time']:>12.3f} | {r['throughput']:>20,.0f}")
        print(f"{'='*70}\n")
        
        # 计算加速比（相对于第一个测试）
        if len(results) > 1:
            base_throughput = results[0]['throughput']
            print(f"吞吐量扩展性:")
            for r in results:
                scale_factor = r['total_size'] / results[0]['total_size']
                efficiency = (r['throughput'] / base_throughput) / scale_factor * 100
                print(f"  {r['total_size']:>10,} 样本: {efficiency:>6.1f}% 效率")
            print()
        
        return results
    
    def compare_with_cpu(self, sample_size: int = 10000):
        """
        GPU vs CPU 性能对比
        
        Args:
            sample_size: 测试样本规模
        """
        print(f"\n{'='*70}")
        print(f"GPU vs CPU 性能对比")
        print(f"{'='*70}\n")
        
        # 生成测试数据
        eval_size = sample_size // 10
        train_texts = [f"Training sample {i}" for i in range(sample_size)]
        eval_texts = [f"Evaluation sample {i}" for i in range(eval_size)]
        
        results = {}
        
        # GPU 测试
        if torch.cuda.is_available():
            print("运行 GPU 测试...")
            self.config.device = "cuda"
            self.model = self.model.to("cuda")
            result_gpu = self.detect_contamination(train_texts, eval_texts)
            results['gpu'] = result_gpu
        
        # CPU 测试
        print("运行 CPU 测试...")
        self.config.device = "cpu"
        self.model = self.model.to("cpu")
        result_cpu = self.detect_contamination(train_texts, eval_texts)
        results['cpu'] = result_cpu
        
        # 对比
        if 'gpu' in results and 'cpu' in results:
            speedup = results['cpu']['timing']['total'] / results['gpu']['timing']['total']
            throughput_improvement = results['gpu']['throughput'] / results['cpu']['throughput']
            
            print(f"\n{'='*70}")
            print(f"对比总结")
            print(f"{'='*70}\n")
            print(f"{'指标':<20} | {'GPU':>15} | {'CPU':>15} | {'加速比':>10}")
            print(f"{'-'*20}-+-{'-'*15}-+-{'-'*15}-+-{'-'*10}")
            print(f"{'总时间 (秒)':<20} | {results['gpu']['timing']['total']:>15.3f} | "
                  f"{results['cpu']['timing']['total']:>15.3f} | {speedup:>10.1f}x")
            print(f"{'吞吐量 (样本/秒)':<20} | {results['gpu']['throughput']:>15,.0f} | "
                  f"{results['cpu']['throughput']:>15,.0f} | {throughput_improvement:>10.1f}x")
            print(f"{'='*70}\n")
            
            print(f"🚀 GPU 加速比: {speedup:.1f}x")
            print(f"⚡ 吞吐量提升: {throughput_improvement:.1f}x\n")
        
        return results


def main():
    """演示 GPU 加速检测"""
    
    # 检查 CUDA
    if not torch.cuda.is_available():
        print("⚠️  警告: CUDA 不可用，将使用 CPU 模式")
        print("请确保安装了正确的 PyTorch GPU 版本")
        print("安装命令: pip install torch --index-url https://download.pytorch.org/whl/cu118\n")
    
    # 配置
    config = GPUConfig(
        device="cuda" if torch.cuda.is_available() else "cpu",
        batch_size=512,
        use_fp16=True
    )
    
    # 初始化检测器
    detector = CBDDetectorGPU(config)
    
    # 选择测试模式
    print("请选择测试模式:")
    print("1. 性能基准测试（推荐）")
    print("2. GPU vs CPU 对比")
    print("3. 快速测试（1k 样本）")
    
    try:
        choice = input("\n请输入选项 (1-3，默认 1): ").strip() or "1"
        
        if choice == "1":
            # 性能基准测试
            detector.benchmark_performance(
                sample_sizes=[100, 1000, 10000, 50000]
            )
        elif choice == "2":
            # GPU vs CPU 对比
            if torch.cuda.is_available():
                detector.compare_with_cpu(sample_size=10000)
            else:
                print("错误: GPU 不可用，无法进行对比测试")
        elif choice == "3":
            # 快速测试
            detector.benchmark_performance(
                sample_sizes=[1000]
            )
        else:
            print("无效的选项")
    
    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
