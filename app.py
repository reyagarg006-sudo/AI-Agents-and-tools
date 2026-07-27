import streamlit as st
from agent import handle_query
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pulse Agent",
    page_icon="◆",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Manrope:wght@300;400;500;600;700&display=swap');

:root {
    --bg:        #1c2128;
    --bg-deep:   #161b22;
    --bg-card:   #212830;
    --border:    #2d3742;
    --border-em: #3d4f5e;
    --em:        #10b981;
    --em-glow:   rgba(16,185,129,0.12);
    --text:      #d4dce6;
    --text-muted:#5e7280;
    --text-dim:  #3a4f5e;
    --slate:     #8ba3b8;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-deep) !important;
    color: var(--text) !important;
    font-family: 'Manrope', sans-serif !important;
}

/* Hide ALL Streamlit chrome + sidebar entirely */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"]         { display: none !important; }
[data-testid="stSidebar"]         { display: none !important; }
[data-testid="collapsedControl"]  { display: none !important; }

.block-container {
    padding: 2.5rem 2rem !important;
    max-width: 820px !important;
}

/* ── Top bar ── */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.75rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--border);
}
.topbar-stats { display: flex; gap: 1.5rem; }
.topbar-stat  { text-align: right; }
.topbar-stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: var(--em);
    font-weight: 700;
    line-height: 1;
}
.topbar-stat-lbl {
    font-size: 0.66rem;
    color: var(--text-dim);
    letter-spacing: 0.09em;
    text-transform: uppercase;
    font-weight: 600;
    margin-top: 2px;
}

/* ── Hero ── */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.3rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: var(--text);
    margin: 0 0 0.1rem 0;
    line-height: 1.15;
}
.hero-title .em { color: var(--em); }
.hero-sub {
    color: var(--text-muted);
    font-size: 0.87rem;
    font-weight: 400;
    letter-spacing: 0.015em;
    margin: 0;
}

/* ── Pills ── */
.pills-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-bottom: 1.5rem;
}
.pill {
    background: transparent;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.26rem 0.72rem;
    font-size: 0.72rem;
    color: var(--text-muted);
    font-weight: 500;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ── Examples label ── */
.examples-label {
    font-size: 0.67rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-dim);
    font-weight: 700;
    margin-bottom: 0.5rem;
}

/* ── Input ── */
[data-testid="stTextInput"] > div > div > input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
[data-testid="stTextInput"] > div > div > input:focus {
    border-color: var(--em) !important;
    box-shadow: 0 0 0 3px var(--em-glow) !important;
    outline: none !important;
}
[data-testid="stTextInput"] > div > div > input::placeholder { color: var(--text-dim) !important; }

/* ── Buttons (all) ── */
.stButton > button {
    background: var(--em) !important;
    color: #0a1a10 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.87rem !important;
    letter-spacing: 0.02em !important;
    padding: 0.55rem 1rem !important;
    transition: background 0.15s ease, transform 0.1s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover { background: #0ea572 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* Ghost variant for example + clear buttons */
div[data-testid="column"] .stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text-muted) !important;
    font-weight: 500 !important;
    font-size: 0.8rem !important;
}
div[data-testid="column"] .stButton > button:hover {
    border-color: var(--em) !important;
    color: var(--em) !important;
}

/* ── Result card ── */
.result-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 2px solid var(--em);
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    margin: 1.25rem 0;
    animation: slideIn 0.3s ease;
}
@keyframes slideIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-label {
    font-size: 0.67rem;
    color: var(--em);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 0.75rem;
}
.result-line {
    color: var(--text);
    font-size: 0.91rem;
    line-height: 1.65;
    margin: 0.2rem 0;
}

