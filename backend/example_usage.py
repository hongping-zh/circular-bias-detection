"""
Simple usage examples for Zenodo-Sleuth Integration

这个文件展示了如何使用集成 API 的各种场景。
"""

import requests
import json
import time


BASE_URL = "http://localhost:5000"


def example_1_simple_analysis():
    """
    示例 1: 最简单的使用方式
    
    直接调用 API，使用所有默认参数
    """
    print("\n" + "="*60)
    print("示例 1: 简单分析（使用默认参数）")
    print("="*60)
    
    response = requests.post(
        f"{BASE_URL}/api/analyze_zenodo",
        json={}  # 空 JSON，使用所有默认值
    )
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"\n✅ 分析成功!")
        print(f"📊 数据集: {data['source_data']['title']}")
        print(f"📈 CBS 得分: {data['sleuth_analysis']['cbs_score']:.4f}")
        print(f"🎯 检测到偏差: {data['sleuth_analysis']['bias_detected']}")
        print(f"⏱️  处理时间: {data['processing_info']['elapsed_time_seconds']}秒")
        
        return data
    else:
        print(f"❌ 错误: {response.status_code}")
        print(response.text)
        return None


def example_2_custom_parameters():
    """
    示例 2: 使用自定义参数
    
    设置自定义权重和 Bootstrap
    """
    print("\n" + "="*60)
    print("示例 2: 自定义参数分析")
    print("="*60)
    
    params = {
        "run_bootstrap": False,
        "weights": [0.4, 0.3, 0.3],  # 自定义权重
        "use_cache": False  # 不使用缓存，强制重新计算
    }
    
    print(f"参数: {json.dumps(params, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/api/analyze_zenodo",
        json=params
    )
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"\n✅ 分析成功!")
        print(f"📈 CBS 得分: {data['sleuth_analysis']['cbs_score']:.4f}")
        
        if 'metrics' in data['sleuth_analysis']:
            print(f"\n详细指标:")
            print(f"  PSI: {data['sleuth_analysis']['metrics']['psi']:.4f}")
            print(f"  CCS: {data['sleuth_analysis']['metrics']['ccs']:.4f}")
            print(f"  ρ_PC: {data['sleuth_analysis']['metrics']['rho_pc']:.4f}")
        
        return data
    else:
        print(f"❌ 错误: {response.status_code}")
        return None


def example_3_get_dataset_info():
    """
    示例 3: 先查看数据集信息
    
    在分析前，先获取数据集摘要
    """
    print("\n" + "="*60)
    print("示例 3: 获取数据集信息")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/zenodo/summary")
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"\n📋 数据集信息:")
        print(f"  DOI: {data['doi']}")
        print(f"  标题: {data['title']}")
        print(f"  作者: {', '.join(data['creators'])}")
        print(f"  发布日期: {data['publication_date']}")
        print(f"  许可证: {data['license']}")
        
        print(f"\n📂 可用文件:")
        for file in data['files']:
            size_mb = file['size'] / (1024 * 1024)
            print(f"  - {file['key']} ({size_mb:.2f} MB)")
        
        return data
    else:
        print(f"❌ 错误: {response.status_code}")
        return None


def example_4_cache_comparison():
    """
    示例 4: 缓存性能对比
    
    演示缓存的性能提升
    """
    print("\n" + "="*60)
    print("示例 4: 缓存性能对比")
    print("="*60)
    
    # 第一次调用 - 无缓存
    print("\n第一次调用（无缓存）...")
    start1 = time.time()
    response1 = requests.post(
        f"{BASE_URL}/api/analyze_zenodo",
        json={"use_cache": True}
    )
    time1 = time.time() - start1
    
    if response1.status_code == 200:
        data1 = response1.json()
        from_cache1 = data1['processing_info'].get('from_cache', False)
        print(f"  时间: {time1:.2f}秒")
        print(f"  来自缓存: {from_cache1}")
    
    # 第二次调用 - 使用缓存
    print("\n第二次调用（应该使用缓存）...")
    start2 = time.time()
    response2 = requests.post(
        f"{BASE_URL}/api/analyze_zenodo",
        json={"use_cache": True}
    )
    time2 = time.time() - start2
    
    if response2.status_code == 200:
        data2 = response2.json()
        from_cache2 = data2['processing_info'].get('from_cache', False)
        print(f"  时间: {time2:.2f}秒")
        print(f"  来自缓存: {from_cache2}")
        
        if from_cache2:
            speedup = time1 / time2
            print(f"\n🚀 缓存加速: {speedup:.1f}x 更快!")
        else:
            print(f"\n⚠️  注意: 缓存可能未生效")


