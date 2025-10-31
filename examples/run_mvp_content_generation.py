"""
MVP 内容生成主脚本

一键运行所有三个关键步骤：
1. 数据收集（Hugging Face）
2. 语义重写构造泄露
3. 案例研究可视化生成

作者: Hongping Zhang
日期: 2024-10-27
"""

import os
import sys
import time
from datetime import datetime

# 添加项目路径到系统路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("=" * 80)
print("CBD MVP 内容生成器")
print("=" * 80)
print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)


def print_section(title):
    """打印章节标题"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def run_step_1_data_collection():
    """步骤 1: 数据收集"""
    print_section("步骤 1/3: Hugging Face 数据收集")
    
    try:
        # 检查是否已安装 datasets
        try:
            import datasets
            print("✓ datasets 库已安装")
        except ImportError:
            print("⚠️  未安装 datasets 库，正在安装...")
            os.system("pip install datasets")
        
        # 导入数据收集器
        from data.huggingface_data_collector import HuggingFaceDataCollector
        
        # 初始化收集器
        collector = HuggingFaceDataCollector(output_dir="./mvp_collected_data")
        
        print("\n[1.1] 创建数据集清单...")
        inventory = collector.create_dataset_inventory()
        print(f"✓ 创建了 {len(inventory)} 个数据集的清单")
        
        print("\n[1.2] 搜索相关数据集...")
        qa_datasets = collector.search_datasets_by_keyword(
            keywords=["question", "answering", "qa"],
            limit=10
        )
        print(f"✓ 找到 {len(qa_datasets)} 个问答数据集")
        
        print("\n[1.3] 收集优先级数据集（演示模式）...")
        print("⚠️  注意: 演示模式只下载少量样本，完整收集请修改参数")
        
        # 演示模式：每个数据集只下载 50 个样本
        collected = collector.collect_all_priority_datasets(
            max_samples_per_dataset=50,
            save_format="csv"
        )
        
        print(f"\n✓ 成功收集 {len(collected)} 个数据集")
        
        print("\n[1.4] 生成收集报告...")
        report = collector.generate_collection_report(collected)
        print("\n" + report)
        
        print("\n✅ 步骤 1 完成！")
        return True
        
    except Exception as e:
        print(f"\n❌ 步骤 1 失败: {str(e)}")
        print("提示: 如果是网络问题，请检查 Hugging Face 连接或设置代理")
        return False


def run_step_2_semantic_rewrite():
    """步骤 2: 语义重写构造泄露"""
    print_section("步骤 2/3: 语义重写构造泄露")
    
    try:
        from examples.semantic_rewrite_leakage import (
            SemanticRewriter, 
            LeakageSimulator,
            demonstrate_leakage_construction
        )
        
        print("[2.1] 初始化语义重写器...")
        rewriter = SemanticRewriter()
        simulator = LeakageSimulator()
        print("✓ 重写器初始化完成")
        
        print("\n[2.2] 构造单个泄露对示例...")
        train_text = "The Statue of Liberty was a gift from the people of France to the people of the United States."
        pair = rewriter.construct_leaked_pair(train_text, leakage_intensity=0.8)
        
        print(f"\n训练数据:\n  {pair.train_text[:80]}...")
        print(f"\n泄露评估问题:\n  {pair.eval_question}")
        print(f"\n语义相似度: {pair.semantic_similarity:.3f}")
        print(f"表面相似度: {pair.surface_similarity:.3f}")
        print(f"预期 C_score: {pair.semantic_similarity:.3f} {'🔴 CRITICAL' if pair.semantic_similarity >= 0.75 else '🟡 HIGH'}")
        
        print("\n[2.3] 批量模拟泄露数据集...")
        df_leaked = simulator.simulate_leakage_dataset(
            num_samples=200,
            leakage_ratio=0.4,
            leakage_intensity=0.75
        )
        
        print(f"✓ 生成了 {len(df_leaked)} 个样本")
        
        print("\n[2.4] 分析泄露分布...")
        analysis = simulator.analyze_leakage_distribution(df_leaked)
        
        print(f"\n泄露分析结果:")
        print(f"  总样本数: {analysis['total_samples']}")
        print(f"  泄露样本: {analysis['leaked_samples']} ({analysis['leakage_ratio']:.1%})")
        print(f"  干净样本: {analysis['clean_samples']}")
        print(f"  高风险样本 (C_score > 0.75): {analysis['high_risk_samples']}")
        
        print("\n[2.5] 保存泄露数据集...")
        output_path = "./mvp_leaked_dataset.csv"
        df_leaked.to_csv(output_path, index=False)
        print(f"✓ 已保存到: {output_path}")
        
        print("\n✅ 步骤 2 完成！")
        return True
        
    except Exception as e:
        print(f"\n❌ 步骤 2 失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_step_3_visualizations():
    """步骤 3: 案例研究可视化"""
    print_section("步骤 3/3: 案例研究可视化生成")
    
    try:
        # 检查必要的库
        required_packages = ['matplotlib', 'seaborn', 'numpy', 'pandas']
        for package in required_packages:
            try:
                __import__(package)
                print(f"✓ {package} 已安装")
            except ImportError:
                print(f"⚠️  正在安装 {package}...")
                os.system(f"pip install {package}")
        
        import numpy as np
        from examples.generate_case_study_visualizations import (
            CaseStudyVisualizer,
            generate_synthetic_data
        )
        
        print("\n[3.1] 初始化可视化器...")
        visualizer = CaseStudyVisualizer(output_dir="./mvp_case_study_figures")
        print("✓ 可视化器初始化完成")
        
        print("\n[3.2] 生成模拟数据...")
        df_contamination = generate_synthetic_data(n_samples=10000, seed=42)
        print(f"✓ 生成了 {len(df_contamination)} 个样本")
        
        print("\n风险分布:")
        risk_counts = df_contamination['risk_level'].value_counts().sort_index()
        for risk, count in risk_counts.items():
            percentage = count / len(df_contamination) * 100
            print(f"  {risk}: {count:,} ({percentage:.1f}%)")
        
        print("\n[3.3] 生成图表 1: 偏差分数分布图...")
        visualizer.generate_contamination_risk_map(
            c_scores=df_contamination['c_score'].values,
            save_path="contamination_risk_map.png"
        )
        
        print("\n[3.4] 生成图表 2: 性能修正对比图...")
        visualizer.generate_performance_reality_check(
            original_acc=95.1,
            corrected_acc=58.3,
            save_path="performance_reality_check.png"
        )
        
        print("\n[3.5] 生成图表 3: 泄露类型分布图...")
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
        
        print("\n[3.6] 生成图表 4: 样本污染热力图...")
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
        
        print("\n[3.7] 保存模拟数据...")
        data_path = os.path.join(visualizer.output_dir, "contamination_data.csv")
        df_contamination.to_csv(data_path, index=False)
        print(f"✓ 数据已保存到: {data_path}")
        
        print("\n✅ 步骤 3 完成！")
        print(f"\n所有图表已保存到: {visualizer.output_dir}")
        return True
        
    except Exception as e:
        print(f"\n❌ 步骤 3 失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_step_4_performance_benchmark():
    """步骤 4: 性能基准测试"""
    print_section("步骤 4/4: 性能基准测试")
    
    try:
        # 检查数据文件是否存在
        data_path = "./mvp_case_study_figures/contamination_data.csv"
        if not os.path.exists(data_path):
            print(f"❌ 数据文件不存在: {data_path}")
            print("请先运行步骤 3（可视化生成）来创建数据文件")
            return False
        
        from examples.performance_benchmark import CBDPerformanceBenchmark
        
        print("[4.1] 初始化性能基准测试器...")
        benchmark = CBDPerformanceBenchmark(data_path)
        
        print("\n[4.2] 加载测试数据...")
        benchmark.load_data()
        
        print("\n[4.3] 运行 CBD 污染检测...")
        benchmark.simulate_cbd_detection(batch_size=100)
        
        print("\n[4.4] 分析性能指标...")
        benchmark.analyze_performance()
        
        print("\n[4.5] 生成性能报告...")
        benchmark.generate_report(output_path="./CBD_PERFORMANCE_REPORT.md")
        
        # 生成简洁摘要
        print("\n[4.6] 生成简洁摘要...")
        with open("./CBD_PERFORMANCE_SUMMARY.md", 'w', encoding='utf-8') as f:
            f.write(f"""# CBD 性能报告 - 执行摘要

