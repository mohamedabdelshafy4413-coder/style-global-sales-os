from __future__ import annotations

from io import BytesIO
import pandas as pd
import streamlit as st
import plotly.express as px

from core.styles import inject_css
from core.database import init_db, query_df, replace_table
from core.seed import seed_demo
from core.scoring import score_markets, score_accounts
from core.config import MARKET_WEIGHTS
from core.email_engine import build_email

st.set_page_config(
    page_title="STYLE Global Sales OS",
    page_icon="🪨",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
init_db()
seed_demo()

def money(v):
    return f"${float(v):,.0f}"

def kpi(label, value, note=""):
    st.markdown(
        f"<div class='kpi'><div class='kpi-label'>{label}</div>"
        f"<div class='kpi-value'>{value}</div><div class='kpi-note'>{note}</div></div>",
        unsafe_allow_html=True
    )

def excel_bytes(df, sheet="Data"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet)
    return output.getvalue()

st.sidebar.markdown("## STYLE GLOBAL SALES OS")
st.sidebar.caption("Arabic Executive Edition")

page = st.sidebar.radio(
    "الوحدات",
    [
        "مركز القيادة التنفيذي",
        "أفضل 10 أسواق",
        "الخمس أسواق الذهبية",
        "ذكاء الدولة",
        "العملاء والحسابات الذهبية",
        "فرص 72 ساعة",
        "Pipeline المبيعات",
        "إدارة RFQ",
        "مصنع حملات الإيميل",
        "Brevo & Deliverability",
        "الاستيراد والتصدير",
    ],
)

st.markdown("""
<div class="hero">
  <h1>STYLE <span class="gold">Global Sales OS</span></h1>
  <p>Market Intelligence → Golden Accounts → RFQ → Quote → Container → Repeat Revenue</p>
</div>
""", unsafe_allow_html=True)

markets_raw = query_df("SELECT * FROM markets")
accounts_raw = query_df("SELECT * FROM accounts")
rfqs = query_df("SELECT * FROM rfqs")
markets = score_markets(markets_raw)
accounts = score_accounts(accounts_raw)

if page == "مركز القيادة التنفيذي":
    pipeline = accounts["potential_usd"].sum() if not accounts.empty else 0
    golden = int((accounts["class"]=="GOLDEN").sum()) if not accounts.empty else 0
    aclass = int((accounts["class"]=="A-CLASS").sum()) if not accounts.empty else 0
    active_rfqs = int(rfqs["status"].isin(["New","Open","Quoting"]).sum()) if not rfqs.empty else 0
    rfq_value = rfqs["potential_usd"].sum() if not rfqs.empty else 0

    cols = st.columns(6)
    cards = [
        ("Potential Pipeline", money(pipeline), "Demo + entered accounts"),
        ("Golden Accounts", golden, "Score ≥ 90"),
        ("A-Class", aclass, "Score 80–89"),
        ("Active RFQs", active_rfqs, "New / Open / Quoting"),
        ("RFQ Value", money(rfq_value), "Open commercial demand"),
        ("Top 72h Market", markets.sort_values("score_72h",ascending=False).iloc[0]["country_en"], "Fast-response lens"),
    ]
    for c, item in zip(cols, cards):
        with c:
            kpi(*item)

    st.markdown("### أقوى الأسواق")
    c1,c2 = st.columns([1.15,1])
    with c1:
        top = markets.sort_values("score_72h",ascending=False).head(5)
        fig = px.bar(top.sort_values("score_72h"),x="score_72h",y="country_en",orientation="h",text="score_72h",labels={"score_72h":"72-Hour Score","country_en":"Market"})
        fig.update_layout(height=360,margin=dict(l=10,r=10,t=20,b=10),showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown("""
        <div class="callout-good"><b>قاعدة الإدارة:</b><br>
        أول 72 ساعة نقيسها بـ <b>Positive Replies + RFQs + Sample Requests + Meetings</b>،
        وليس بوعد غير واقعي بصفقات مضمونة.</div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown("#### Top Golden / A-Class")
        st.dataframe(accounts.sort_values(["account_score","potential_usd"],ascending=False)[["company","country","class","account_score","potential_usd","stage","next_action"]].head(8),use_container_width=True,hide_index=True)

elif page == "أفضل 10 أسواق":
    st.subheader("Market Prioritization Engine")
    st.caption("عدّل الأوزان وشاهد ترتيب الأسواق يتغير فورًا.")
    with st.expander("تعديل أوزان السوق", expanded=False):
        weights = {}
        cols = st.columns(2)
        for i,(k,v) in enumerate(MARKET_WEIGHTS.items()):
            with cols[i%2]:
                weights[k] = st.slider(k.replace("_"," ").title(),0,30,int(v),1)
        markets = score_markets(markets_raw,weights)

    view = markets.sort_values("market_score",ascending=False)
    st.dataframe(view[["country_en","market_score","score_72h","score_scale","priority","best_buyer","entry_point","product_focus","send_window"]],use_container_width=True,hide_index=True)
    fig = px.scatter(view,x="score_72h",y="score_scale",size="deal_potential",color="priority",text="country_en",hover_data=["best_buyer","product_focus"],labels={"score_72h":"Fast Opportunity","score_scale":"12M Scale"})
    fig.update_traces(textposition="top center")
    fig.update_layout(height=560)
    st.plotly_chart(fig,use_container_width=True)

elif page == "الخمس أسواق الذهبية":
    st.subheader("GOLDEN 5")
    mode = st.radio("زاوية القرار",["أسرع فرصة 72 ساعة","أكبر حسابات خلال 12 شهر"],horizontal=True)
    col = "score_72h" if mode.startswith("أسرع") else "score_scale"
    top5 = markets.sort_values(col,ascending=False).head(5)
    for _,r in top5.iterrows():
        with st.expander(f"⭐ {r['country_ar']} / {r['country_en']} — {r[col]}/100", expanded=False):
            a,b,c = st.columns(3)
            with a:
                st.markdown("**أفضل مشتري**"); st.write(r["best_buyer"])
                st.markdown("**نقطة الدخول**"); st.write(r["entry_point"])
            with b:
                st.markdown("**الخامات/العرض**"); st.write(r["product_focus"])
                st.markdown("**Mindset**"); st.write(r["business_mindset"])
            with c:
                st.markdown("**أفضل توقيت اختبار**"); st.write(r["send_window"])
                st.markdown("**Evidence Status**"); st.write(r["evidence_status"])
            st.markdown("**Customs / Rules**"); st.info(r["customs_note"])
            st.markdown("**Main Risk**"); st.warning(r["risk_note"])

elif page == "ذكاء الدولة":
    st.subheader("Country Intelligence")
    selected = st.selectbox("اختر الدولة",markets["country_ar"].tolist())
    r = markets[markets["country_ar"]==selected].iloc[0]
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Market Score",r["market_score"])
    c2.metric("72h Score",r["score_72h"])
    c3.metric("12M Scale",r["score_scale"])
    c4.metric("Language",r["language"])
    t1,t2,t3 = st.tabs(["Commercial","Buyer Mind & Entry","Customs / Risk"])
    with t1:
        st.write("**Best Buyer:**",r["best_buyer"])
        st.write("**Entry Point:**",r["entry_point"])
        st.write("**Product Focus:**",r["product_focus"])
        st.write("**Send Window:**",r["send_window"])
    with t2:
        st.write(r["business_mindset"])
        st.markdown("<div class='callout-warn'>لا تستخدم رسالة واحدة لكل الأسواق. غيّر الـ angle واللغة والـ proof والـ CTA حسب نوع المشتري والدولة.</div>", unsafe_allow_html=True)
    with t3:
        st.write(r["customs_note"])
        st.error(r["risk_note"])
        st.caption("أي تعريفة/جمارك/متطلبات فنية يجب التحقق منها رسميًا قبل التسعير النهائي والشحن.")

elif page == "العملاء والحسابات الذهبية":
    st.subheader("Golden Account Engine")
    f1,f2,f3 = st.columns(3)
    cf = f1.multiselect("الدولة",sorted(accounts["country"].dropna().unique()))
    cl = f2.multiselect("Class",sorted(accounts["class"].dropna().unique()))
    min_score = f3.slider("Minimum Score",0,100,65)
    view = accounts.copy()
    if cf: view = view[view["country"].isin(cf)]
    if cl: view = view[view["class"].isin(cl)]
    view = view[view["account_score"]>=min_score]
    st.dataframe(view.sort_values(["account_score","potential_usd"],ascending=False)[["company","country","account_type","decision_maker","title","account_score","class","score_72h","potential_usd","stage","next_action","next_date","data_status"]],use_container_width=True,hide_index=True)
    st.markdown("### تعديل / إضافة حسابات")
    edited = st.data_editor(accounts_raw,num_rows="dynamic",use_container_width=True,hide_index=True,key="accounts_editor")
    if st.button("حفظ الحسابات"):
        replace_table(edited,"accounts")
        st.success("تم الحفظ. أعد فتح الصفحة لرؤية الـscores الجديدة.")

elif page == "فرص 72 ساعة":
    st.subheader("72-Hour Sales Attack")
    top = accounts.sort_values(["score_72h","potential_usd"],ascending=False).head(15)
    st.dataframe(top[["company","country","account_type","class","score_72h","potential_usd","stage","decision_maker","next_action","next_date"]],use_container_width=True,hide_index=True)
    d1,d2,d3 = st.columns(3)
    with d1:
        st.markdown("#### DAY 1 — Precision Launch"); st.write("اختر 20–50 حسابًا فقط. Verify decision-maker + email. Personalize one commercial line. CTA منخفض الاحتكاك.")
    with d2:
        st.markdown("#### DAY 2 — Signal Follow-up"); st.write("ابدأ بالردود الإيجابية، ثم الحسابات عالية القيمة. أرسل فقط الخامات/التوفر/الداتا المطلوبة.")
    with d3:
        st.markdown("#### DAY 3 — RFQ Acceleration"); st.write("حوّل: Material + Size + Thickness + Quantity + Port إلى RFQ. الرد التجاري في نفس يوم العمل.")

elif page == "Pipeline المبيعات":
    st.subheader("Sales Pipeline")
    opp = query_df("SELECT * FROM opportunities")
    edited = st.data_editor(opp,num_rows="dynamic",use_container_width=True,hide_index=True,key="opp_editor")
    if st.button("حفظ الـPipeline"):
        replace_table(edited,"opportunities"); st.success("تم الحفظ.")
    if not edited.empty:
        tmp = edited.copy()
        tmp["value_usd"] = pd.to_numeric(tmp["value_usd"],errors="coerce").fillna(0)
        tmp["probability"] = pd.to_numeric(tmp["probability"],errors="coerce").fillna(0)
        tmp["weighted_value"] = tmp["value_usd"]*tmp["probability"]
        c1,c2,c3 = st.columns(3)
        c1.metric("Pipeline",money(tmp["value_usd"].sum()))
        c2.metric("Weighted",money(tmp["weighted_value"].sum()))
        c3.metric("Opportunities",len(tmp))
        agg = tmp.groupby("stage",as_index=False)["value_usd"].sum()
        fig = px.funnel(agg,x="value_usd",y="stage")
        st.plotly_chart(fig,use_container_width=True)

elif page == "إدارة RFQ":
    st.subheader("RFQ Manager")
    edited = st.data_editor(rfqs,num_rows="dynamic",use_container_width=True,hide_index=True,key="rfq_editor")
    if st.button("حفظ RFQs"):
        replace_table(edited,"rfqs"); st.success("تم الحفظ.")
    if not edited.empty:
        tmp = edited.copy()
        tmp["potential_usd"] = pd.to_numeric(tmp["potential_usd"],errors="coerce").fillna(0)
        c1,c2,c3 = st.columns(3)
        c1.metric("RFQs",len(tmp)); c2.metric("Potential",money(tmp["potential_usd"].sum())); c3.metric("Open",int(tmp["status"].isin(["New","Open","Quoting"]).sum()))
    st.markdown("<div class='callout-risk'><b>قاعدة:</b> لا ترسل Quote نهائي قبل مراجعة HS code + destination + origin + tariff/VAT + freight + packing + Incoterm.</div>", unsafe_allow_html=True)

elif page == "مصنع حملات الإيميل":
    st.subheader("Country-Specific B2B Email Builder")
    c1,c2 = st.columns(2)
    with c1:
        country = st.selectbox("الدولة",markets["country_en"].tolist())
        persona = st.selectbox("نوع المشتري",["Importer","Distributor","Fabricator","Contractor","Developer","Architect","Procurement"])
        language = st.selectbox("لغة الرسالة",["English","Arabic","French"])
    with c2:
        company = st.text_input("Company")
        contact = st.text_input("Decision Maker")
        product = st.text_input("Hero Product / Offer","Galala / Sunny / Egyptian Granite")
    subject,body = build_email(language,persona,company,contact,product)
    st.markdown("#### Subject"); st.code(subject,language=None)
    st.markdown("#### Email"); st.code(body,language=None)
    market_row = markets[markets["country_en"]==country].iloc[0]
    st.info(f"Recommended test window: {market_row['send_window']} | Buyer mindset: {market_row['business_mindset']}")
    st.caption("Use legitimate B2B contact data and comply with applicable privacy/marketing rules. Do not mass-spam scraped lists.")

elif page == "Brevo & Deliverability":
    st.subheader("Brevo & Email Deliverability")
    st.markdown("""
    ### قبل أول حملة
    1. SPF مضبوط
    2. DKIM مضبوط
    3. DMARC موجود
    4. Email verification
    5. Bounce منخفض
    6. لا تبدأ بآلاف الرسائل
    7. راقب Positive Reply / RFQ / Meeting وليس Open Rate فقط

    ### Pilot Stack
    - Brevo: إرسال + automation حسب الخطة المتاحة في حسابك
    - Hunter / Apollo: بحث عن contacts حسب الحاجة
    - MillionVerifier / ZeroBounce: verification
    - MXToolbox: DNS / blacklist checks
    - Mail-Tester: basic deliverability test
    - Google Postmaster Tools: domain reputation عند توفر volume مناسب
    """)
    st.warning("الأسعار والباقات تتغير. راجع صفحة Brevo الرسمية قبل اتخاذ قرار شراء أو Upgrade.")

elif page == "الاستيراد والتصدير":
    st.subheader("Data Import / Export")
    target = st.selectbox("الجدول",["accounts","rfqs","opportunities"])
    current = query_df(f"SELECT * FROM {target}")
    st.dataframe(current,use_container_width=True,hide_index=True)
    c1,c2 = st.columns(2)
    with c1:
        st.download_button("Download CSV",current.to_csv(index=False).encode("utf-8-sig"),f"{target}.csv","text/csv")
    with c2:
        st.download_button("Download Excel",excel_bytes(current,target[:31]),f"{target}.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    up = st.file_uploader("Upload CSV / Excel",type=["csv","xlsx"])
    if up:
        imported = pd.read_csv(up) if up.name.lower().endswith(".csv") else pd.read_excel(up)
        st.dataframe(imported,use_container_width=True,hide_index=True)
        st.warning("الاستيراد سيستبدل الجدول المختار بالكامل.")
        if st.button("تأكيد الاستيراد"):
            replace_table(imported,target); st.success("تم الاستيراد.")
