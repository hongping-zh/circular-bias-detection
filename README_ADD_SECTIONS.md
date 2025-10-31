
## 📁 目录结构说明

- circular_bias_detector/ 核心库代码（core/metrics.py、core/bootstrap.py 等，指标与 CBS 计算、可视化）。
- circular_bias_cli/ 命令行入口与适配器（main.py、adapters/、utils/）。
- examples/ 可运行示例、复现脚本与 Notebook（如 basic_usage_example.py、reproduce_simulations.py）。
- tests/ 单元测试与端到端测试。
- web-app/ 浏览器端应用（Vite + React + Pyodide），src/ 源码，public/ 静态资源，dist/ 构建产物。
- data/ 示例 CSV 与数据字典，用于快速试用。
- experiments/ 论文/报告复现实验脚本与表图生成。
- docs/ 使用与技术文档（可构建为文档站点）。
- paper/ 论文相关材料（图、参考文献、投稿文件）；JOSS 论文正文为根目录的 paper.md。

> 提示：若仅想快速上手，直接查看 examples/ 与 web-app/。

## ⏱️ 5分钟上手

- 方式A：Web App（零安装）
  1. 打开在线演示或本地启动 web-app（先执行 npm install；再执行 npm run dev）。
  2. 在页面导入评估日志 CSV（或使用 data/sample_data.csv）。
  3. 查看 CBS 仪表盘、雷达图与时间序列，并导出结果。

- 方式B：Python/CLI（本地离线）
  1. 安装：pip install circular-bias-detector
  2. 最小示例：使用 examples/ 下的脚本运行，或在 Python 中调用 compute_cbs。
  3. CLI 示例：circular-bias --input data/sample_data.csv --output out.json
  4. 更多示例：examples/basic_usage_example.py、examples/bootstrap_example.py、examples/reproduce_simulations.py
