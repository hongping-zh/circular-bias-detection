# 🎯 导师需求 - 48小时冲刺计划

**制定时间：** 2025-10-15 17:16  
**目标：** 48小时内完成导师提出的4项核心需求  
**优先级：** P0 (紧急且重要)

---

## 📊 需求清单

| # | 需求 | 优先级 | 预计时间 | 状态 |
|---|------|--------|----------|------|
| 1 | 真实数据分析（Pyodide集成） | P0 | 8小时 | 🔜 待开始 |
| 2 | UI交互增强 + 动态提示 | P0 | 4小时 | 🔜 待开始 |
| 3 | 高级设置（阈值自定义） | P1 | 3小时 | 🔜 待开始 |
| 4 | 混合任务支持 + 分组分析 | P1 | 5小时 | 🔜 待开始 |

**总计：** 20小时工作量 → 48小时完成（包括测试和调试）

---

## 🎯 需求1: 真实数据分析（最高优先级）

### **现状问题**
- ❌ 当前前端使用mock数据
- ❌ Python后端已完成但未集成
- ❌ 用户无法获得真实的统计分析结果

### **解决方案：Pyodide集成**

#### **方案A: Pyodide（推荐）**
**优点：**
- ✅ 100%浏览器内运行
- ✅ 无需后端服务器
- ✅ 隐私保护（数据不离开浏览器）
- ✅ 部署简单（静态网站）

**缺点：**
- ⚠️ 首次加载较慢（~50MB）
- ⚠️ Bootstrap可能较慢（但可优化）

#### **方案B: Flask API（备用）**
**优点：**
- ✅ 性能更好
- ✅ 已有完整后端

**缺点：**
- ❌ 需要服务器
- ❌ 数据隐私问题
- ❌ 部署复杂

**决策：优先实现方案A（Pyodide），保留方案B作为企业版选项**

---

### **实施步骤**

#### **Step 1: Pyodide环境配置（1小时）**

```javascript
// src/utils/pyodideLoader.js
export async function loadPyodide() {
  const pyodide = await loadPyodideInstance({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/"
  });
  
  // 加载必要的包
  await pyodide.loadPackage(['numpy', 'pandas', 'scipy']);
  
  return pyodide;
}
```

#### **Step 2: Python代码打包（2小时）**

创建单文件版本的算法：
```python
# backend/pyodide_bundle.py
# 将psi_calculator, ccs_calculator, rho_pc_calculator, bias_scorer
# 合并为单个文件，便于在浏览器加载
```

#### **Step 3: JS-Python桥接（3小时）**

```javascript
// src/services/biasDetector.js
export async function detectBias(csvData, options) {
  const pyodide = await getPyodide(); // 单例
  
  // 传递CSV数据到Python
  pyodide.globals.set('csv_string', csvData);
  
  // 运行Python代码
  const result = await pyodide.runPythonAsync(`
    import pandas as pd
    from io import StringIO
    from bias_scorer import detect_circular_bias
    
    df = pd.read_csv(StringIO(csv_string))
    result = detect_circular_bias(df, run_bootstrap=${options.bootstrap})
    result
  `);
  
  return result.toJs();
}
```

#### **Step 4: UI集成（2小时）**

```javascript
// 替换mock数据
const handleAnalyze = async () => {
  setLoading(true);
  try {
    const result = await detectBias(csvData, { 
      bootstrap: enableBootstrap 
    });
    setResults(result);
  } catch (error) {
    showError(error);
  } finally {
    setLoading(false);
  }
};
```

---

## 🎨 需求2: UI交互增强（高优先级）

### **现状问题**
- ❌ 界面较简洁，缺乏动态反馈
- ❌ 加载状态不明显
- ❌ 结果展示不够直观
- ❌ 缺少中间步骤提示

### **解决方案**

#### **2.1 增强进度反馈（1小时）**

```javascript
// 详细进度组件
<AnalysisProgress 
  steps={[
    { name: 'Loading data', status: 'complete', time: '0.1s' },
    { name: 'Computing PSI', status: 'running', progress: 45 },
    { name: 'Computing CCS', status: 'pending' },
    { name: 'Computing ρ_PC', status: 'pending' },
    { name: 'Bootstrap CI (optional)', status: 'pending' },
    { name: 'Generating report', status: 'pending' }
  ]}
/>
```

