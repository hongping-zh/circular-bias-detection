# 算法增强实施路线图 🗺️

## 📊 项目概览

**目标**: 通过新检测指标和机器学习集成，将循环偏差检测准确率从 93% 提升至 97%+

**时间线**: 8-10周

**优先级**: ⭐⭐⭐⭐⭐ 高优先级

---

## ✅ 已完成工作（当前状态）

### 代码实现
- ✅ **新指标模块** (`circular_bias_detector/advanced_metrics.py`)
  - TDI: 时间依赖指数
  - ICS: 信息准则分数
  - CBI: 跨基准不一致性
  - ADS: 自适应漂移分数
  - MCI: 多约束交互指数

- ✅ **ML集成模块** (`circular_bias_detector/ml_detector.py`)
  - MLBiasDetector: XGBoost分类器
  - EnsembleBiasDetector: 统计+ML集成
  - 特征工程（19个特征）
  - SHAP可解释性支持

- ✅ **示例代码** (`examples/advanced_detection_example.py`)
  - 4个完整演示场景
  - 交互式教程

- ✅ **测试套件** (`tests/test_advanced_metrics.py`)
  - 30+ 单元测试
  - 边界情况测试

### 文档
- ✅ 核心文档 (`docs/ALGORITHM_ENHANCEMENT.md`)
- ✅ 本路线图文档

---

## 🚀 Phase 1: 核心功能验证（Week 1-2）

### Week 1: 集成与测试

#### 任务清单
- [ ] **代码集成**
  ```bash
  # 更新 __init__.py 导出新模块
  # 确保向后兼容
  ```
  
- [ ] **运行测试套件**
  ```bash
  cd circular-bias-detection
  python -m pytest tests/test_advanced_metrics.py -v
  python examples/advanced_detection_example.py
  ```

- [ ] **修复依赖**
  ```bash
  # 更新 requirements.txt
  pip install xgboost scikit-learn shap
  ```

- [ ] **性能基准测试**
  - 新指标计算时间
  - 内存使用
  - 与现有指标比较

#### 验收标准
- ✓ 所有测试通过
- ✓ 示例脚本正常运行
- ✓ 无性能退化

### Week 2: 真实数据验证

#### 任务清单
- [ ] **在现有数据集上测试**
  - Computer Vision (ImageNet)
  - NLP (GLUE)
  - Recommender Systems (MovieLens)

- [ ] **评估指标改进**
  - 准确率提升
  - 召回率提升
  - F1分数提升
  - ROC-AUC提升

- [ ] **案例研究**
  - 选择3个真实偏差案例
  - 对比新旧指标检测效果
  - 生成对比报告

#### 交付物
- 📄 验证报告 (`VALIDATION_REPORT.md`)
- 📊 性能对比图表
- 📝 案例研究文档

---

## 🤖 Phase 2: ML模型训练与优化（Week 3-5）

### Week 3: 数据集构建

#### 任务清单
- [ ] **合成数据生成**
  ```python
  # 生成1000+标注样本
  # 覆盖不同偏差强度 (0.0 - 1.0)
  # 不同数据规模 (T=10-50, K=3-10)
  ```

- [ ] **真实案例标注**
  - 收集已知偏差案例（从论文、评审意见）
  - 标注偏差类型和严重程度
  - 目标: 100+ 真实样本

- [ ] **数据增强**
  - 时间序列扰动
  - 算法数量变化
  - 约束维度变化

#### 交付物
- 📦 标注数据集 (`data/ml_training_dataset.csv`)
- 📄 数据文档 (`data/ML_DATASET_README.md`)

### Week 4: 模型训练

#### 任务清单
- [ ] **XGBoost优化**
  ```python
  # 超参数网格搜索
  param_grid = {
      'max_depth': [3, 5, 7],
      'learning_rate': [0.01, 0.1, 0.3],
      'n_estimators': [50, 100, 200],
      'subsample': [0.6, 0.8, 1.0]
  }
  ```

