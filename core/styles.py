import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    :root{--gold:#C9A962;--gold2:#E7CB82;--panel:#171A1F;--line:#2A3038;--muted:#A8AFB8;--green:#3BC47D;--red:#F06A6A;--amber:#F4B860;}
    html,body,[data-testid='stAppViewContainer']{direction:rtl;text-align:right;}
    [data-testid='stSidebar']{direction:rtl;border-left:1px solid var(--line);}
    .block-container{max-width:1500px;padding-top:1.2rem;padding-bottom:3rem;}
    .hero{background:radial-gradient(circle at 92% 8%,rgba(201,169,98,.20),transparent 30%),linear-gradient(125deg,#111316 0%,#1A1E23 55%,#2B261D 100%);border:1px solid rgba(201,169,98,.45);border-radius:24px;padding:28px 30px;margin-bottom:18px;box-shadow:0 14px 40px rgba(0,0,0,.28);}
    .hero h1{font-size:2.3rem;margin:0 0 8px;color:#fff}.hero p{margin:0;color:#D8D1C1}.gold{color:var(--gold2)}
    .kpi{background:linear-gradient(180deg,#1C2026,#16191E);border:1px solid var(--line);border-radius:16px;padding:16px;min-height:112px;}
    .kpi-label{color:var(--muted);font-size:.78rem;margin-bottom:7px}.kpi-value{font-size:1.72rem;font-weight:900;color:#fff}.kpi-note{color:#8D96A1;font-size:.74rem;margin-top:5px}
    .callout-good{border-right:4px solid var(--green);background:rgba(59,196,125,.08);border-radius:12px;padding:12px 14px}
    .callout-warn{border-right:4px solid var(--amber);background:rgba(244,184,96,.08);border-radius:12px;padding:12px 14px}
    .callout-risk{border-right:4px solid var(--red);background:rgba(240,106,106,.08);border-radius:12px;padding:12px 14px}
    [data-testid='stMetric']{background:#171A1F;border:1px solid var(--line);padding:14px;border-radius:14px}
    .stButton>button{border-radius:12px;border:1px solid rgba(201,169,98,.5);font-weight:800}
    </style>
    """, unsafe_allow_html=True)
