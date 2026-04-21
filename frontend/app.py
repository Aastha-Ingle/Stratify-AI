import gradio as gr
import requests
import yfinance as yf
import matplotlib.pyplot as plt

BACKEND_URL = "http://127.0.0.1:8000/decision"


def get_stock_chart(ticker):
    data = yf.Ticker(ticker).history(period="1mo")
    if data.empty:
        return None

    fig, ax = plt.subplots(figsize=(7, 2.6), facecolor="#0b1220")
    ax.set_facecolor("#0b1220")
    ax.plot(data.index, data["Close"], color="#2f7df6", linewidth=2.8)
    ax.set_title(f"{ticker} Stock Price (1 Month)", color="white", fontsize=12, fontweight="bold")
    ax.set_xlabel("Date", color="#94a3b8", fontsize=9)
    ax.set_ylabel("Price", color="#94a3b8", fontsize=9)
    ax.tick_params(colors="#94a3b8", labelsize=8)

    for spine in ax.spines.values():
        spine.set_color("#22304a")

    ax.grid(alpha=0.18, color="#334155")
    fig.tight_layout()
    return fig


def detect_ticker(query):
    q = query.lower()
    if "tesla" in q:
        return "TSLA"
    if "apple" in q:
        return "AAPL"
    if "google" in q:
        return "GOOGL"
    if "amazon" in q:
        return "AMZN"
    return None


def build_history_html(history):
    if not history:
        return """
        <div class="history-box">
            <div class="history-empty">No queries yet</div>
        </div>
        """

    seen = set()
    unique_history = []
    for q in reversed(history):
        if q not in seen:
            seen.add(q)
            unique_history.append(q)

    items = "".join([f'<div class="history-item">{q}</div>' for q in unique_history[:6]])

    return f"""
    <div class="history-box">
        {items}
    </div>
    """


def chat(query, history):
    history = history or []

    try:
        response = requests.get(BACKEND_URL, params={"query": query}, timeout=15)
        data = response.json()

        decision = data.get("decision", "N/A")
        reason = data.get("reason", "N/A")
        risk = data.get("risk", "N/A")
        confidence = data.get("confidence", "N/A")

        output_html = f"""
        <div class="dashboard-grid">
            <div class="big-card">
                <div class="card-label">Decision</div>
                <div class="decision-value">{decision}</div>
            </div>
            <div class="small-card">
                <div class="card-label">Reason</div>
                <div class="card-text">{reason}</div>
            </div>
            <div class="small-card">
                <div class="card-label">Risk</div>
                <div class="card-text">{risk}</div>
            </div>
            <div class="wide-card">
                <div class="card-label">Confidence</div>
                <div class="card-text">{confidence}</div>
            </div>
        </div>
        """

        clean_query = query.strip()
        if clean_query:
            history.append(clean_query)

        ticker = detect_ticker(query)
        chart = get_stock_chart(ticker) if ticker else None
        history_html = build_history_html(history)

        return output_html, gr.update(value=chart, visible=chart is not None), history_html, history

    except Exception as e:
        error_html = f"""
        <div class="wide-card">
            <div class="card-label">Error</div>
            <div class="card-text">{str(e)}</div>
        </div>
        """
        return error_html, gr.update(value=None, visible=False), build_history_html(history), history


