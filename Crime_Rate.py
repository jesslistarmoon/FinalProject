import requests
import sqlite3

DB_PATH = "./FinalProjectDB.db"
NYPD_API_URL = "https://data.cityofnewyork.us/resource/h9gi-nx95.json"

def fetch_nypd_crime_data(limit=100):
    """Fetch crime data from NYC Open Data (NYPD API)"""
    params = {
        "$limit": limit,
        "$where": "zip_code IS NOT NULL AND borough IS NOT NULL"
    }

    response = requests.get(NYPD_API_URL, params=params)
    response.raise_for_status()
    return response.json()

def store_crime_data(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    count = 0
    for entry in data:
        if count == 25:
            break
        try:
            collision_id = entry.get("collision_id", None)
            if collision_id is None:
                continue
            borough = entry.get("borough", "UNKNOWN")
            zipcode = entry.get("zip_code", "UNKNOWN")

            cur.execute("SELECT id FROM boroughs WHERE borough_name = ?", (borough,))
            rows = cur.fetchone()
            if rows is None:
                # print(borough, "not in boroughs table, creating...")
                cur.execute("""
                    INSERT INTO boroughs
                    (borough_name)
                    VALUES (?)
                """, (
                    borough,
                ))
                borough_id = cur.lastrowid
            else:
                borough_id = rows[0]

            cur.execute("SELECT id FROM zipcodes WHERE zipcode = ?", (zipcode,))
            rows = cur.fetchone()
            if rows is None:
                # print(zipcode, "not in zipcodes table, creating...")
                cur.execute("""
                    INSERT INTO zipcodes
                    (zipcode)
                    VALUES (?)
                """, (
                    zipcode,
                ))
                zipcode_id = cur.lastrowid
            else:
                zipcode_id = rows[0]

            cur.execute("SELECT 1 FROM collisions WHERE id = ?", (collision_id,))
            if cur.fetchone() is not None:
                continue
            cur.execute("""
                INSERT INTO collisions
                (id, borough_id, zipcode_id)
                VALUES (?, ?, ?)
            """, (
                collision_id, borough_id, zipcode_id
            ))
            print("Stored", collision_id)
            count+=1


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