**实现：**
- Stepper组件显示当前步骤
- 每步显示预计时间
- 实时进度条（0-100%）
- 动画效果

#### **2.2 动态提示系统（1小时）**

```javascript
// Toast通知系统
import { Toaster, toast } from 'react-hot-toast';

// 成功提示
toast.success('✅ Data loaded: 20 rows, 5 time periods');

// 警告提示
toast.warning('⚠️ Bootstrap may take 10-30 seconds');

// 错误提示
toast.error('❌ Missing required column: performance');

// 信息提示
toast.info('💡 Tip: Upload CSV with time_period, algorithm, performance columns');
```

**提示场景：**
- 文件上传成功
- 数据验证结果
- 计算开始/完成
- 异常检测到
- 建议操作

#### **2.3 结果可视化增强（2小时）**

**新增图表：**

1. **CBS风险仪表盘**
```javascript
// 半圆仪表盘显示CBS分数
<GaugeChart
  value={0.636}
  min={0}
  max={1}
  segments={[
    { end: 0.3, color: '#22c55e', label: 'Low Risk' },
    { end: 0.6, color: '#f59e0b', label: 'Medium Risk' },
    { end: 1.0, color: '#ef4444', label: 'High Risk' }
  ]}
/>
```

2. **指标雷达图**
```javascript
// 显示PSI/CCS/ρ_PC在雷达图上的位置
<RadarChart
  data={[
    { indicator: 'PSI', value: 0.8, threshold: 0.15 },
    { indicator: 'CCS', value: 0.6, threshold: 0.85 },
    { indicator: 'ρ_PC', value: 0.7, threshold: 0.5 }
  ]}
/>
```

3. **置信区间可视化**
```javascript
// 箱线图显示Bootstrap结果
<BoxPlot
  data={{
    psi: { mean: 0.82, ci: [0.75, 0.89] },
    ccs: { mean: 0.61, ci: [0.58, 0.64] },
    rho_pc: { mean: 0.71, ci: [0.65, 0.77] }
  }}
/>
```

4. **时间序列热力图**
```javascript
// 显示每个时间段每个算法的异常程度
<Heatmap
  data={anomalyScoresByPeriodAndAlgo}
  xAxis="Time Period"
  yAxis="Algorithm"
  colorScale="RdYlGn"
/>
```

---

## ⚙️ 需求3: 高级设置（中高优先级）

### **现状问题**
- ❌ 阈值固定（PSI=0.15, CCS=0.85, ρ_PC=0.5）
- ❌ 无法根据场景调整
- ❌ Bootstrap迭代数固定
- ❌ 缺少专家模式

### **解决方案**

#### **3.1 高级设置面板（2小时）**

```javascript
// Advanced Settings Modal
<AdvancedSettings>
  <Section title="Thresholds">
    <NumberInput
      label="PSI Threshold"
      value={psiThreshold}
      min={0.05}
      max={0.30}
      step={0.01}
      default={0.15}
      tooltip="Higher = more tolerant to parameter changes"
    />
    
    <NumberInput
      label="CCS Threshold"
      value={ccsThreshold}
      min={0.70}
      max={0.95}
      step={0.01}
      default={0.85}
      tooltip="Lower = more tolerant to constraint variation"
    />
    
    <NumberInput
      label="ρ_PC Threshold"
      value={rhoPcThreshold}
      min={0.30}
      max={0.70}
      step={0.05}
      default={0.50}
      tooltip="Higher = more tolerant to correlation"
    />
  </Section>
  
  <Section title="Bootstrap">
    <Select
      label="Iterations"
      options={[100, 500, 1000, 2000, 5000]}
      value={bootstrapN}
      default={1000}
    />
    
    <NumberInput
      label="Confidence Level"
      value={confidence}
      min={0.90}
      max={0.99}
      step={0.01}
      default={0.95}
      format="percentage"
    />
  </Section>
  
  <Section title="CBS Weights">
    <WeightSlider
      weights={[w1, w2, w3]}
      labels={['PSI', 'CCS', 'ρ_PC']}
      constraint="sum to 1.0"
    />
  </Section>
  
  <Section title="Detection Mode">
    <RadioGroup
      options={[
        { value: 'strict', label: 'Strict (2/3 rule)' },
        { value: 'moderate', label: 'Moderate (any indicator)' },
        { value: 'lenient', label: 'Lenient (all indicators)' }
      ]}
    />
  </Section>
</AdvancedSettings>
```

