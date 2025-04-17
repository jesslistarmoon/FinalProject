import requests
import sqlite3
from datetime import datetime

DB_PATH = "/Users/jiyihong/Desktop/SI206/FinalProject/NYC_Data.db"
NYPD_API_URL = "https://data.cityofnewyork.us/resource/h9gi-nx95.json"

def fetch_nypd_crime_data(limit=200):
    """Fetch crime data from NYC Open Data (NYPD API)"""
    params = {
        "$limit": limit,
        "$where": "location IS NOT NULL"
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

    countInserted = 0
    for entry in data:
        if countInserted == 25:
            break
        try:
            offense = entry.get("ofns_desc", "UNKNOWN")
            level = entry.get("law_cat_cd", "UNKNOWN")
            borough = entry.get("boro_nm", "UNKNOWN")
            zip_code = entry.get("addr_pct_cd", "UNKNOWN")  # Note: May not be a real zip

            lat = float(entry.get("latitude", 0))
            lng = float(entry.get("longitude", 0))
            occurred_date = entry.get("cmplnt_fr_dt", "UNKNOWN")
            timestamp = datetime.utcnow().isoformat()

            # Collision table data
            borough = entry.get("borough", "UNKNOWN")
            zipcode = entry.get("zip_code", "UNKNOWN")
            location = entry.get("location", None)
            if location is None:
                continue
            lat = location["latitude"]
            long = location["longitude"]
            collision_id = entry.get("collision_id", None)
            if collision_id is None:
                continue


            if lat == 0 or lng == 0:
                continue
            
            cur.execute("SELECT 1 FROM collision_data WHERE collision_id = ?", (collision_id,))
            if cur.fetchone():
                continue
            else:
                print("Adding collision")
                cur.execute("""
                    INSERT INTO collision_data 
                    (collision_id, borough, latitude, longitude, zipcode)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    collision_id, borough, lat, long, zipcode
                ))
                countInserted+=1

        except Exception as e:
            print("Skipping entry due to error:", e)
            continue

    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Fetching NYPD Crime Data...")
    crime_data = fetch_nypd_crime_data(100)
    store_crime_data(crime_data)
    print("Stored records successfully.")


