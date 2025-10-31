# CBD 实时系统集成指南

本指南展示如何将 CBD 以“旁路审计”方式集成到在线/实时评测流水线�?
## 集成原则
- 非侵入：不改变业务主链路的评�?打分逻辑
- 低开销：批/微批监控，按需触发深入审计
- 可观测：将关键指标输出到现有监控平台（如 Prometheus/Grafana�?
## 参考架�?- 生产评测服务 �?旁路采样器（抽样请求与评分） �?CBD 审计微服�?�?报警/报表

## Python 服务化示例（伪代码）
```python
from fastapi import FastAPI
from circular_bias_detector import SimpleBiasDetector

app = FastAPI()
detector = SimpleBiasDetector()

@app.post("/audit")
def audit(batch: dict):
    # X, S, Y 的具体结构按你的数据协议定义
    performance = batch["performance"]
    constraints = batch["constraints"]
    result = detector.quick_check(performance, constraints)
    level = result.get("risk_level", "unknown")
    return {"risk_level": level, "result": result}
```

## 运行建议
- 滑动窗口与抽样率�?QPS、指标波动设�?- 审计结果阈值触发报警或灰度机制
- 定期导出报告归档，便于回�?