#### **3.2 预设配置（1小时）**

```javascript
// 预设场景
const presets = {
  standard: {
    name: "Standard (Recommended)",
    psi: 0.15, ccs: 0.85, rho_pc: 0.50,
    bootstrap: 1000, confidence: 0.95
  },
  
  strict: {
    name: "Strict (High Confidence)",
    psi: 0.10, ccs: 0.90, rho_pc: 0.40,
    bootstrap: 2000, confidence: 0.99
  },
  
  lenient: {
    name: "Lenient (Exploratory)",
    psi: 0.20, ccs: 0.80, rho_pc: 0.60,
    bootstrap: 500, confidence: 0.90
  },
  
  academic: {
    name: "Academic (Publication)",
    psi: 0.15, ccs: 0.85, rho_pc: 0.50,
    bootstrap: 5000, confidence: 0.95,
    note: "High bootstrap for peer review"
  },
  
  industrial: {
    name: "Industrial (Fast)",
    psi: 0.15, ccs: 0.85, rho_pc: 0.50,
    bootstrap: 100, confidence: 0.95,
    note: "Quick screening"
  }
};
```

---

## 🔀 需求4: 混合任务支持（中优先级）

### **现状问题**
- ❌ 假设所有数据来自同一任务
- ❌ 无法处理ImageNet+GLUE混合评估
- ❌ 不同任务的性能指标不可比（accuracy vs F1 vs BLEU）
- ❌ 缺少任务分组分析

### **解决方案**

#### **4.1 任务识别（1.5小时）**

**方案A: 自动识别（基于列名）**
```python
# backend/core/task_detector.py

def detect_task_type(df):
    """
    根据列名和数据特征自动识别任务类型
    """
    # 检查是否有task列
    if 'task' in df.columns or 'task_type' in df.columns:
        return df['task'].unique()
    
    # 基于列名启发式识别
    if 'imagenet' in str(df.columns).lower():
        return ['computer_vision']
    elif 'glue' in str(df.columns).lower() or 'bleu' in str(df.columns).lower():
        return ['nlp']
    
    # 基于评估协议列
    if 'evaluation_protocol' in df.columns:
        protocols = df['evaluation_protocol'].unique()
        tasks = []
        for p in protocols:
            if 'ImageNet' in p: tasks.append('CV')
            elif 'GLUE' in p or 'SQuAD' in p: tasks.append('NLP')
        return list(set(tasks))
    
    # 默认：单一任务
    return ['unknown']
```

**方案B: 用户指定（推荐）**
```javascript
// UI: 任务配置
<TaskConfiguration>
  <h3>📋 Task Detection</h3>
  
  <RadioGroup label="Detection Mode">
    <option value="auto">Auto-detect from data</option>
    <option value="manual">Manually specify</option>
  </RadioGroup>
  
  {mode === 'manual' && (
    <TaskMapper>
      {/* 根据algorithm或evaluation_protocol映射任务 */}
      <Rule>
        <Select column="algorithm" />
        <span>contains</span>
        <Input placeholder="ResNet|VGG" />
        <span>→ Task:</span>
        <Input placeholder="Computer Vision" />
      </Rule>
      
      <Rule>
        <Select column="evaluation_protocol" />
        <span>contains</span>
        <Input placeholder="GLUE|SQuAD" />
        <span>→ Task:</span>
        <Input placeholder="NLP" />
      </Rule>
      
      <Button onClick={addRule}>+ Add Rule</Button>
    </TaskMapper>
  )}
</TaskConfiguration>
```

#### **4.2 分组分析（2小时）**

