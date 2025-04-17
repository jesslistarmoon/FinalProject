import requests
import sqlite3
from datetime import datetime
import os

DB_PATH = "project_data.db"
NYPD_API_URL = "https://data.cityofnewyork.us/resource/h9gi-nx95.json"

def fetch_nypd_crime_data(limit=25, offset=0):
    params = {
        "$limit": limit,
        "$offset": offset,
        "$where": "cmplnt_fr_dt >= '2023-01-01T00:00:00'",
        "$order": "cmplnt_fr_dt DESC"
    }
    response = requests.get(NYPD_API_URL, params=params)
    response.raise_for_status()
    return response.json()

def setup_crime_table(cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS crime_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zip_code INTEGER,
            crime_count INTEGER
        )
    ''')

def store_crime_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    setup_crime_table(cur)

    existing_zips = set(row[0] for row in cur.execute("SELECT zip_code FROM crime_data").fetchall())
    zip_counts = {}
    offset = 0

    while len(zip_counts) < 100:
        data = fetch_nypd_crime_data(limit=25, offset=offset)
        offset += 25

        for entry in data:
            zip_code = entry.get("addr_pct_cd")
            if zip_code and zip_code.isdigit():
                zip_code = int(zip_code)
                if zip_code in existing_zips:
                    continue
                zip_counts[zip_code] = zip_counts.get(zip_code, 0) + 1

        if offset > 2000:
            break

    for zip_code, count in zip_counts.items():
        cur.execute("INSERT INTO crime_data (zip_code, crime_count) VALUES (?, ?)", (zip_code, count))

    conn.commit()
    conn.close()
    print("✅ Crime data stored.")

if __name__ == "__main__":
    print("Fetching NYPD Crime Data...")
    store_crime_data()
    print("Stored records successfully.")
