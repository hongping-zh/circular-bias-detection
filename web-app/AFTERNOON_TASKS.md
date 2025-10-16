# 🎯 Afternoon Tasks - MVP Phase 2

## 📅 任务清单

### ✅ 上午已完成
- [x] 进度条 + Web Worker
- [x] 错误处理增强
- [x] 交互式教程
- [x] Chart.js可视化（3个图表）
- [x] 数学公式文档
- [x] 数据准备指南

---

## 🚀 下午任务

### 任务1: Baseline基线选项 (估时: 1小时)

#### A. 新增UI组件

**文件:** `src/components/BaselineSelector.jsx`

**功能:**
- 下拉选择对照组
- 选项：
  - "No Baseline" (默认)
  - "First Time Period" (第一个时间段)
  - "Best Performer" (最佳算法)
  - "Worst Performer" (最差算法)
  - "Median Algorithm" (中位数算法)

**实现要点:**
```jsx
<select onChange={handleBaselineChange}>
  <option value="none">No Baseline</option>
  <option value="first_period">First Time Period</option>
  <option value="best">Best Performer</option>
  <option value="worst">Worst Performer</option>
  <option value="median">Median Algorithm</option>
</select>
```

#### B. 对照组比较逻辑

**文件:** `src/utils/baselineComparison.js`

**函数:**
```javascript
function computeBaselineDiff(currentResults, baselineResults) {
  return {
    psi_diff: currentResults.psi - baselineResults.psi,
    ccs_diff: currentResults.ccs - baselineResults.ccs,
    rho_pc_diff: currentResults.rho_pc - baselineResults.rho_pc,
    improvement_percentage: ...
  };
}
```

#### C. 差异可视化

**文件:** 更新 `src/components/VisualizationCharts.jsx`

**新增图表:**
- 对比条形图（Baseline vs Current）
- 差异百分比显示
- 改善/恶化指示器

---

### 任务2: 用户群体分析 (估时: 1.5小时)

#### A. 分组计算逻辑

**文件:** `src/utils/groupAnalysis.js`

**功能:**
- 按算法分组
- 按时间段分组
- 按性能范围分组（高/中/低）
- 自定义分组条件

**实现要点:**
```javascript
function groupByPerformance(data) {
  const high = data.filter(d => d.performance > 0.8);
  const medium = data.filter(d => d.performance >= 0.5 && d.performance <= 0.8);
  const low = data.filter(d => d.performance < 0.5);
  
  return { high, medium, low };
}
```

#### B. 子群体偏差检测

**文件:** 更新 `src/utils/dataValidator.js`

**功能:**
- 为每个群体分别计算PSI, CCS, ρ_PC
- 检测群体间差异
- 标记异常群体

#### C. 对比可视化

**文件:** `src/components/GroupComparisonChart.jsx`

**新增图表:**
- 分组条形图（各群体指标对比）
- 雷达图（多维度对比）
- 分组箱线图（分布对比）

---

### 任务3: 增强可视化 (估时: 1小时)

#### A. 推荐物品分布图

**文件:** `src/components/DistributionHeatmap.jsx`

**使用:** Chart.js Matrix (Heatmap plugin)

**安装:**
```bash
npm install chartjs-chart-matrix
```

**功能:**
- 算法 × 时间段热力图
- 颜色深度表示性能
- 鼠标悬停显示详细值

#### B. 用户兴趣变化图

**文件:** `src/components/InterestDriftChart.jsx`

**类型:** 堆叠面积图 (Stacked Area Chart)

**功能:**
- X轴: 时间段
- Y轴: 兴趣强度
- 面积: 不同类别的占比
- 显示兴趣漂移趋势

#### C. 茧房效应可视化

**文件:** `src/components/FilterBubbleIndicator.jsx`

**指标:**
```javascript
filterBubbleScore = concentrationIndex * diversityLoss
```

**可视化:**
- 环形图显示集中度
- 趋势线显示多样性下降
- 警告指示器（茧房效应严重度）

#### D. 不同用户组对比图

**文件:** 更新 `src/components/GroupComparisonChart.jsx`

**类型:** 分组条形图 + 误差线

**功能:**
- 并排显示各组指标
- 误差线表示组内变异
- 高亮显示显著差异

---

## 📁 文件结构

```
web-app/src/
├── components/
│   ├── BaselineSelector.jsx          ← 新建
│   ├── GroupComparisonChart.jsx      ← 新建
│   ├── DistributionHeatmap.jsx       ← 新建
│   ├── InterestDriftChart.jsx        ← 新建
│   ├── FilterBubbleIndicator.jsx     ← 新建
│   ├── VisualizationCharts.jsx       ← 更新（添加baseline对比）
│   └── Dashboard.jsx                 ← 更新（集成新组件）
├── utils/
│   ├── baselineComparison.js         ← 新建
│   ├── groupAnalysis.js              ← 新建
│   └── dataValidator.js              ← 更新（添加分组检测）
└── App.jsx                            ← 更新（baseline状态管理）
```

---

## 🔧 技术要求

### 额外依赖

```bash
# 热力图支持
npm install chartjs-chart-matrix

# 可选：更多图表类型
npm install chartjs-plugin-datalabels
```

### Chart.js配置

需要注册新的图表类型：

```javascript
import { Chart } from 'chart.js';
import { MatrixController, MatrixElement } from 'chartjs-chart-matrix';

Chart.register(MatrixController, MatrixElement);
```

---

## ✅ 实施步骤

### Step 1: 安装依赖 (5分钟)