- [ ] **交叉验证**
  - 5-fold CV
  - 时间序列分割
  - 分层采样

- [ ] **特征选择**
  - SHAP重要性分析
  - 递归特征消除
  - 相关性分析

#### 验收标准
- ✓ CV AUC > 0.90
- ✓ 测试集 AUC > 0.88
- ✓ F1 score > 0.85

### Week 5: 集成优化

#### 任务清单
- [ ] **权重优化**
  ```python
  # 在验证集上搜索最优权重
  # 统计 vs ML权重比例
  best_weights = optimize_ensemble_weights(X_val, y_val)
  ```

- [ ] **校准**
  - Platt scaling
  - Isotonic regression
  - 置信度校准

- [ ] **错误分析**
  - 分析误检案例
  - 分析漏检案例
  - 迭代改进

#### 交付物
- 🎯 优化后的模型 (`models/bias_detector_v2.pkl`)
- 📊 性能报告
- 🔍 错误分析文档

---

## 🔬 Phase 3: 高级功能开发（Week 6-7）

### Week 6: LSTM时序模型（可选）

#### 任务清单
- [ ] **架构设计**
  - LSTM + Attention
  - 多头注意力机制
  - 残差连接

- [ ] **数据准备**
  - 滑动窗口切分
  - 序列填充
  - PyTorch DataLoader

- [ ] **训练与评估**
  - 与XGBoost对比
  - 消融实验
  - 可视化注意力权重

#### 决策点
如果 LSTM performance > XGBoost + 5%，则继续；否则跳过

### Week 7: 在线学习能力

#### 任务清单
- [ ] **增量学习**
  ```python
  # 支持模型在线更新
  detector.partial_fit(X_new, y_new)
  ```

- [ ] **主动学习**
  - 不确定性采样
  - 查询最有价值样本
  - 人工标注接口

- [ ] **模型版本管理**
  - 自动保存检查点
  - 模型回滚机制
  - A/B测试框架

---

## 🎯 Phase 4: 系统集成（Week 8-9）

### Week 8: API更新

#### 任务清单
- [ ] **更新BiasDetector类**
  ```python
  class BiasDetector:
      def detect_bias(self, ..., 
                     use_advanced_metrics=True,
                     use_ml=True,
                     ensemble_mode='auto'):
          # 集成新功能
  ```

- [ ] **CLI工具更新**
  ```bash
  circular-bias detect data.csv \
      --advanced-metrics \
      --ml-model models/bias_detector_v2.pkl \
      --explain
  ```

- [ ] **Web应用集成**
  - 后端API更新
  - 前端UI增强
  - 实时ML推理

#### 交付物
- 📦 更新的Python包
- 🔧 更新的CLI工具
- 🌐 更新的Web应用

### Week 9: 文档与示例

#### 任务清单
- [ ] **API文档**
  - Sphinx文档生成
  - 所有新函数docstring
  - 类型提示完善

- [ ] **教程更新**
  - 快速开始指南
  - 高级用法教程
  - ML模型训练指南

- [ ] **Jupyter Notebooks**
  - `tutorial_advanced_metrics.ipynb`
  - `tutorial_ml_integration.ipynb`
  - `tutorial_ensemble_detection.ipynb`

---

## 🚢 Phase 5: 发布与推广（Week 10）

### Week 10: 发布准备

#### 任务清单
- [ ] **版本发布**
  - 更新版本号到 v2.0.0
  - 撰写CHANGELOG
  - Git标签

- [ ] **性能报告**
  ```
  检测准确率:  93.2% → 96.8% (+3.6%)
  召回率:      89.0% → 94.5% (+5.5%)
  F1分数:      91.0% → 95.6% (+4.6%)
  ```

- [ ] **论文更新**
  - 撰写方法学部分
  - 实验结果章节
  - 消融研究

- [ ] **社区推广**
  - GitHub Release
  - 技术博客文章
  - 学术会议投稿

