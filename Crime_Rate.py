import requests
import sqlite3
from datetime import datetime

DB_PATH = "nyc_crime_mobility.db"
NYPD_API_URL = "https://data.cityofnewyork.us/resource/h9gi-nx95.json"

def fetch_nypd_crime_data(limit=100):
    """Fetch crime data from NYC Open Data (NYPD API)"""
    params = {
        "$limit": limit,
        "$where": "cmplnt_fr_dt >= '2023-01-01T00:00:00'",
        "$order": "cmplnt_fr_dt DESC"
    }

    response = requests.get(NYPD_API_URL, params=params)
    response.raise_for_status()
    return response.json()

def extract_zip_code(lat, lon):
    """Optional: you could reverse geocode this later using Google Maps if zip not provided"""
    return None  # Placeholder for future logic

def store_crime_data(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for entry in data:
        try:
            offense = entry.get("ofns_desc", "UNKNOWN")
            level = entry.get("law_cat_cd", "UNKNOWN")
            borough = entry.get("boro_nm", "UNKNOWN")
            zip_code = entry.get("addr_pct_cd", "UNKNOWN")  # Note: May not be a real zip

            lat = float(entry.get("latitude", 0))
            lng = float(entry.get("longitude", 0))
            occurred_date = entry.get("cmplnt_fr_dt", "UNKNOWN")
            timestamp = datetime.utcnow().isoformat()

            if lat == 0 or lng == 0:
                continue

            cur.execute("""
                INSERT INTO crime_reports 
                (zip_code, borough, offense, level, latitude, longitude, occurred_date, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                zip_code, borough, offense, level, lat, lng, occurred_date, timestamp
            ))

        except Exception as e:
            print("Skipping entry due to error:", e)
            continue

    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Fetching NYPD Crime Data...")
    crime_data = fetch_nypd_crime_data(limit=100)
    store_crime_data(crime_data)
    print("Stored records successfully.")


