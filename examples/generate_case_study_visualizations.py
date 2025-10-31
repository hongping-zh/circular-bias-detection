"""
案例研究可视化生成器 - "污染危机" (Contamination Crisis)

本脚本生成案例研究中使用的所有图表和可视化，包括：
1. 偏差分数分布图 (The Risk Map)
2. 性能修正对比图 (The Reality Check)
3. 泄露类型分布饼图
4. 样本级别热力图

作者: Hongping Zhang
日期: 2024-10-27
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import os

# 设置中文字体支持（如果需要）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 设置绘图风格
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300


class CaseStudyVisualizer:
    """案例研究可视化生成器"""
    
    def __init__(self, output_dir: str = "./case_study_figures"):
        """
        初始化可视化器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        print(f"✓ 输出目录: {output_dir}")
    
    def generate_contamination_risk_map(
        self,
        c_scores: np.ndarray,
        save_path: str = "contamination_risk_map.png"
    ):
        """
        生成偏差分数分布图 (The Risk Map)
        
        Args:
            c_scores: Circular Score 数组
            save_path: 保存路径
        """
        print("\n生成图表 1: 偏差分数分布图...")
        
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # 绘制直方图
        n, bins, patches = ax.hist(
            c_scores, 
            bins=50, 
            alpha=0.8, 
            color='steelblue', 
            edgecolor='black',
            linewidth=0.5
        )
        
        # 添加风险区域背景色
        ax.axvspan(0.00, 0.30, alpha=0.15, color='green', label='🟢 Low Risk (< 0.30)')
        ax.axvspan(0.30, 0.50, alpha=0.15, color='orange', label='🟠 Medium Risk (0.30-0.50)')
        ax.axvspan(0.50, 0.75, alpha=0.15, color='gold', label='🟡 High Risk (0.50-0.75)')
        ax.axvspan(0.75, 1.00, alpha=0.25, color='red', label='🔴 CRITICAL (≥ 0.75)')
        
        # 添加阈值线
        ax.axvline(x=0.30, color='orange', linestyle='--', linewidth=2, alpha=0.7)
        ax.axvline(x=0.50, color='gold', linestyle='--', linewidth=2, alpha=0.7)
        ax.axvline(x=0.75, color='red', linestyle='--', linewidth=2.5, alpha=0.8)
        
        # 设置坐标轴
        ax.set_xlabel('Circular Score ($C_{score}$)', fontsize=16, fontweight='bold')
        ax.set_ylabel('Number of Samples', fontsize=16, fontweight='bold')
        ax.set_title(
            'Contamination Risk Distribution\nOpenDomainQA-2024 Evaluation Dataset',
            fontsize=18, 
            fontweight='bold',
            pad=20
        )
        
        # 添加统计信息文本框
        stats_text = (
            f"Total Samples: {len(c_scores):,}\n"
            f"Critical (≥0.75): {np.sum(c_scores >= 0.75):,} ({np.sum(c_scores >= 0.75)/len(c_scores)*100:.1f}%)\n"
            f"High (≥0.50): {np.sum(c_scores >= 0.50):,} ({np.sum(c_scores >= 0.50)/len(c_scores)*100:.1f}%)\n"
            f"Medium (≥0.30): {np.sum(c_scores >= 0.30):,} ({np.sum(c_scores >= 0.30)/len(c_scores)*100:.1f}%)\n"
            f"Mean: {np.mean(c_scores):.3f} | Median: {np.median(c_scores):.3f}"
        )
        ax.text(
            0.97, 0.97, stats_text,
            transform=ax.transAxes,
            fontsize=11,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray', linewidth=1.5)
        )
        
        # 图例
        ax.legend(loc='upper left', fontsize=11, frameon=True, shadow=True)
        
        # 网格
        ax.grid(axis='y', alpha=0.3, linestyle=':', linewidth=0.8)
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        full_path = os.path.join(self.output_dir, save_path)
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ 已保存: {full_path}")
    
    def generate_performance_reality_check(
        self,
        original_acc: float = 95.1,
        corrected_acc: float = 58.3,
        save_path: str = "performance_reality_check.png"
    ):
        """
        生成性能修正对比图 (The Reality Check)
        
        Args:
            original_acc: 原始准确率 (%)
            corrected_acc: 修正后准确率 (%)
            save_path: 保存路径
        """
        print("\n生成图表 2: 性能修正对比图...")
        
        fig, ax = plt.subplots(figsize=(11, 8))
        
        categories = ['Original\n(All Samples)\nn=10,000', 'Corrected\n(Clean Samples)\nn=6,000']
        accuracies = [original_acc, corrected_acc]
        colors = ['#3498DB', '#E74C3C']  # 蓝色和红色
        
        # 绘制柱状图
        bars = ax.bar(
            categories, 
            accuracies, 
            color=colors, 
            width=0.55,
            edgecolor='black', 
            linewidth=2.5,
            alpha=0.85
        )
        
        # 添加数值标签
        for bar, acc in zip(bars, accuracies):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2., 
                height + 1.5,
                f'{acc:.1f}%',
                ha='center', 
                va='bottom',
                fontsize=22, 
                fontweight='bold',
                color=bar.get_facecolor()
            )
        
        # 添加下降箭头
        arrow_start_x = 0
        arrow_end_x = 1
        arrow_start_y = original_acc - 2
        arrow_end_y = corrected_acc + 2
        
        ax.annotate(
            '',
            xy=(arrow_end_x, arrow_end_y),
            xytext=(arrow_start_x, arrow_start_y),
            arrowprops=dict(
                arrowstyle='->', 
                lw=4, 
                color='darkred',
                shrinkA=0,
                shrinkB=0
            )
        )
        
        # 下降幅度标注
        drop_percent = original_acc - corrected_acc
        ax.text(
            0.5, (original_acc + corrected_acc) / 2,
            f'-{drop_percent:.1f}%\n↓',
            ha='center',
            va='center',
            fontsize=20,
            fontweight='bold',
            color='darkred',
            bbox=dict(
                boxstyle='round,pad=0.5',
                facecolor='white',
                edgecolor='darkred',
                linewidth=3
            )
        )
        
        # 设置坐标轴
        ax.set_ylabel('Accuracy (%)', fontsize=18, fontweight='bold')
        ax.set_title(
            'The Contamination Crisis:\nPerformance Before and After CBD Correction',
            fontsize=20,
            fontweight='bold',
            pad=25
        )
        ax.set_ylim(0, 110)
        ax.set_xlim(-0.7, 1.7)
        
        # 添加参考线
        ax.axhline(y=50, color='gray', linestyle=':', linewidth=1.5, alpha=0.5, label='50% Baseline')
        ax.axhline(y=75, color='gray', linestyle=':', linewidth=1.5, alpha=0.5, label='75% Target')
        
        # 网格
        ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
        ax.set_axisbelow(True)
        
        # 添加说明文本
        impact_text = (
            "Impact: 36.8% performance drop\n"
            "when contaminated samples removed\n\n"
            "CBD reveals the true model capability"
        )
        ax.text(
            0.98, 0.05, impact_text,
            transform=ax.transAxes,
            fontsize=11,
            verticalalignment='bottom',
            horizontalalignment='right',
            style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='orange', linewidth=2)
        )
        
        plt.tight_layout()
        full_path = os.path.join(self.output_dir, save_path)
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ 已保存: {full_path}")
    
    def generate_leakage_type_distribution(
        self,
        leakage_types: Dict[str, int],
        save_path: str = "leakage_type_distribution.png"
    ):
        """
        生成泄露类型分布饼图
        
        Args:
            leakage_types: 泄露类型字典 {类型: 数量}
            save_path: 保存路径
        """
        print("\n生成图表 3: 泄露类型分布图...")
        
        fig, ax = plt.subplots(figsize=(11, 8))
        
        labels = list(leakage_types.keys())
        sizes = list(leakage_types.values())
        colors = ['#FF6B6B', '#4ECDC4', '#FFD93D', '#95E1D3']
        explode = (0.05, 0.05, 0.05, 0.05)
        
        # 绘制饼图
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            explode=explode,
            shadow=True,
            textprops={'fontsize': 13, 'fontweight': 'bold'}
        )
        
        # 美化百分比文本
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(14)
            autotext.set_fontweight('bold')
        
        ax.set_title(
            'Distribution of Leakage Types\n(Among Contaminated Samples)',
            fontsize=18,
            fontweight='bold',
            pad=20
        )
        
        # 添加图例
        legend_labels = [
            f"{label}: {size:,} samples" 
            for label, size in zip(labels, sizes)
        ]
        ax.legend(
            legend_labels,
            loc='center left',
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=11,
            frameon=True,
            shadow=True
        )
        
        plt.tight_layout()
        full_path = os.path.join(self.output_dir, save_path)
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ 已保存: {full_path}")
    
    def generate_sample_heatmap(
        self,
        c_scores_matrix: np.ndarray,
        sample_ids: List[int],
        train_ids: List[int],
        save_path: str = "sample_contamination_heatmap.png"
    ):
        """
        生成样本级别污染热力图
        
        Args:
            c_scores_matrix: C_score 矩阵 (eval_samples x train_samples)
            sample_ids: 评估样本ID列表
            train_ids: 训练样本ID列表
            save_path: 保存路径
        """
        print("\n生成图表 4: 样本污染热力图...")
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # 绘制热力图
        im = ax.imshow(
            c_scores_matrix,
            cmap='YlOrRd',
            aspect='auto',
            interpolation='nearest',
            vmin=0,
            vmax=1
        )
        
        # 添加颜色条
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Circular Score ($C_{score}$)', fontsize=14, fontweight='bold')
        
        # 设置坐标轴标签
        ax.set_xlabel('Training Sample Index', fontsize=14, fontweight='bold')
        ax.set_ylabel('Evaluation Sample Index', fontsize=14, fontweight='bold')
        ax.set_title(
            'Sample-Level Contamination Heatmap\n(Top 50 Eval Samples × Top 50 Train Samples)',
            fontsize=16,
            fontweight='bold',
            pad=20
        )
        
        # 简化刻度（只显示部分）
        if len(sample_ids) > 10:
            step = len(sample_ids) // 10
            ax.set_yticks(range(0, len(sample_ids), step))
            ax.set_yticklabels([sample_ids[i] for i in range(0, len(sample_ids), step)])
        
        if len(train_ids) > 10:
            step = len(train_ids) // 10
            ax.set_xticks(range(0, len(train_ids), step))
            ax.set_xticklabels([train_ids[i] for i in range(0, len(train_ids), step)])
        
        plt.tight_layout()
        full_path = os.path.join(self.output_dir, save_path)
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ 已保存: {full_path}")


