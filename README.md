# STYLE Global Sales OS

Arabic-first Streamlit application for international B2B export sales of Style for Marble & Granite.

## Core modules
- Executive Command Center
- Top 10 Markets
- Golden 5
- Country Intelligence
- Golden Accounts
- 72-Hour Opportunities
- Sales Pipeline
- RFQ Manager
- Country-specific Email Campaign Builder
- Brevo & Deliverability
- CSV / Excel Import & Export

## Run locally
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud
1. Open Streamlit Community Cloud.
2. Select repository `style-global-sales-os`.
3. Branch: `main`.
4. Main file: `app.py`.
5. Preferred slug: `style-global-sales-os`.
6. Deploy.

## Data caution
Seeded markets/accounts are DEMO strategic model data. Replace with verified trade, buyer, customs, freight, RFQ and sales data before commercial reliance.

Never hardcode API keys. Use Streamlit Secrets for Brevo or future integrations.
