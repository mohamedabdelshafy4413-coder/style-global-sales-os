import sqlite3
from contextlib import contextmanager
import pandas as pd
from .config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS markets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_ar TEXT NOT NULL,
    country_en TEXT NOT NULL,
    region TEXT,
    import_demand REAL DEFAULT 50,
    import_growth REAL DEFAULT 50,
    product_fit REAL DEFAULT 50,
    buyer_quality REAL DEFAULT 50,
    deal_potential REAL DEFAULT 50,
    construction REAL DEFAULT 50,
    repeat_potential REAL DEFAULT 50,
    logistics REAL DEFAULT 50,
    market_access REAL DEFAULT 50,
    competition_advantage REAL DEFAULT 50,
    fast_response REAL DEFAULT 50,
    language TEXT,
    best_buyer TEXT,
    entry_point TEXT,
    product_focus TEXT,
    business_mindset TEXT,
    customs_note TEXT,
    risk_note TEXT,
    send_window TEXT,
    evidence_status TEXT DEFAULT 'DEMO'
);

CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    country TEXT NOT NULL,
    account_type TEXT,
    website TEXT,
    decision_maker TEXT,
    title TEXT,
    email TEXT,
    linkedin TEXT,
    import_activity REAL DEFAULT 50,
    purchasing_power REAL DEFAULT 50,
    product_fit REAL DEFAULT 50,
    repeat_potential REAL DEFAULT 50,
    project_activity REAL DEFAULT 50,
    decision_access REAL DEFAULT 50,
    financial_strength REAL DEFAULT 50,
    buying_signal REAL DEFAULT 50,
    potential_usd REAL DEFAULT 0,
    stage TEXT DEFAULT 'Target',
    last_contact TEXT,
    next_action TEXT,
    next_date TEXT,
    data_status TEXT DEFAULT 'DEMO'
);

CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    company TEXT,
    country TEXT,
    stage TEXT,
    value_usd REAL DEFAULT 0,
    probability REAL DEFAULT .1,
    expected_close TEXT,
    signal TEXT,
    next_action TEXT,
    next_date TEXT
);

CREATE TABLE IF NOT EXISTS rfqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer TEXT NOT NULL,
    country TEXT,
    stone TEXT,
    format TEXT,
    thickness TEXT,
    finish TEXT,
    dimensions TEXT,
    quantity TEXT,
    destination_port TEXT,
    incoterm TEXT,
    requested_price REAL,
    offered_price REAL,
    estimated_margin_pct REAL,
    potential_usd REAL DEFAULT 0,
    status TEXT DEFAULT 'New',
    deadline TEXT,
    owner TEXT,
    next_action TEXT
);
"""

@contextmanager
def connect():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with connect() as conn:
        conn.executescript(SCHEMA)

def query_df(sql, params=()):
    with connect() as conn:
        return pd.read_sql_query(sql, conn, params=params)

def execute(sql, params=()):
    with connect() as conn:
        cur = conn.execute(sql, params)
        return cur.lastrowid

def replace_table(df: pd.DataFrame, table: str):
    with connect() as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)
