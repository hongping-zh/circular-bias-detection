# Overleaf 编译说明

## 📁 已创建的文件

1. **`Circular_Bias_Survey_NMI_FINAL.tex`** - 完整的 LaTeX 主文件
2. **`references.bib`** - BibTeX 参考文献（已存在，昨天创建）
3. **本文件** - Overleaf 使用说明

---

## 🚀 在 Overleaf 中编译步骤

### 第一步：上传文件

1. 登录 Overleaf: https://www.overleaf.com
2. 创建新项目：**New Project** → **Blank Project**
3. 命名项目：`Circular_Bias_NMI_Submission`
4. 上传以下文件：
   - `Circular_Bias_Survey_NMI_FINAL.tex`
   - `references.bib`
   - 4 张图片（如果有）：
     - `figure1_feedback_loops.png` (或 .pdf)
     - `figure2_framework.png` (或 .pdf)
     - `figure3_timelines.png` (或 .pdf)

### 第二步：设置编译器

1. 点击左上角菜单按钮
2. 选择 **Settings**
3. 设置：
   - **Compiler**: pdfLaTeX
   - **TeX Live version**: 2024（或最新版本）
   - **Main document**: `Circular_Bias_Survey_NMI_FINAL.tex`

### 第三步：编译

1. 点击 **Recompile** 按钮（绿色）
2. 第一次编译可能需要 30-60 秒
3. 如果出现错误，查看日志（Log）

---

## ⚠️ 可能的编译问题和解决方案

### 问题 1: 缺少 `tcolorbox` 包

**错误信息**: `! LaTeX Error: File 'tcolorbox.sty' not found.`

**解决方案**: 在文件开头添加：
```latex
\usepackage{tcolorbox}
```

如果仍然报错，替换 Box 1 的代码为：
```latex
\begin{center}
\fbox{\begin{minipage}{0.9\textwidth}
\textbf{Box 1 | Distorted Cultural Transmission}

Circular bias in AI mirrors how human cultures transmit knowledge...
\end{minipage}}
\end{center}
```

### 问题 2: 缺少 `naturemag.bst` 文件

**错误信息**: `I couldn't open style file naturemag.bst`

**解决方案**: 将参考文献样式改为标准样式：
```latex
\bibliographystyle{unsrtnat}  % 或 plainnat
```

### 问题 3: 图片文件未找到

**错误信息**: `! LaTeX Error: File 'figure1_feedback_loops.png' not found.`

**临时解决方案**: 注释掉图片引用（编译后再添加）：
```latex
% \includegraphics[width=\textwidth]{figure1_feedback_loops.png}
```

### 问题 4: 参考文献未显示

**解决方案**: 需要编译多次
1. 第一次编译：生成 `.aux` 文件
2. 运行 BibTeX：自动或手动
3. 第二次编译：生成引用
4. 第三次编译：更新交叉引用

在 Overleaf 中，点击 **Recompile** 2-3 次即可。

---

## 📊 当前文档统计

- **字数**: 约 5,200 词（不含参考文献）✅
- **页数**: 预计 12-15 页（双倍行距）
- **参考文献**: 30 条
- **表格**: 1 个（Table 1）
- **图片**: 3 个（需要上传）
- **Box**: 1 个（Box 1）

---

## 🔧 编译后需要检查的内容

### 1. 格式检查
- [ ] 双倍行距正确
- [ ] 行号显示
- [ ] 页边距 2.5 cm
- [ ] 字体 Times New Roman 11pt

### 2. 内容检查
- [ ] 所有引用显示正确（[1], [2], 等）
- [ ] 参考文献列表完整
- [ ] 表格格式清晰
- [ ] Box 1 显示正确
- [ ] 数学公式渲染正确

### 3. 图片检查（如果上传了）
- [ ] Figure 1 显示
- [ ] Figure 2 显示
- [ ] Figure 3 显示
- [ ] 图例（Figure Legends）在文末

---

## 📝 已完成的修正

### ✅ CRITICAL 问题已修复
1. ✅ Section 2.4 完整（无中文字符）
2. ✅ 样本数量统一为 "15 seminal works"
3. ✅ 关键词精简至 5 个
4. ✅ 摘要中 AI 缩写已定义
5. ✅ 移除 "recursive skew" 冗余

### ✅ 字数已优化
- Introduction: 精简至 ~500 词
- Section 3: 精简至 ~1,500 词
- Section 5: 精简至 ~800 词
- Section 6: 精简至 ~500 词
- **总字数**: ~5,200 词 ✅

### ✅ 格式已调整
- 引用格式：Nature 数字编号
- Box 1：使用 tcolorbox
- 表格：Nature 标准格式
- 数学符号：已定义

---

## 🎯 编译成功后的下一步

1. **下载 PDF**：点击 **Download PDF** 按钮
2. **检查 PDF**：
   - 打开 PDF，逐页检查
   - 特别注意引用编号是否正确
   - 检查表格和公式是否清晰
3. **准备讨论**：
   - 记录需要调整的地方
   - 准备问题清单

---

## 💡 Overleaf 使用技巧

### 快捷键
- **Ctrl + Enter**: 编译
- **Ctrl + F**: 查找
- **Ctrl + /**: 注释/取消注释

### 协作功能
- **Share**: 可以分享链接给我查看
- **Track Changes**: 可以追踪修改
- **Comments**: 可以添加评论

### 历史版本
- **History**: 可以查看所有修改历史
- **Labels**: 可以标记重要版本

---

## 📞 遇到问题？

如果编译遇到问题：

1. **查看完整日志**：点击 **Logs and output files**
2. **复制错误信息**：发送给我
3. **截图**：如果有显示问题，截图发送

我会帮您快速解决！

---

## 🎉 准备好了吗？

1. 上传 `.tex` 和 `.bib` 文件到 Overleaf
2. 点击 **Recompile**
3. 等待 PDF 生成
4. 下载并查看
5. 告诉我结果！

**祝编译顺利！** 🚀
