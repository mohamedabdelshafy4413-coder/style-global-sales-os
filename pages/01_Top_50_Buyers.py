from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from html import unescape
from urllib.parse import urlparse, urljoin

import pandas as pd
import requests
import streamlit as st

from core.database import connect, query_df

st.set_page_config(page_title="Top 50 Buyers | STYLE", page_icon="🎯", layout="wide")

st.markdown("""
<style>
html, body, [data-testid='stAppViewContainer']{direction:rtl;text-align:right}
.block-container{max-width:1550px;padding-top:1.2rem}
.hero{background:linear-gradient(125deg,#111316,#1d2228 60%,#332b1d);border:1px solid #695b36;border-radius:22px;padding:24px 28px;margin-bottom:16px}
.hero h1{margin:0;color:#fff}.hero p{color:#d9d0bd;margin:.45rem 0 0}.gold{color:#e4c879}
.good{border-right:4px solid #45be7b;background:#173126;border-radius:12px;padding:12px 14px}
.warn{border-right:4px solid #e4b55d;background:#342a17;border-radius:12px;padding:12px 14px}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='hero'>
<h1>STYLE <span class='gold'>Top 50 Buyer Intelligence</span></h1>
<p>أقوى المستوردين والموزعين المحتملين → بيانات التواصل العامة → فرصة الشراء → ترتيب الأولوية</p>
</div>
""", unsafe_allow_html=True)

DEFAULT_MATERIALS = ["Galala Light", "Sunny Light", "Meli Brown", "Meli Grey", "Zafarana Flower"]

BUYER_SCHEMA = """
CREATE TABLE IF NOT EXISTS buyer_intelligence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    country TEXT,
    materials TEXT,
    website TEXT,
    email TEXT,
    whatsapp TEXT,
    phone TEXT,
    contact_name TEXT,
    contact_role TEXT,
    importer_signal REAL DEFAULT 50,
    buyer_scale REAL DEFAULT 50,
    material_fit REAL DEFAULT 50,
    repeat_potential REAL DEFAULT 50,
    project_signal REAL DEFAULT 50,
    contact_quality REAL DEFAULT 50,
    source_confidence REAL DEFAULT 50,
    opportunity_score REAL DEFAULT 0,
    opportunity_class TEXT,
    purchase_opportunity TEXT,
    why_ranked TEXT,
    evidence_url TEXT,
    evidence_summary TEXT,
    source_status TEXT DEFAULT 'RESEARCH',
    last_verified TEXT
)
"""
with connect() as conn:
    conn.execute(BUYER_SCHEMA)

EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
PHONE_RE = re.compile(r"(?:\+?\d[\d\s().-]{7,}\d)")
WA_RE = re.compile(r"(?:wa\.me/|api\.whatsapp\.com/send\?phone=)(\+?\d+)", re.I)
BLOCKED = {"linkedin.com","facebook.com","instagram.com","youtube.com","pinterest.com","wikipedia.org","x.com","twitter.com","google.com","bing.com"}


def secret(name: str) -> str:
    try:
        value = st.secrets.get(name, "")
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name, "")


def domain_of(url: str) -> str:
    try:
        host = urlparse(url if "://" in url else "https://" + url).netloc.lower().split(":")[0]
        return host[4:] if host.startswith("www.") else host
    except Exception:
        return ""


def is_company_url(url: str) -> bool:
    d = domain_of(url)
    return bool(d) and not any(d == b or d.endswith("." + b) for b in BLOCKED)


def clean_html(html: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def safe_get(url: str):
    try:
        return requests.get(url, timeout=7, headers={"User-Agent":"Mozilla/5.0 STYLEGlobalSalesOS/1.0"}, allow_redirects=True)
    except Exception:
        return None


def public_contacts(website: str) -> dict:
    out = {"email":"", "whatsapp":"", "phone":""}
    if not website:
        return out
    parsed = urlparse(website if "://" in website else "https://" + website)
    home = f"{parsed.scheme or 'https'}://{parsed.netloc or parsed.path}".rstrip("/")
    pages = [home, urljoin(home + "/", "contact"), urljoin(home + "/", "contact-us"), urljoin(home + "/", "about-us")]
    emails, phones, whats = [], [], []
    for url in pages[:4]:
        r = safe_get(url)
        if not r or r.status_code >= 400 or not r.text:
            continue
        raw = r.text[:600000]
        text = clean_html(raw)
        for e in EMAIL_RE.findall(raw + " " + text):
            e = e.lower().strip(".,;:()[]<>")
            if any(x in e for x in ["example.com","sentry.io","wixpress.com"]):
                continue
            if e not in emails:
                emails.append(e)
        for w in WA_RE.findall(raw):
            w = "+" + re.sub(r"\D", "", w)
            if len(w) >= 9 and w not in whats:
                whats.append(w)
        lower = raw.lower()
        for m in re.finditer("whatsapp", lower):
            window = raw[max(0,m.start()-150):m.end()+220]
            for ph in PHONE_RE.findall(window):
                clean = re.sub(r"[^\d+]", "", ph)
                if 8 <= len(re.sub(r"\D", "", clean)) <= 16 and clean not in whats:
                    whats.append(clean)
        for ph in PHONE_RE.findall(text):
            clean = re.sub(r"[^\d+]", "", ph)
            if 8 <= len(re.sub(r"\D", "", clean)) <= 16 and clean not in phones:
                phones.append(clean)
    out["email"] = emails[0] if emails else ""
    out["whatsapp"] = whats[0] if whats else ""
    out["phone"] = phones[0] if phones else ""
    return out


def serper_search(api_key: str, query: str, num: int = 20):
    r = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY":api_key,"Content-Type":"application/json"},
        json={"q":query,"num":min(max(int(num),10),100)},
        timeout=20,
    )
    r.raise_for_status()
    return r.json().get("organic", []) or []


