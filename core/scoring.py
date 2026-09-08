import pandas as pd
from .config import MARKET_WEIGHTS, ACCOUNT_WEIGHTS

def normalize(weights):
    total = sum(max(float(v), 0) for v in weights.values()) or 1
    return {k:max(float(v),0)/total for k,v in weights.items()}

def score_markets(df, weights=None):
    weights = normalize(weights or MARKET_WEIGHTS)
    out = df.copy()
    score = 0
    for col,w in weights.items():
        if col in out.columns:
            score += pd.to_numeric(out[col], errors="coerce").fillna(0) * w
    out["market_score"] = score.round(1)
    out["score_72h"] = (
        out["fast_response"]*.30 + out["buyer_quality"]*.20 +
        out["market_access"]*.15 + out["product_fit"]*.15 +
        out["deal_potential"]*.10 + out["logistics"]*.10
    ).round(1)
    out["score_scale"] = (
        out["deal_potential"]*.25 + out["repeat_potential"]*.20 +
        out["import_demand"]*.15 + out["buyer_quality"]*.15 +
        out["construction"]*.10 + out["product_fit"]*.10 +
        out["market_access"]*.05
    ).round(1)
    def p(v):
        return "ATTACK NOW" if v>=78 else ("BUILD PIPELINE" if v>=65 else "STRATEGIC DEVELOPMENT")
    out["priority"] = out["market_score"].apply(p)
    return out

def score_accounts(df):
    out = df.copy()
    score = 0
    for col,w in ACCOUNT_WEIGHTS.items():
        score += pd.to_numeric(out[col], errors="coerce").fillna(0) * (w/100)
    out["account_score"] = score.round(1)
    def c(v):
        if v>=90: return "GOLDEN"
        if v>=80: return "A-CLASS"
        if v>=65: return "HIGH POTENTIAL"
        if v>=50: return "NURTURE"
        return "LOW PRIORITY"
    out["class"] = out["account_score"].apply(c)
    out["score_72h"] = (
        out["buying_signal"]*.30 + out["decision_access"]*.20 +
        out["project_activity"]*.15 + out["import_activity"]*.15 +
        out["product_fit"]*.10 + out["purchasing_power"]*.10
    ).round(1)
    return out