def example_5_clear_cache():
    """
    示例 5: 清除缓存
    
    当数据集更新后，清除缓存
    """
    print("\n" + "="*60)
    print("示例 5: 清除缓存")
    print("="*60)
    
    response = requests.post(f"{BASE_URL}/api/cache/clear")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ {data['message']}")
        return True
    else:
        print(f"❌ 错误: {response.status_code}")
        return False


def example_6_error_handling():
    """
    示例 6: 错误处理
    
    演示如何处理各种错误情况
    """
    print("\n" + "="*60)
    print("示例 6: 错误处理示例")
    print("="*60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze_zenodo",
            json={"run_bootstrap": True},
            timeout=60
        )
        
        response.raise_for_status()  # 抛出 HTTP 错误
        
        data = response.json()
        print(f"✅ 请求成功")
        return data
        
    except requests.exceptions.Timeout:
        print("❌ 错误: 请求超时")
        print("   建议: 增加超时时间或禁用 Bootstrap")
        
    except requests.exceptions.ConnectionError:
        print("❌ 错误: 无法连接到服务器")
        print("   建议: 检查服务器是否运行 (python app.py)")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 错误: {e}")
        if e.response.status_code == 400:
            print("   这通常是数据验证错误")
            print(f"   详情: {e.response.json()}")
        elif e.response.status_code == 500:
            print("   服务器内部错误")
            print(f"   详情: {e.response.json()}")
    
    except Exception as e:
        print(f"❌ 未知错误: {str(e)}")
    
    return None


def example_7_frontend_integration():
    """
    示例 7: 前端集成示例（伪代码）
    
    展示如何在前端 JavaScript 中使用
    """
    print("\n" + "="*60)
    print("示例 7: 前端集成示例（JavaScript）")
    print("="*60)
    
    js_code = """
// 前端 JavaScript 示例

async function analyzeBias() {
  try {
    // 显示加载状态
    showLoading();
    
    // 调用 API
    const response = await fetch('http://localhost:5000/api/analyze_zenodo', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        run_bootstrap: false,
        use_cache: true
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    // 显示结果
    displayResults({
      score: data.sleuth_analysis.cbs_score,
      biasDetected: data.sleuth_analysis.bias_detected,
      datasetTitle: data.source_data.title,
      processingTime: data.processing_info.elapsed_time_seconds
    });
    
  } catch (error) {
    console.error('分析失败:', error);
    showError('分析失败，请稍后重试');
  } finally {
    hideLoading();
  }
}

// 调用
analyzeBias();
"""
    
    print(js_code)


def main():
    """运行所有示例"""
    
    print("\n" + "="*70)
    print("  Zenodo-Sleuth 集成 API 使用示例")
    print("="*70)
    print(f"\n服务器地址: {BASE_URL}")
    print("确保服务器正在运行: python app.py")
    print("\n按 Ctrl+C 可随时退出\n")
    
    input("按 Enter 开始运行示例...")
    
    try:
        # 示例 1: 简单分析
        example_1_simple_analysis()
        input("\n按 Enter 继续下一个示例...")
        
        # 示例 2: 自定义参数
        example_2_custom_parameters()
        input("\n按 Enter 继续下一个示例...")
        
        # 示例 3: 获取数据集信息
        example_3_get_dataset_info()
        input("\n按 Enter 继续下一个示例...")
        
        # 示例 4: 缓存对比
        example_4_cache_comparison()
        input("\n按 Enter 继续下一个示例...")
        
        # 示例 5: 清除缓存
        example_5_clear_cache()
        input("\n按 Enter 继续下一个示例...")
        
        # 示例 6: 错误处理
        example_6_error_handling()
        input("\n按 Enter 继续下一个示例...")
        
        # 示例 7: 前端集成
        example_7_frontend_integration()
        
        print("\n" + "="*70)
        print("  所有示例运行完成！")
        print("="*70)
        print("\n更多信息请参考:")
        print("  - README_ZENODO.md (快速入门)")
        print("  - ZENODO_INTEGRATION_GUIDE.md (完整文档)")
        print("  - INTEGRATION_SUMMARY.md (架构总结)")
        
    except KeyboardInterrupt:
        print("\n\n已取消")
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")


if __name__ == "__main__":
    main()