```bash
cd C:\Users\14593\CascadeProjects\circular-bias-detection\web-app
npm install chartjs-chart-matrix chartjs-plugin-datalabels
```

### Step 2: Baseline功能 (60分钟)

1. 创建 `BaselineSelector.jsx` (15分钟)
2. 创建 `baselineComparison.js` (20分钟)
3. 更新 `VisualizationCharts.jsx` (15分钟)
4. 更新 `App.jsx` 集成 (10分钟)

### Step 3: 用户群体分析 (90分钟)

1. 创建 `groupAnalysis.js` (30分钟)
2. 更新 `dataValidator.js` (20分钟)
3. 创建 `GroupComparisonChart.jsx` (40分钟)

### Step 4: 增强可视化 (60分钟)

1. 创建 `DistributionHeatmap.jsx` (20分钟)
2. 创建 `InterestDriftChart.jsx` (15分钟)
3. 创建 `FilterBubbleIndicator.jsx` (15分钟)
4. 集成到 `Dashboard.jsx` (10分钟)

### Step 5: 测试和调试 (30分钟)

1. 本地测试所有新功能
2. 检查响应式布局
3. 验证计算逻辑
4. 修复bugs

### Step 6: 部署 (15分钟)

```bash
git add -A
git commit -m "feat: Add MVP Phase 2 - Baseline, Groups, Enhanced Viz"
git push origin main
npm run deploy
```

---

## 🎯 预期成果

### 新增功能

1. **Baseline对照**
   - ✅ 5种baseline选项
   - ✅ 差异计算
   - ✅ 对比可视化

2. **群体分析**
   - ✅ 3种分组方式
   - ✅ 子群体偏差检测
   - ✅ 群体对比图表

3. **增强可视化**
   - ✅ 热力图（算法×时间）
   - ✅ 兴趣漂移图（堆叠面积）
   - ✅ 茧房效应指示器
   - ✅ 分组对比图

### 预计代码量

| 组件 | 估计行数 |
|------|---------|
| BaselineSelector.jsx | 80 |
| baselineComparison.js | 120 |
| groupAnalysis.js | 150 |
| GroupComparisonChart.jsx | 200 |
| DistributionHeatmap.jsx | 120 |
| InterestDriftChart.jsx | 100 |
| FilterBubbleIndicator.jsx | 100 |
| 集成更新 | 100 |
| **总计** | **~970行** |

---

## 📊 优先级排序

如果时间紧张，按此顺序实施：

1. **最高优先级:** Baseline对照 (用户最需要)
2. **高优先级:** 群体分析 (核心功能)
3. **中优先级:** 分布热力图 (直观)
4. **低优先级:** 茧房效应可视化 (锦上添花)

---

## 🐛 潜在问题

### 问题1: Chart.js热力图渲染慢

**解决方案:**
- 限制数据点数量（最多50×50）
- 使用虚拟化
- 添加加载动画

### 问题2: 分组计算复杂度高

**解决方案:**
- 缓存计算结果
- 使用Web Worker异步计算
- 限制最大分组数

### 问题3: 太多图表影响性能

**解决方案:**
- 懒加载图表（滚动到可见时才渲染）
- 选项卡切换显示
- 提供"简化视图"选项

---

## 📝 代码模板

### BaselineSelector.jsx 骨架

```javascript
import React from 'react';

function BaselineSelector({ onBaselineChange }) {
  return (
    <div className="baseline-selector">
      <label>Compare Against Baseline:</label>
      <select onChange={(e) => onBaselineChange(e.target.value)}>
        <option value="none">No Baseline</option>
        <option value="first_period">First Time Period</option>
        <option value="best">Best Performer</option>
        <option value="worst">Worst Performer</option>
        <option value="median">Median Algorithm</option>
      </select>
    </div>
  );
}

export default BaselineSelector;
```

### groupAnalysis.js 骨架

```javascript
export function groupByPerformance(data, thresholds = { high: 0.8, low: 0.5 }) {
  // 分组逻辑
}

export function computeGroupBias(group) {
  // 计算群体偏差
}

export function compareGroups(groups) {
  // 群体对比
}
```

---

## ✅ 检查清单

下午开始前检查：

- [ ] Chart.js已安装
- [ ] 依赖包已更新
- [ ] 本地开发服务器运行正常
- [ ] Git工作区干净
- [ ] 有咖啡/茶 ☕

完成后检查：

- [ ] 所有新组件创建
- [ ] 功能本地测试通过
- [ ] 无控制台错误
- [ ] 响应式布局正常
- [ ] Git提交完成
- [ ] 部署到GitHub Pages

---

## 🎉 完成后成果

**新增功能:**
- 5种Baseline对照模式
- 3种群体分析方式
- 4种增强可视化

**总代码量:**
- 上午: ~2114行
- 下午: ~970行
- **总计: ~3084行**

**项目状态:**
- MVP Phase 1: ✅ 完成
- MVP Phase 2: ⏳ 下午完成
- 生产就绪: 🎯 接近

---

## 💡 提示

1. **先实现核心逻辑，后优化UI**
2. **每完成一个功能就提交Git**
3. **遇到问题先查Chart.js文档**
4. **保持代码简洁，避免过度工程**

---

**祝下午工作顺利！休息好！** 😊☕

---

**快捷命令备忘：**

```bash
# 安装依赖
npm install chartjs-chart-matrix chartjs-plugin-datalabels

# 启动开发
npm run dev

# 构建
npm run build

# 部署
npm run deploy
```
