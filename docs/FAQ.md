# FAQ

## 安装失败或版本冲突怎么办？
- 确认 Python 版本满足项目要求（见 README 与 pyproject/requirements）。
- 使用全新虚拟环境：`python -m venv .venv && source .venv/bin/activate`（Windows 使用 `.venv\Scripts\activate`）。
- 升级 pip：`pip install -U pip`。
- 若遇到编译依赖，参考系统提示安装如 `build-essential`/`clang` 等工具链。

## 数据格式有什么要求？
- 保证 X（样本/特征）、S（评分器输出）、Y（可选基准）在样本维度对齐（同一主键/索引）。
- JSONL 建议每行一个样本；CSV 请在 README/文档中注明字段含义。

## 没有 Y（基准标签）还能检测吗？
- 可以。CBD 侧重检测“依赖/循环性”结构信号与稳健性分析；Y 为可选但有助于校准。

## 报告显示高风险时该如何处理？
- 复查数据采样与评分器配置，固定评测环境与参数。
- 引入外部独立基准或去相关化的评测集。
- 增加重抽样规模、加入对照组或替代评分器复核。

## 性能与资源开销
- 离线批处理：时间取决于样本量与重抽样次数。
- 在线监控：按 QPS 设置滑动窗口与抽样率；必要时异步化。

## 支持哪些操作系统？
- 支持主流 Windows/macOS/Linux。若遇编译型依赖，请按具体系统提示安装工具链。

## 如何在论文/项目中引用？
- 参见 README 的 Citation 部分（包含 DOI 与 JOSS 评审链接）。