```python
# backend/core/grouped_analysis.py

def analyze_by_task(df):
    """
    按任务分组进行独立分析
    """
    tasks = detect_task_type(df)
    
    results = {}
    
    for task in tasks:
        # 筛选该任务的数据
        task_df = df[df['task'] == task]
        
        # 独立分析
        task_result = detect_circular_bias(
            task_df,
            run_bootstrap=True
        )
        
        results[task] = task_result
    
    # 跨任务比较
    cross_task_analysis = compare_tasks(results)
    
    return {
        'by_task': results,
        'cross_task': cross_task_analysis
    }

def compare_tasks(task_results):
    """
    比较不同任务的偏差程度
    """
    comparison = {}
    
    for task, result in task_results.items():
        comparison[task] = {
            'cbs': result['cbs_score'],
            'bias_detected': result['bias_detected'],
            'risk_level': result['risk_level']
        }
    
    # 识别最高风险任务
    highest_risk = max(comparison.items(), 
                      key=lambda x: x[1]['cbs'])
    
    return {
        'summary': comparison,
        'highest_risk_task': highest_risk[0],
        'task_count': len(task_results)
    }
```

#### **4.3 UI展示（1.5小时）**

```javascript
// 多任务结果展示
<MultiTaskResults>
  {/* 任务概览卡片 */}
  <TaskOverview>
    {tasks.map(task => (
      <TaskCard key={task}>
        <h4>{task}</h4>
        <CBS value={results[task].cbs_score} />
        <Badge risk={results[task].risk_level} />
      </TaskCard>
    ))}
  </TaskOverview>
  
  {/* 对比图表 */}
  <TaskComparison>
    <BarChart
      data={tasks.map(t => ({
        task: t,
        psi: results[t].psi.score,
        ccs: results[t].ccs.score,
        rho_pc: results[t].rho_pc.score
      }))}
    />
  </TaskComparison>
  
  {/* 详细分析（可折叠） */}
  {tasks.map(task => (
    <Collapsible key={task} title={`${task} Details`}>
      <DetailedResults data={results[task]} />
    </Collapsible>
  ))}
</MultiTaskResults>
```

---

## 📅 48小时实施时间表

### **Day 1 (明天 - 10月16日)**

#### **上午 (9:00-12:00) - 3小时**
- ✅ Setup Pyodide环境 (1h)
- ✅ Python代码打包 (2h)

#### **下午 (14:00-18:00) - 4小时**
- ✅ JS-Python桥接 (2h)
- ✅ UI集成测试 (2h)

#### **晚上 (20:00-22:00) - 2小时**
- ✅ UI交互增强：进度组件 (1h)
- ✅ Toast通知系统 (1h)

**Day 1完成：真实数据分析 + 基础UI增强**

---

### **Day 2 (后天 - 10月17日)**

#### **上午 (9:00-12:00) - 3小时**
- ✅ 结果可视化：仪表盘 (1h)
- ✅ 结果可视化：雷达图 (1h)
- ✅ 结果可视化：热力图 (1h)

#### **下午 (14:00-18:00) - 4小时**
- ✅ 高级设置面板 (2h)
- ✅ 预设配置 (1h)
- ✅ 测试和调试 (1h)

#### **晚上 (20:00-23:00) - 3小时**
- ✅ 混合任务：后端实现 (1.5h)
- ✅ 混合任务：UI实现 (1.5h)

**Day 2完成：UI增强 + 高级设置 + 混合任务**

---

### **Day 3 (大后天 - 10月18日上午)**

#### **上午 (9:00-12:00) - 3小时**
- ✅ 集成测试 (1h)
- ✅ Bug修复 (1h)
- ✅ 文档更新 (1h)

**完成度：100%**

---

## 🎯 优先级调整建议

### **如果只有24小时：**
1. ✅ 真实数据分析（Pyodide）- 8h **必做**
2. ✅ UI交互增强（进度+通知）- 2h **必做**
3. ✅ 高级设置（阈值）- 3h **重要**
4. ⏸️ 混合任务支持 - 5h **延后**

### **如果只有12小时：**
1. ✅ 真实数据分析（Pyodide）- 8h **必做**
2. ✅ UI基础增强 - 2h **必做**
3. ✅ 高级设置（简化版）- 2h **重要**

---

## 📦 技术栈更新

### **新增依赖**