---

## 📈 关键性能指标 (KPI)

### 检测性能
| 指标 | 当前 | 目标 | 状态 |
|------|------|------|------|
| 准确率 | 93.2% | 97.0% | 🎯 |
| 召回率 | 89.0% | 94.0% | 🎯 |
| F1分数 | 91.0% | 95.5% | 🎯 |
| AUC | 0.94 | 0.97 | 🎯 |

### 计算效率
| 指标 | 要求 |
|------|------|
| 检测时间 | < 2秒 (中等数据集) |
| 内存占用 | < 500MB |
| 模型大小 | < 50MB |

### 可用性
- [ ] 零配置使用（开箱即用）
- [ ] 详细的错误信息
- [ ] 可视化解释
- [ ] 多语言文档

---

## 🛠️ 技术栈

### 核心依赖
```txt
numpy>=1.20.0
pandas>=1.3.0
scipy>=1.7.0
xgboost>=1.5.0        # 新增
scikit-learn>=1.0.0   # 新增
shap>=0.40.0          # 新增（可选）
```

### 可选依赖
```txt
torch>=1.10.0         # LSTM模型
plotly>=5.0.0         # 交互可视化
jupyter>=1.0.0        # Notebooks
```

---

## 🔄 持续改进计划

### 短期（3个月内）
1. **用户反馈收集**
   - 创建GitHub Issues模板
   - 用户调研问卷
   - 使用统计分析

2. **Bug修复**
   - 快速响应bug报告
   - 每周发布补丁版本

3. **性能优化**
   - 代码profiling
   - 向量化优化
   - 缓存策略

### 中期（6个月内）
1. **新领域支持**
   - 强化学习评估
   - 多模态模型评估
   - 联邦学习评估

2. **企业功能**
   - 团队协作功能
   - 审计日志
   - 权限管理

3. **云服务**
   - REST API服务
   - Docker容器化
   - K8s部署

### 长期（1年内）
1. **自动化研究**
   - 自动发现新偏差模式
   - 元学习优化
   - 自适应阈值

2. **生态系统**
   - 与MLflow集成
   - 与Weights & Biases集成
   - 与TensorBoard集成

---

## 💡 快速开始

### 安装增强版本
```bash
cd circular-bias-detection
pip install -e .[ml]  # 包含ML依赖
```

### 测试新功能
```bash
# 运行示例
python examples/advanced_detection_example.py

# 运行测试
pytest tests/test_advanced_metrics.py -v
```

### 使用新指标
```python
from circular_bias_detector.advanced_metrics import compute_all_advanced_metrics

results = compute_all_advanced_metrics(
    performance_matrix, 
    constraint_matrix
)

print(f"TDI: {results['tdi']:.4f}")
print(f"ICS: {results['ics']:.4f}")
print(f"ADS: {results['ads']:.4f}")
print(f"MCI: {results['mci']:.4f}")
```

### 使用ML检测
```python
from circular_bias_detector.ml_detector import MLBiasDetector

# 训练（一次性）
detector = MLBiasDetector()
detector.train(X_train, y_train)

# 预测
features = detector.extract_features(perf, const)
prediction, probability = detector.predict(features.reshape(1, -1))

print(f"Bias probability: {probability[0]:.2%}")
```

---

## 📞 支持与联系

- **GitHub Issues**: 技术问题和bug报告
- **Discussions**: 功能建议和讨论
- **Email**: yujjam@uest.edu.gr

---

## 🙏 贡献

欢迎贡献！优先领域：
1. 新的检测指标设计
2. ML模型改进
3. 真实案例标注
4. 文档改进
5. 性能优化

请参考 `CONTRIBUTING.md`

---

## 📄 许可证

CC BY 4.0 - 自由用于学术和商业用途，需注明出处

---

**最后更新**: 2025-10-22  
**版本**: v2.0-dev  
**状态**: 🚧 开发中