def generate_synthetic_data(n_samples: int = 10000, seed: int = 42) -> pd.DataFrame:
    """
    生成模拟的案例研究数据
    
    Args:
        n_samples: 样本数量
        seed: 随机种子
        
    Returns:
        包含 C_score 的 DataFrame
    """
    np.random.seed(seed)
    
    # 模拟不同风险等级的样本
    n_low = int(n_samples * 0.60)  # 60% 低风险
    n_medium = int(n_samples * 0.25)  # 25% 中等风险
    n_high = int(n_samples * 0.12)  # 12% 高风险
    n_critical = n_samples - n_low - n_medium - n_high  # 3% 关键风险
    
    # 为每个风险等级生成 C_score
    c_scores_low = np.random.beta(2, 8, n_low) * 0.30  # 集中在 0-0.30
    c_scores_medium = np.random.beta(3, 3, n_medium) * 0.20 + 0.30  # 集中在 0.30-0.50
    c_scores_high = np.random.beta(3, 2, n_high) * 0.25 + 0.50  # 集中在 0.50-0.75
    c_scores_critical = np.random.beta(2, 1, n_critical) * 0.25 + 0.75  # 集中在 0.75-1.0
    
    # 合并所有分数
    all_c_scores = np.concatenate([
        c_scores_low,
        c_scores_medium,
        c_scores_high,
        c_scores_critical
    ])
    
    # 随机打乱
    np.random.shuffle(all_c_scores)
    
    # 创建 DataFrame
    df = pd.DataFrame({
        'sample_id': range(n_samples),
        'c_score': all_c_scores,
        'risk_level': ['🟢 Low' if s < 0.30 else 
                       '🟠 Medium' if s < 0.50 else 
                       '🟡 High' if s < 0.75 else 
                       '🔴 Critical' for s in all_c_scores]
    })
    
    return df


