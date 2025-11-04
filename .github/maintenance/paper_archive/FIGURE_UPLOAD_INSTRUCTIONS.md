# 图片上传说明

## ✅ 已完成的修改

我已经在 LaTeX 文件中添加了 4 张图片的引用代码：

1. **Figure 1** - 插入在 Section 1.2 结尾（Introduction）
2. **Figure 2** - 插入在 Section 4.4 结尾（Detection Methods）
3. **Figure 3** - 插入在 Section 5.4 结尾（Case Studies）
4. **Figure 4** - 插入在 Section 3.1 开头（Literature Synthesis）

---

## 📁 需要上传的图片文件

您需要将以下 **4 张图片**上传到 Overleaf：

### 从桌面文件夹2上传：

1. **`figure1_feedback_loops.png`** (或 .pdf, .jpg)
   - 三层反馈循环架构图
   - 建议尺寸：宽度 183mm（双栏图）
   - 分辨率：≥300 dpi

2. **`figure2_framework.png`** (或 .pdf, .jpg)
   - 四阶段治理框架图
   - 建议尺寸：宽度 183mm（双栏图）
   - 分辨率：≥300 dpi

3. **`figure3_timelines.png`** (或 .pdf, .jpg)
   - 跨领域时间演化图（4个子图）
   - 建议尺寸：宽度 183mm（双栏图）
   - 分辨率：≥300 dpi

4. **`figure4_research_trends.png`** (或 .pdf, .jpg)
   - 研究趋势和关键里程碑图（2021-2025）
   - 建议尺寸：宽度 155mm（单栏图）
   - 分辨率：≥300 dpi

---

## 🚀 在 Overleaf 中上传图片

### 方法1：拖拽上传（推荐）

1. 打开 Overleaf 项目
2. 点击左上角的 **Upload** 按钮
3. 选择 **4 张图片文件**
4. 或者直接将图片拖拽到文件列表

### 方法2：创建文件夹

1. 在 Overleaf 左侧文件列表中
2. 点击 **New Folder** 创建 `figures` 文件夹
3. 上传图片到 `figures` 文件夹
4. 修改 LaTeX 中的路径为 `figures/figure1_feedback_loops.png`

---

## 📝 图片文件名要求

LaTeX 中使用的文件名：
```latex
figure1_feedback_loops.png
figure2_framework.png
figure3_timelines.png
figure4_research_trends.png
```

**重要**：上传的文件名必须与 LaTeX 中的完全一致！

---

## ⚠️ 如果图片文件名不同

如果您的图片文件名不同（例如 `图1.png`），有两个选择：

### 选择1：重命名图片文件（推荐）
在上传前，将图片重命名为：
- `figure1_feedback_loops.png`
- `figure2_framework.png`
- `figure3_timelines.png`
- `figure4_research_trends.png`

### 选择2：修改 LaTeX 代码
在 Overleaf 中修改这 4 处：
```latex
% 第一处（约第82行）- Figure 1
\includegraphics[width=0.9\textwidth]{您的实际文件名1.png}

% 第二处（约第139行）- Figure 4
\includegraphics[width=0.85\textwidth]{您的实际文件名4.png}

% 第三处（约第256行）- Figure 2
\includegraphics[width=0.95\textwidth]{您的实际文件名2.png}

% 第四处（约第292行）- Figure 3
\includegraphics[width=\textwidth]{您的实际文件名3.png}
```

---

## 🔧 上传后的操作

1. **检查文件列表**：确认 **4 张图片**都已上传
2. **点击 Recompile**：重新编译 LaTeX
3. **查看 PDF**：图片应该正确显示
4. **检查图片质量**：
   - 图片清晰
   - 文字可读
   - 尺寸合适

---

## 📊 图片在 PDF 中的位置

编译后，图片将出现在：

| 图片 | 位置 | 页码（预计） |
|------|------|-------------|
| Figure 1 | Introduction 结尾 | 第 2-3 页 |
| Figure 4 | Section 3 开头 | 第 4-5 页 |
| Figure 2 | Section 4 结尾 | 第 8-9 页 |
| Figure 3 | Section 5 结尾 | 第 11-12 页 |

---

## ❓ 常见问题

### Q1: 图片仍然不显示？

**检查**：
1. 文件名是否完全一致（区分大小写）
2. 文件格式是否支持（.png, .pdf, .jpg）
3. 查看编译日志（Log）是否有错误

**解决**：
```
! LaTeX Error: File 'figure1_feedback_loops.png' not found.
```
→ 检查文件名拼写和大小写

### Q2: 图片太大或太小？

**调整宽度**：
```latex
% 当前设置
\includegraphics[width=0.9\textwidth]{...}  % 90% 页面宽度

% 可以改为
\includegraphics[width=0.7\textwidth]{...}  % 70% 页面宽度
\includegraphics[width=\textwidth]{...}     % 100% 页面宽度
```

### Q3: 图片位置不对？

LaTeX 会自动调整图片位置。如果需要固定位置：
```latex
\begin{figure}[H]  % 强制在此处（需要 \usepackage{float}）
```

---

## ✅ 完成检查清单

上传图片后，确认：

- [ ] **4 张图片**都已上传到 Overleaf
- [ ] 文件名与 LaTeX 中一致
- [ ] 重新编译成功（无错误）
- [ ] PDF 中显示 **4 张图片**
- [ ] 图片清晰可读
- [ ] 图片尺寸合适
- [ ] 图例（Figure Legends）在文末正确显示

---

## 🎉 完成后

如果一切正常，您的 PDF 应该包含：
- ✅ 完整的正文（约 13-16 页）
- ✅ **4 张高质量图片**
- ✅ 1 个表格（Table 1）
- ✅ 15 条参考文献
- ✅ 详细的图例说明（4 个 Figure Legends）

**准备好后，下载 PDF 并发给我查看！** 📄✨