/* ── Chat bubbles ── */
.chat-item {
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
    margin-bottom: 1.5rem;
    animation: slideIn 0.25s ease;
}
.chat-meta {
    font-size: 0.67rem;
    color: var(--text-dim);
    letter-spacing: 0.07em;
    text-transform: uppercase;
    font-weight: 600;
}
.chat-q {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px 8px 8px 2px;
    padding: 0.7rem 1rem;
    color: var(--slate);
    font-size: 0.9rem;
    max-width: 78%;
    align-self: flex-start;
    line-height: 1.5;
}
.chat-a {
    background: var(--bg);
    border: 1px solid var(--border-em);
    border-left: 2px solid var(--em);
    border-radius: 8px 8px 2px 8px;
    padding: 0.7rem 1rem;
    color: var(--text);
    font-size: 0.9rem;
    max-width: 88%;
    align-self: flex-end;
    line-height: 1.55;
}
.chat-a p { margin: 0.2rem 0; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
[data-testid="stExpander"] summary {
    color: var(--slate) !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 0.87rem !important;
}

[data-testid="stSpinner"] { color: var(--em) !important; }
[data-testid="stAlert"]   { border-radius: 8px !important; font-size: 0.87rem !important; }
hr { border-color: var(--border) !important; margin: 1.75rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ───────────────────────────────────────────────────────────────
if "history"       not in st.session_state: st.session_state.history       = []
if "total_queries" not in st.session_state: st.session_state.total_queries = 0
if "prefill"       not in st.session_state: st.session_state.prefill       = ""

# ── Top bar (title + live stats) ───────────────────────────────────────────────
st.markdown(f"""
<div class='topbar'>
  <div>
    <div class='hero-title'>Pulse <span class='em'>Agent</span></div>
    <div class='hero-sub'>Intelligent assistant — weather, currency, search &amp; maps.</div>
  </div>
  <div class='topbar-stats'>
    <div class='topbar-stat'>
      <div class='topbar-stat-num'>{st.session_state.total_queries}</div>
      <div class='topbar-stat-lbl'>Queries</div>
    </div>
    <div class='topbar-stat'>
      <div class='topbar-stat-num'>{len(st.session_state.history)}</div>
      <div class='topbar-stat-lbl'>Saved</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Capability pills ───────────────────────────────────────────────────────────
st.markdown("""
<div class='pills-row'>
  <div class='pill'>🌤️ Weather</div>
  <div class='pill'>💱 Currency</div>
  <div class='pill'>🔍 Search</div>
  <div class='pill'>📍 Distance</div>
</div>
""", unsafe_allow_html=True)

# ── Quick example buttons ──────────────────────────────────────────────────────
st.markdown("<div class='examples-label'>Quick examples</div>", unsafe_allow_html=True)
examples = ["Weather in Mumbai?", "500 EUR to INR", "Delhi → Bangalore distance", "Latest AI news"]
ex_cols  = st.columns(len(examples))
for col, ex in zip(ex_cols, examples):
    with col:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state.prefill = ex
            st.rerun()

st.markdown("<div style='margin-top:1.1rem'></div>", unsafe_allow_html=True)

# ── Input row ──────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    user_query = st.text_input(
        "query",
        value=st.session_state.prefill,
        placeholder="Ask me anything…   e.g. What's the weather in Delhi?",
        label_visibility="collapsed",
        key="query_input",
    )
with col_btn:
    submit = st.button("Ask →", use_container_width=True, key="ask_btn")

st.markdown(
    "<small style='color:#3a4f5e'>Press "
    "<kbd style='background:#212830;border:1px solid #2d3742;border-radius:4px;"
    "padding:1px 5px;font-size:0.68rem'>Enter</kbd> or click <b>Ask →</b></small>",
    unsafe_allow_html=True,
)

# Clear prefill once consumed
if st.session_state.prefill:
    st.session_state.prefill = ""

# ── Process ────────────────────────────────────────────────────────────────────
if submit and user_query.strip():
    with st.spinner("Thinking…"):
        try:
            result = handle_query(user_query)
            st.session_state.total_queries += 1
            st.session_state.history.append({
                "query":     user_query,
                "result":    result,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "date":      datetime.now().strftime("%b %d"),
            })
            lines      = [l for l in result.split("\n") if l.strip()]
            lines_html = "".join(f"<div class='result-line'>▸ {l}</div>" for l in lines)
            st.markdown(f"""
            <div class='result-card'>
              <div class='result-label'>◆ Result</div>
              {lines_html}
            </div>""", unsafe_allow_html=True)
            st.success("Query answered successfully!")
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

elif submit:
    st.warning("Please enter a query first.")

# ── History ────────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("---")
    hc1, hc2 = st.columns([4, 1])
    with hc1:
        st.markdown("### Conversation History")
    with hc2:
        if st.button("Clear all", key="clear_btn", use_container_width=True):
            st.session_state.history       = []
            st.session_state.total_queries = 0
            st.rerun()

    for item in reversed(st.session_state.history):
        lines       = [l for l in item["result"].split("\n") if l.strip()]
        answer_html = "".join(f"<p>▸ {l}</p>" for l in lines)
        st.markdown(f"""
        <div class='chat-item'>
          <div class='chat-meta'>🕐 {item['date']} · {item['timestamp']}</div>
          <div class='chat-q'>🧑 {item['query']}</div>
          <div class='chat-a'>◆ {answer_html}</div>
        </div>""", unsafe_allow_html=True)

    with st.expander("📋 View as plain text"):
        for item in reversed(st.session_state.history):
            st.markdown(f"**{item['timestamp']}** — {item['query']}")
            st.code(item["result"], language="")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#2d3742;font-size:0.7rem;"
    "font-family:Manrope,sans-serif;letter-spacing:0.1em;text-transform:uppercase'>"
    "Pulse Agent · Powered by Google Generative AI · Weather · Currency · Search · Maps"
    "</p>",
    unsafe_allow_html=True,
)