def main():
    """主函数：生成所有案例研究可视化"""
    
    print("=" * 70)
    print("案例研究可视化生成器 - 污染危机")
    print("=" * 70)
    
    # 初始化可视化器
    visualizer = CaseStudyVisualizer(output_dir="./case_study_figures")
    
    # 生成模拟数据
    print("\n步骤 1: 生成模拟数据...")
    df_contamination = generate_synthetic_data(n_samples=10000, seed=42)
    print(f"✓ 生成了 {len(df_contamination)} 个样本")
    print(f"\n风险分布:")
    print(df_contamination['risk_level'].value_counts().sort_index())
    
    # 保存数据
    data_path = os.path.join(visualizer.output_dir, "contamination_data.csv")
    df_contamination.to_csv(data_path, index=False)
    print(f"✓ 数据已保存到: {data_path}")
    
    # 图表 1: 偏差分数分布图
    print("\n" + "=" * 70)
    visualizer.generate_contamination_risk_map(
        c_scores=df_contamination['c_score'].values,
        save_path="contamination_risk_map.png"
    )
    
    # 图表 2: 性能修正对比图
    print("\n" + "=" * 70)
    visualizer.generate_performance_reality_check(
        original_acc=95.1,
        corrected_acc=58.3,
        save_path="performance_reality_check.png"
    )
    
    # 图表 3: 泄露类型分布
    print("\n" + "=" * 70)
    leakage_types = {
        'Exact Match': 120,
        'Paraphrase': 850,
        'Partial Overlap': 1530,
        'Semantic Similar': 1500
    }
    visualizer.generate_leakage_type_distribution(
        leakage_types=leakage_types,
        save_path="leakage_type_distribution.png"
    )
    
    # 图表 4: 样本热力图
    print("\n" + "=" * 70)
    # 生成模拟的 C_score 矩阵（50 x 50）
    n_eval = 50
    n_train = 50
    c_scores_matrix = np.random.beta(2, 5, (n_eval, n_train))
    # 添加一些高风险样本
    c_scores_matrix[5:10, 10:15] = np.random.uniform(0.7, 0.9, (5, 5))
    c_scores_matrix[20:25, 30:35] = np.random.uniform(0.75, 0.95, (5, 5))
    
    visualizer.generate_sample_heatmap(
        c_scores_matrix=c_scores_matrix,
        sample_ids=list(range(n_eval)),
        train_ids=list(range(n_train)),
        save_path="sample_contamination_heatmap.png"
    )
    
    # 生成总结报告
    print("\n" + "=" * 70)
    print("可视化生成完成!")
    print("=" * 70)
    print(f"\n生成的文件:")
    print(f"  1. contamination_risk_map.png - 偏差分数分布图")
    print(f"  2. performance_reality_check.png - 性能修正对比图")
    print(f"  3. leakage_type_distribution.png - 泄露类型分布图")
    print(f"  4. sample_contamination_heatmap.png - 样本污染热力图")
    print(f"  5. contamination_data.csv - 模拟数据")
    print(f"\n所有文件已保存到: {visualizer.output_dir}")
    print("\n✅ 完成！")


if __name__ == "__main__":
    main()