custom_css = """
body, .gradio-container {
    background: #07111f !important;
    color: white !important;
    font-family: 'Segoe UI', sans-serif !important;
    overflow: hidden !important;
}

.gradio-container {
    max-width: 100vw !important;
    height: 100vh !important;
    margin: 0 auto !important;
    padding: 10px !important;
}

.gradio-container > .main,
.gradio-container .wrap {
    height: 100% !important;
}

.sidebar {
    height: calc(100vh - 20px);
    background: linear-gradient(180deg, #08101d, #0b1220);
    border: 1px solid #162235;
    border-radius: 22px;
    padding: 14px 12px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.logo {
    font-size: 18px;
    font-weight: 700;
    color: white;
    margin-bottom: 14px;
}

.history-box {
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow: hidden;
}

.history-item {
    background: #0f172a;
    border: 1px solid #223049;
    color: #dbeafe;
    padding: 10px 12px;
    border-radius: 12px;
    font-size: 13px;
    line-height: 1.4;
    word-break: break-word;
}

.history-empty {
    color: #64748b;
    font-size: 13px;
    padding: 6px 2px;
}

.topbar {
    background: linear-gradient(135deg, #0f224d, #08152f) !important;
    border: 1px solid rgba(59, 130, 246, 0.30) !important;
    border-radius: 22px;
    padding: 16px 20px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28);
    margin-bottom: 12px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}

.topbar h1 {
    margin: 0;
    font-size: 22px;
    color: white;
}

.topbar p {
    margin: 4px 0 0 0;
    color: #9fb6d9;
    font-size: 13px;
}

.panel {
    background: linear-gradient(180deg, #0d1526, #0a1220);
    border: 1px solid #1a2940;
    border-radius: 22px;
    padding: 14px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.30);
    height: 100%;
    overflow: hidden;
}

.result-panel {
    height: calc(100vh - 110px);
}

.query-panel {
    height: calc(100vh - 110px);
}

.dashboard-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 10px;
}

.big-card, .small-card, .wide-card {
    background: linear-gradient(180deg, #101a2f, #0e1728);
    border: 1px solid #21314a;
    border-radius: 18px;
    padding: 16px;
}

.big-card {
    grid-column: 1 / -1;
    min-height: 96px;
    background: linear-gradient(135deg, #2563eb, #172554);
}

.wide-card {
    grid-column: 1 / -1;
}

.card-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #93c5fd;
    margin-bottom: 10px;
    font-weight: 700;
}

.decision-value {
    font-size: 28px;
    font-weight: 800;
    color: white;
}

.card-text {
    font-size: 14px;
    color: #e2e8f0;
    line-height: 1.55;
}

textarea, input {
    background: #0f172a !important;
    color: white !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

button {
    border-radius: 12px !important;
}

.primary-btn button {
    width: 100% !important;
    background: linear-gradient(180deg, #2f7df6, #1d63ea) !important;
    color: white !important;
    border: 1px solid #4ea1ff !important;
    box-shadow: 0 0 0 1px rgba(78, 161, 255, 0.18), 0 8px 24px rgba(29, 99, 234, 0.35) !important;
    font-weight: 700 !important;
    padding: 11px 18px !important;
    border-radius: 12px !important;
}

.primary-btn button:hover {
    background: linear-gradient(180deg, #4690ff, #2a72f0) !important;
    border: 1px solid #74b4ff !important;
}

.examples-title {
    color: #e5e7eb;
    font-size: 13px;
    margin: 12px 0 8px 0;
    font-weight: 600;
    background: transparent !important;
    padding: 0 !important;
}

.example-btn button {
    width: 100%;
    justify-content: flex-start !important;
    text-align: left !important;
    background: rgba(15, 23, 42, 0.92) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(255, 255, 255, 0.72) !important;
    box-shadow: none !important;
    padding: 9px 12px !important;
    margin-bottom: 8px !important;
    font-weight: 600 !important;
    border-radius: 11px !important;
    font-size: 13px !important;
}

.example-btn button:hover {
    background: rgba(30, 41, 59, 0.98) !important;
    border: 1px solid #ffffff !important;
}

footer {
    display: none !important;
}
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Base()) as demo:
    history_state = gr.State([])

    with gr.Row():
        with gr.Column(scale=2, min_width=220):
            with gr.Group(elem_classes="sidebar"):
                gr.HTML('<div class="logo"> Query History</div>')
                history_html = gr.HTML("""
                <div class="history-box">
                    <div class="history-empty">No queries yet</div>
                </div>
                """)

        with gr.Column(scale=8):
            gr.HTML("""
            <div class="topbar">
                <h1>Decision Dashboard</h1>
                <p>AI-powered business intelligence with real-time market insight</p>
            </div>
            """)

            with gr.Row():
                with gr.Column(scale=6, min_width=540):
                    with gr.Group(elem_classes=["panel", "result-panel"]):
                        output_text = gr.HTML("""
                        <div class="dashboard-grid">
                            <div class="big-card">
                                <div class="card-label">Decision</div>
                                <div class="decision-value">Awaiting Query</div>
                            </div>
                            <div class="small-card">
                                <div class="card-label">Reason</div>
                                <div class="card-text">Your backend response will appear here.</div>
                            </div>
                            <div class="small-card">
                                <div class="card-label">Risk</div>
                                <div class="card-text">Risk details will appear here.</div>
                            </div>
                            <div class="wide-card">
                                <div class="card-label">Confidence</div>
                                <div class="card-text">Confidence score will appear here.</div>
                            </div>
                        </div>
                        """)
                        output_chart = gr.Plot(label="Market Chart", visible=False)

                with gr.Column(scale=4, min_width=300):
                    with gr.Group(elem_classes=["panel", "query-panel"]):
                        user_input = gr.Textbox(
                            placeholder="Ask: Should I invest in Apple?",
                            label="Ask Your Query",
                            lines=2
                        )

                        submit_btn = gr.Button("Analyze Now", elem_classes="primary-btn")

                        gr.HTML('<div class="examples-title">Examples</div>')
                        ex1 = gr.Button("Should I invest in Apple?", elem_classes="example-btn")
                        ex2 = gr.Button("Should I invest in Tesla?", elem_classes="example-btn")
                        ex3 = gr.Button("Google market trend", elem_classes="example-btn")
                        ex4 = gr.Button("Amazon growth analysis", elem_classes="example-btn")

    ex1.click(fn=lambda: "Should I invest in Apple?", outputs=user_input)
    ex2.click(fn=lambda: "Should I invest in Tesla?", outputs=user_input)
    ex3.click(fn=lambda: "Google market trend", outputs=user_input)
    ex4.click(fn=lambda: "Amazon growth analysis", outputs=user_input)

    submit_btn.click(
        fn=chat,
        inputs=[user_input, history_state],
        outputs=[output_text, output_chart, history_html, history_state]
    )

demo.launch()