def keyword_score(text: str, words: list[str]) -> int:
    t = (text or "").lower()
    hits = sum(1 for w in words if w.lower() in t)
    return min(100, 35 + hits * 11)


def classify(score: float) -> str:
    if score >= 90: return "GOLDEN"
    if score >= 80: return "A-CLASS"
    if score >= 70: return "HIGH POTENTIAL"
    if score >= 60: return "MEDIUM"
    return "RESEARCH"


def score_row(r: dict) -> float:
    return round(
        r["importer_signal"]*.25 + r["buyer_scale"]*.20 + r["material_fit"]*.15 +
        r["repeat_potential"]*.10 + r["project_signal"]*.10 + r["contact_quality"]*.08 +
        r["source_confidence"]*.12,
        1,
    )


def discover_country(country: str, materials: list[str], api_key: str, limit: int = 12):
    material_query = " OR ".join(f'\"{m}\"' for m in materials)
    queries = [
        f'({material_query}) marble granite importer distributor wholesaler {country}',
        f'natural stone importer distributor fabricator warehouse {country} Egyptian marble granite',
    ]
    rows, seen = [], set()
    for q in queries:
        for item in serper_search(api_key, q, num=max(limit, 10)):
            url = item.get("link") or ""
            if not is_company_url(url):
                continue
            dom = domain_of(url)
            if dom in seen:
                continue
            seen.add(dom)
            title = (item.get("title") or "").strip()
            snippet = (item.get("snippet") or "").strip()
            text = f"{title} {snippet}"
            matched = [m for m in materials if m.lower() in text.lower()]
            importer = keyword_score(text,["import","importer","distributor","wholesale","stockist","warehouse","natural stone"])
            scale = keyword_score(text,["group","branches","warehouse","projects","commercial","wholesale","distribution","showroom"])
            project = keyword_score(text,["project","contractor","developer","hotel","hospitality","construction","commercial"])
            material_fit = 95 if matched else 70
            company = re.split(r"[-–—|]", title)[0].strip() or dom
            row = {
                "company":company[:140], "country":country, "materials":", ".join(matched or materials),
                "website":url, "email":"", "whatsapp":"", "phone":"", "contact_name":"", "contact_role":"",
                "importer_signal":importer, "buyer_scale":scale, "material_fit":material_fit,
                "repeat_potential":min(95,round((importer+scale)/2)), "project_signal":project,
                "contact_quality":30, "source_confidence":55,
                "evidence_url":url, "evidence_summary":snippet[:450], "source_status":"SEARCH_EVIDENCE_ONLY",
                "last_verified":datetime.now(timezone.utc).date().isoformat(),
            }
            row["opportunity_score"] = score_row(row)
            row["opportunity_class"] = classify(row["opportunity_score"])
            row["purchase_opportunity"] = "High probability of near-term commercial relevance" if row["opportunity_score"] >= 80 else "Requires qualification before outreach"
            row["why_ranked"] = "; ".join(x for x in [
                "import/distribution signal" if importer >= 70 else "",
                "scale/warehouse signal" if scale >= 70 else "",
                "material-specific match" if matched else "",
                "project signal" if project >= 70 else "",
            ] if x) or "requires deeper qualification"
            rows.append(row)
            if len(rows) >= limit:
                return rows
    return rows


def enrich(row: dict) -> dict:
    contacts = public_contacts(row.get("website", ""))
    row.update(contacts)
    found = sum(bool(row.get(k)) for k in ["email","whatsapp","phone"])
    row["contact_quality"] = {0:30,1:58,2:80,3:95}[found]
    if found:
        row["source_confidence"] = max(row["source_confidence"],72)
        row["source_status"] = "PUBLIC_CONTACT_FOUND"
    row["opportunity_score"] = score_row(row)
    row["opportunity_class"] = classify(row["opportunity_score"])
    return row


