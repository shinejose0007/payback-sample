import sqlite3
import os
import pandas as pd

DB_PATH = os.environ.get('FEATURE_STORE_DB', 'feature_store.db')

def ensure_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS features (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT,
                    ds TEXT,
                    lag_1 REAL,
                    lag_7 REAL,
                    rolling_mean_7 REAL,
                    exog REAL,
                    target REAL
                )''')
    conn.commit()
    conn.close()

def write_features(df: pd.DataFrame):
    ensure_table()
    conn = sqlite3.connect(DB_PATH)
    df[['ds','lag_1','lag_7','rolling_mean_7','exog','target']].to_sql('features', conn, if_exists='append', index=False)
    conn.close()

def read_recent(n=10):
    ensure_table()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM features ORDER BY id DESC LIMIT {n}", conn)
    conn.close()
    return df
