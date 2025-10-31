import gradio as gr
import pandas as pd
import numpy as np
from circular_bias_detector import SimpleBiasDetector

# Initialize once
detector = SimpleBiasDetector()

REQUIRED_COLUMNS = [
    "time_period", "algorithm", "performance",
    "constraint_compute", "constraint_memory"
]

def detect_bias_from_csv(file):
    try:
        df = pd.read_csv(file.name)
        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            return (
                f"❌ CSV 缺少必要列: {missing}\n"
                f"请参考示例：time_period, algorithm, performance, constraint_compute, constraint_memory"
            )

        # Build matrices
        perf = df.pivot(index="time_period", columns="algorithm", values="performance").values
        const = df.groupby("time_period")[
            ["constraint_compute", "constraint_memory"]
        ].first().values

        result = detector.quick_check(perf, const)
        if result.get("has_bias"):
            rec = result.get("recommendation", "Bias detected. Please review your evaluation setup.")
            risk = result.get("risk_level", "unknown").upper()
            return f"⚠️ {risk} RISK\n{rec}"
        else:
            return "✅ No bias detected"
    except Exception as e:
        return f"❌ 处理失败：{type(e).__name__}: {e}"

EXAMPLE_URL = "https://raw.githubusercontent.com/hongping-zh/circular-bias-detection/main/data/tiny_sample.csv"

with gr.Blocks(title="Sleuth - Circular Bias Detection") as demo:
    gr.Markdown("# Sleuth: Circular Bias Detection")
    gr.Markdown(
        "上传评测日志 CSV（包含列：time_period, algorithm, performance, "
        "constraint_compute, constraint_memory），即刻检测循环偏差。"
    )
    with gr.Row():
        file_in = gr.File(label="Upload CSV", file_count="single", type="filepath")
        out = gr.Textbox(label="Detection Result", lines=6)
    btn = gr.Button("Detect Bias")
    btn.click(fn=detect_bias_from_csv, inputs=file_in, outputs=out)

    gr.Markdown("或使用示例数据一键体验：")
    gr.Examples(
        examples=[[EXAMPLE_URL]],
        inputs=[file_in],
        label="Try with tiny_sample.csv"
    )

if __name__ == "__main__":
    demo.launch()