def save_df(df: pd.DataFrame):
    with connect() as conn:
        df.to_sql("buyer_intelligence", conn, if_exists="replace", index=False)

markets = query_df("SELECT country_en FROM markets ORDER BY id")
default_countries = markets["country_en"].tolist() if not markets.empty else []

c1,c2 = st.columns(2)
with c1:
    materials = st.multiselect("الخمس خامات", DEFAULT_MATERIALS, default=DEFAULT_MATERIALS, max_selections=5)
with c2:
    countries = st.multiselect("العشر دول", default_countries, default=default_countries)

with st.expander("إعداد البحث المباشر", expanded=False):
    st.write("البحث الحقيقي يحتاج Search API. النظام لا يخمّن Email أو WhatsApp.")
    serper_key = st.text_input("SERPER_API_KEY", value=secret("SERPER_API_KEY"), type="password")
    st.caption("خزّن المفتاح في Streamlit → App Settings → Secrets باسم SERPER_API_KEY.")

run = st.button("🔎 ابحث وابنِ Top 50 الآن", type="primary", use_container_width=True)

if run:
    if not serper_key:
        st.error("أضف SERPER_API_KEY أولاً.")
    elif not materials or not countries:
        st.error("اختار الخامات والدول.")
    else:
        with st.spinner("جاري اكتشاف الشركات وترتيبها وفحص بيانات التواصل العامة..."):
            all_rows = []
            try:
                for country in countries:
                    all_rows.extend(discover_country(country, materials, serper_key, limit=12))
                dedup, seen = [], set()
                for row in sorted(all_rows, key=lambda x:x["opportunity_score"], reverse=True):
                    d = domain_of(row["website"])
                    if d in seen: continue
                    seen.add(d); dedup.append(row)
                top = dedup[:50]
                enriched = [enrich(r) for r in top]
                df = pd.DataFrame(enriched).sort_values(["opportunity_score","importer_signal","buyer_scale"], ascending=False).reset_index(drop=True)
                save_df(df)
                st.success(f"تم حفظ {len(df)} Buyer Opportunities مرتبة.")
            except Exception as e:
                st.error(f"فشل البحث: {e}")

try:
    buyers = query_df("SELECT * FROM buyer_intelligence")
except Exception:
    buyers = pd.DataFrame()

if buyers.empty:
    st.info("القائمة فارغة حاليًا. أضف SERPER_API_KEY واضغط زر البحث.")
else:
    buyers = buyers.sort_values(["opportunity_score","importer_signal","buyer_scale"], ascending=False).reset_index(drop=True)
    buyers.insert(0,"rank",range(1,len(buyers)+1))

    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Buyer Opportunities",len(buyers))
    k2.metric("Golden / A-Class",int((buyers["opportunity_score"]>=80).sum()))
    k3.metric("Emails",int(buyers["email"].fillna("").str.len().gt(3).sum()))
    k4.metric("WhatsApp",int(buyers["whatsapp"].fillna("").str.len().gt(5).sum()))

    f1,f2,f3 = st.columns(3)
    fc = f1.multiselect("فلتر الدولة", sorted(buyers["country"].dropna().unique()))
    fm = f2.multiselect("فلتر الخامة", DEFAULT_MATERIALS)
    minimum = f3.slider("Minimum Opportunity",0,100,60)

    view = buyers.copy()
    if fc: view = view[view["country"].isin(fc)]
    if fm:
        pattern = "|".join(re.escape(x) for x in fm)
        view = view[view["materials"].fillna("").str.contains(pattern,case=False,regex=True)]
    view = view[view["opportunity_score"]>=minimum]

    cols = ["rank","company","country","materials","opportunity_score","opportunity_class","purchase_opportunity","email","whatsapp","phone","website","why_ranked","importer_signal","buyer_scale","material_fit","source_confidence","source_status","last_verified"]
    st.dataframe(
        view[cols], use_container_width=True, hide_index=True, height=650,
        column_config={
            "website":st.column_config.LinkColumn("Website",display_text="Open"),
            "opportunity_score":st.column_config.ProgressColumn("Purchase Opportunity",min_value=0,max_value=100,format="%.1f"),
        }
    )

    st.markdown("""
    <div class='warn'><b>مهم:</b> Opportunity Score ترتيب بحث ومبيعات داخلي، وليس إثباتًا لحجم مشتريات فعلي.
    أفضل نسخة احترافية للـranking تربط بيانات الشحن/الجمارك الفعلية (shipment count, volume, supplier origins, recency) بمصدر تجاري موثوق.</div>
    """, unsafe_allow_html=True)

    st.download_button("Download Top 50 CSV", buyers.to_csv(index=False).encode("utf-8-sig"), "style_top50_buyers.csv", "text/csv", use_container_width=True)
