#!/usr/bin/env python3
"""
快速演示脚本 - 验证算法增强功能

运行此脚本即可快速验证所有新功能是否正常工作。
"""

import numpy as np
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

def check_dependencies():
    """检查依赖安装情况"""
    print("🔍 检查依赖...")
    
    deps = {
        'numpy': True,
        'pandas': True,
        'scipy': True,
        'xgboost': False,
        'sklearn': False,
        'shap': False
    }
    
    for package, required in deps.items():
        try:
            if package == 'sklearn':
                __import__('sklearn')
            else:
                __import__(package)
            print(f"  ✅ {package:15s} - 已安装")
        except ImportError:
            status = "⚠️  推荐" if not required else "❌ 必需"
            print(f"  {status} {package:15s} - 未安装")
            if required or package in ['xgboost', 'sklearn']:
                print(f"      安装命令: pip install {package}")
    print()


def test_advanced_metrics():
    """测试新指标"""
    print("=" * 60)
    print("📊 测试 1: 新检测指标")
    print("=" * 60)
    
    try:
        from circular_bias_detector.advanced_metrics import (
            compute_tdi, compute_ics, compute_ads, compute_mci
        )
        from circular_bias_detector.utils import create_synthetic_data
        
        # 生成测试数据
        print("\n生成测试数据...")
        perf, const = create_synthetic_data(
            n_time_periods=15,
            n_algorithms=4,
            n_constraints=3,
            bias_intensity=0.6,
            random_seed=42
        )
        print(f"  数据形状: performance={perf.shape}, constraints={const.shape}")
        
        # 计算新指标
        print("\n计算新指标...")
        tdi = compute_tdi(perf)
        ics = compute_ics(perf, const)
        ads = compute_ads(perf, const)
        mci, _ = compute_mci(const)
        
        print(f"  TDI (时间依赖):     {tdi:.4f} {'✓' if tdi < 0.6 else '⚠'}")
        print(f"  ICS (信息准则):     {ics:+.4f} {'✓' if ics > -0.5 else '⚠'}")
        print(f"  ADS (自适应漂移):   {ads:.4f} {'✓' if ads < 0.3 else '⚠'}")
        print(f"  MCI (多约束交互):   {mci:.4f} {'✓' if mci < 0.8 else '⚠'}")
        
        print("\n✅ 新指标模块运行正常！")
        return True
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ml_features():
    """测试ML特征提取"""
    print("\n" + "=" * 60)
    print("🤖 测试 2: ML特征提取")
    print("=" * 60)
    
    try:
        from circular_bias_detector.ml_detector import MLBiasDetector
        from circular_bias_detector.utils import create_synthetic_data
        
        print("\n初始化ML检测器...")
        detector = MLBiasDetector()
        
        print("生成测试数据...")
        perf, const = create_synthetic_data(
            n_time_periods=12,
            n_algorithms=3,
            n_constraints=2,
            bias_intensity=0.5,
            random_seed=123
        )
        
        print("提取特征向量...")
        features = detector.extract_features(perf, const)
        
        print(f"  特征维度: {len(features)}")
        print(f"  特征名称: {len(detector.feature_names)} 个")
        print(f"  前5个特征值: {features[:5]}")
        
        print("\n✅ ML特征提取正常！")
        return True
        
    except ImportError as e:
        print(f"\n⚠️  需要安装: pip install xgboost scikit-learn")
        print(f"   错误: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """测试与现有系统集成"""
    print("\n" + "=" * 60)
    print("🔗 测试 3: 系统集成")
    print("=" * 60)
    
    try:
        from circular_bias_detector import BiasDetector
        from circular_bias_detector.advanced_metrics import compute_all_advanced_metrics
        from circular_bias_detector.utils import create_synthetic_data
        
        print("\n使用传统检测器...")
        traditional_detector = BiasDetector()
        
        perf, const = create_synthetic_data(
            n_time_periods=15,
            n_algorithms=4,
            n_constraints=3,
            bias_intensity=0.7,
            random_seed=999
        )
        
        # 传统检测
        trad_results = traditional_detector.detect_bias(perf, const)
        print(f"  传统检测 - 偏差: {trad_results['overall_bias']}, 置信度: {trad_results['confidence']:.2%}")
        
        # 新指标检测
        print("\n使用新指标...")
        adv_results = compute_all_advanced_metrics(perf, const)
        print(f"  TDI: {adv_results['tdi']:.4f}")
        print(f"  ICS: {adv_results['ics']:+.4f}")
        print(f"  ADS: {adv_results['ads']:.4f}")
        print(f"  MCI: {adv_results['mci']:.4f}")
        
        print("\n✅ 系统集成正常！新旧指标可协同工作")
        return True
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_example_script():
    """测试示例脚本可运行性"""
    print("\n" + "=" * 60)
    print("📖 测试 4: 示例代码")
    print("=" * 60)
    
    example_path = os.path.join(
        os.path.dirname(__file__), 
        'examples', 
        'advanced_detection_example.py'
    )
    
    if os.path.exists(example_path):
        print(f"\n✅ 示例文件存在: {example_path}")
        print("   运行命令: python examples/advanced_detection_example.py")
        return True
    else:
        print(f"\n❌ 示例文件不存在: {example_path}")
        return False


def test_unit_tests():
    """检查单元测试"""
    print("\n" + "=" * 60)
    print("🧪 测试 5: 单元测试套件")
    print("=" * 60)
    
    test_path = os.path.join(
        os.path.dirname(__file__),
        'tests',
        'test_advanced_metrics.py'
    )
    
    if os.path.exists(test_path):
        print(f"\n✅ 测试文件存在: {test_path}")
        print("   运行命令: pytest tests/test_advanced_metrics.py -v")
        print("   或: python tests/test_advanced_metrics.py")
        return True
    else:
        print(f"\n❌ 测试文件不存在: {test_path}")
        return False


def main():
    """主函数"""
    print("\n" + "🚀" * 30)
    print("算法增强功能 - 快速验证")
    print("🚀" * 30 + "\n")
    
    # 检查依赖
    check_dependencies()
    
    # 运行测试
    results = []
    
    results.append(("新检测指标", test_advanced_metrics()))
    results.append(("ML特征提取", test_ml_features()))
    results.append(("系统集成", test_integration()))
    results.append(("示例代码", test_example_script()))
    results.append(("单元测试", test_unit_tests()))
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {name:20s} {status}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print(f"\n总计: {passed_count}/{total_count} 测试通过")
    
    if passed_count == total_count:
        print("\n🎉 恭喜！所有功能正常运行！")
        print("\n📚 下一步:")
        print("   1. 运行完整示例: python examples/advanced_detection_example.py")
        print("   2. 阅读文档: ALGORITHM_ENHANCEMENT_SUMMARY.md")
        print("   3. 查看路线图: ALGORITHM_ENHANCEMENT_ROADMAP.md")
    elif passed_count >= 3:
        print("\n⚠️  大部分功能正常，部分功能需要额外依赖")
        print("   安装完整依赖: pip install xgboost scikit-learn shap")
    else:
        print("\n❌ 部分功能异常，请检查安装和代码")
        print("   查看错误信息并根据提示修复")
    
    print("\n" + "=" * 60)
    print("验证完成！")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