```json
{
  "dependencies": {
    "pyodide": "^0.24.1",           // Python in browser
    "react-hot-toast": "^2.4.1",     // Toast notifications
    "recharts": "^2.10.0",           // 图表库（已有）
    "framer-motion": "^10.16.0",     // 动画
    "@radix-ui/react-slider": "^1.1.2", // 滑块
    "@radix-ui/react-select": "^2.0.0", // 选择器
    "react-gauge-chart": "^0.4.1"    // 仪表盘
  }
}
```

---

## 🧪 测试计划

### **测试场景**

1. **真实数据测试**
   - [ ] sample_data.csv（已有）
   - [ ] 大型数据集（1000行）
   - [ ] 边界情况（2算法、2时间段）

2. **UI交互测试**
   - [ ] 加载状态显示
   - [ ] Toast通知触发
   - [ ] 图表交互
   - [ ] 响应式布局

3. **高级设置测试**
   - [ ] 阈值修改生效
   - [ ] 预设配置切换
   - [ ] Bootstrap参数调整

4. **混合任务测试**
   - [ ] CV + NLP混合数据
   - [ ] 任务自动识别
   - [ ] 分组分析结果

---

## 📊 成功指标

### **功能指标**
- ✅ Pyodide成功加载（<10秒）
- ✅ 真实算法计算正确
- ✅ Bootstrap完成（<30秒，1000次）
- ✅ 所有图表正确显示
- ✅ 高级设置生效
- ✅ 混合任务正确识别

### **用户体验指标**
- ✅ 进度反馈清晰
- ✅ 错误提示具体
- ✅ 交互流畅（无卡顿）
- ✅ 结果易读

---

## 🚨 风险和应对

### **风险1: Pyodide加载慢**
**影响：** 首次使用体验差  
**应对：**
- 添加加载进度条
- 缓存Pyodide（localStorage）
- 提供"跳过Bootstrap"快速模式

### **风险2: Bootstrap在浏览器太慢**
**影响：** 用户等待时间长  
**应对：**
- 默认100次迭代（可调整）
- Web Worker异步计算
- 可中断计算

### **风险3: 混合任务复杂度高**
**影响：** 实现时间超预期  
**应对：**
- 先实现简单版（用户手动指定）
- 自动识别作为v1.2功能

### **风险4: UI性能问题**
**影响：** 大数据集卡顿  
**应对：**
- 虚拟滚动
- 图表数据采样
- 懒加载组件

---

## 💡 额外建议

### **给导师的演示建议**

1. **准备3个Demo场景**
   - 场景1: 干净数据（无偏差）
   - 场景2: 明显偏差（CBS>0.6）
   - 场景3: 混合任务

2. **突出改进点**
   - Before: Mock数据 → After: 真实统计
   - Before: 固定阈值 → After: 灵活配置
   - Before: 单一任务 → After: 多任务支持
   - Before: 简单UI → After: 丰富交互

3. **准备FAQ**
   - Q: Bootstrap为什么慢？
   - A: 统计严谨性需要，可调整迭代数
   
   - Q: 如何解释CBS分数？
   - A: <0.3低风险，0.3-0.6中风险，>0.6高风险
   
   - Q: 支持哪些任务类型？
   - A: 任何时间序列评估，CV/NLP/RL均可

---

## 📝 下一步行动

### **立即执行（今晚）**
1. [ ] Review这个计划，确认优先级
2. [ ] 决定48小时 vs 24小时方案
3. [ ] 准备开发环境

### **明天早上第一件事**
1. [ ] 安装Pyodide依赖
2. [ ] 创建pyodide_bundle.py
3. [ ] 开始实现

---

## 🎉 预期成果

**48小时后，Sleuth将拥有：**

✅ **核心功能**
- 真实Python算法（浏览器内）
- Bootstrap置信区间
- 完整统计推断

✅ **灵活性**
- 阈值自定义
- Bootstrap参数调整
- 多种预设配置

✅ **扩展性**
- 混合任务支持
- 任务分组分析
- 跨任务对比

✅ **用户体验**
- 详细进度反馈
- 动态提示系统
- 丰富可视化
- 专业图表

**这将是一个production-ready的学术工具！** 🚀

---

**准备好开始了吗？** 💪