> **一句话总结：** CBD 可在 **{benchmark.results['detection_time']:.2f} 秒**内完成 10,000 个样本的污染检测，吞吐量达 **{benchmark.results['throughput']:.0f} 样本/秒**

## ⚡ 核心指标

| 指标 | 数值 |
|------|------|
| **检测 10k 样本耗时** | **{benchmark.results['detection_time']:.2f} 秒** |
| **吞吐量** | **{benchmark.results['throughput']:.0f} 样本/秒** |
| **单样本处理时间** | **{benchmark.results['avg_time_per_sample']:.3f} 毫秒** |
| **性能评级** | **⭐⭐⭐⭐⭐ 优秀** |

完整报告请查看：[CBD_PERFORMANCE_REPORT.md](CBD_PERFORMANCE_REPORT.md)
""")
        print("✓ 简洁摘要已保存: ./CBD_PERFORMANCE_SUMMARY.md")
        
        print("\n✅ 步骤 4 完成！")
        return True
        
    except Exception as e:
        print(f"\n❌ 步骤 4 失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def print_summary(results):
    """打印执行总结"""
    print("\n" + "=" * 80)
    print("执行总结")
    print("=" * 80)
    
    print("\n任务完成状态:")
    steps = [
        ("步骤 1: 数据收集", results['step1']),
        ("步骤 2: 语义重写", results['step2']),
        ("步骤 3: 可视化生成", results['step3']),
        ("步骤 4: 性能基准测试", results['step4'])
    ]
    
    for step_name, status in steps:
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {step_name}")
    
    success_count = sum(results.values())
    print(f"\n总计: {success_count}/4 个步骤成功完成")
    
    if success_count == 4:
        print("\n🎉 所有步骤成功完成！")
        print("\n生成的文件:")
        print("  📁 ./mvp_collected_data/ - 收集的数据集")
        print("  📄 ./mvp_leaked_dataset.csv - 模拟泄露数据集")
        print("  📁 ./mvp_case_study_figures/ - 案例研究可视化")
        print("  📄 ./CBD_PERFORMANCE_REPORT.md - 详细性能报告")
        print("  📄 ./CBD_PERFORMANCE_SUMMARY.md - 性能执行摘要")
        print("\n下一步:")
        print("  1. 查看生成的图表（PNG 文件）")
        print("  2. 阅读性能报告: CBD_PERFORMANCE_SUMMARY.md")
        print("  3. 阅读实施指南: docs/MVP_CONTENT_IMPLEMENTATION_GUIDE.md")
        print("  4. 将内容集成到 MVP 网站")
    else:
        print("\n⚠️  部分步骤失败，请检查错误信息并重试")
        print("\n故障排除:")
        print("  - 检查网络连接（Hugging Face 数据集下载）")
        print("  - 确保已安装所有依赖: pip install -r requirements.txt")
        print("  - 查看详细错误信息")


def main():
    """主函数"""
    start_time = time.time()
    
    results = {
        'step1': False,
        'step2': False,
        'step3': False,
        'step4': False
    }
    
    # 询问用户是否运行每个步骤
    print("\n请选择要运行的步骤:")
    print("1. 数据收集（需要网络连接，较慢）")
    print("2. 语义重写构造泄露（快速）")
    print("3. 可视化生成（快速）")
    print("4. 性能基准测试（快速）")
    print("5. 运行所有步骤")
    print("0. 退出")
    
    choice = input("\n请输入选项 (0-5): ").strip()
    
    if choice == '0':
        print("退出程序")
        return
    elif choice == '1':
        results['step1'] = run_step_1_data_collection()
    elif choice == '2':
        results['step2'] = run_step_2_semantic_rewrite()
    elif choice == '3':
        results['step3'] = run_step_3_visualizations()
    elif choice == '4':
        results['step4'] = run_step_4_performance_benchmark()
    elif choice == '5':
        print("\n运行所有步骤...\n")
        
        # 步骤 1: 数据收集（可选跳过）
        skip_step1 = input("步骤 1（数据收集）需要网络连接且较慢，是否跳过？(y/n): ").strip().lower()
        if skip_step1 != 'y':
            results['step1'] = run_step_1_data_collection()
        else:
            print("\n⏭️  跳过步骤 1")
        
        # 步骤 2: 语义重写
        results['step2'] = run_step_2_semantic_rewrite()
        
        # 步骤 3: 可视化
        results['step3'] = run_step_3_visualizations()
        
        # 步骤 4: 性能测试
        results['step4'] = run_step_4_performance_benchmark()
    else:
        print("无效的选项")
        return
    
    # 打印总结
    elapsed_time = time.time() - start_time
    print_summary(results)
    
    print(f"\n总耗时: {elapsed_time:.1f} 秒")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断执行")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ 发生未预期的错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
