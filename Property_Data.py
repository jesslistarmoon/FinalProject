import requests
import sqlite3
from collections import defaultdict

DB_PATH = "./FinalProjectDB.db"
NYPD_API_URL = "https://data.cityofnewyork.us/resource/8y4t-faws.json"

boroughCodeToName = {
    0: "UNKNOWN",
    1: "MANHATTAN",
    2: "BRONX",
    3: "BROOKLYN",
    4: "QUEENS",
    5: "STATEN ISLAND"
}

def fetch_property_data(limit=100):
    """Fetch crime data from NYC Open Data (NYPD API)"""
    params = {
        "$limit": limit,
        "$where": "BORO IS NOT NULL AND PYMKTTOT IS NOT NULL",
        "$select": "PARID, BORO, PYMKTTOT, ZIP_CODE"
    }

    response = requests.get(NYPD_API_URL, params=params)
    response.raise_for_status()
    return response.json()

def store_property_data(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    boroughCount = defaultdict(int)
    count = 0
    for entry in data:
        if count == 25:
            break
        try:
            property_id = entry.get("PARID", None)
            if property_id is None:
                continue

            boroughCode = int(entry.get("BORO", 0))
            if boroughCount[boroughCode] == 5:
                continue
            borough = boroughCodeToName[boroughCode]

            zipcode = entry.get("ZIP_CODE", "UNKNOWN")

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

            market_value = entry.get("PYMKTTOT", None)
            if market_value is None:
                continue
            market_value = int(market_value)
            if market_value == 0:
                continue

            cur.execute("SELECT 1 FROM properties WHERE id = ?", (property_id,))
            if cur.fetchone() is not None:
                continue
            cur.execute("""
                INSERT INTO properties
                (id, market_value, borough_id, zipcode_id)
                VALUES (?, ?, ?, ?)
            """, (
                property_id, market_value, borough_id, zipcode_id
            ))
            print("Stored", property_id)
            count+=1
            boroughCount[boroughCode]+=1


        except Exception as e:
            print("Skipping entry due to error:", e)
            raise e

    print(boroughCount)
    conn.commit()
    conn.close()
    return

if __name__ == "__main__":
    print("Fetching NY Property Data...")
    property_data = fetch_property_data(limit=200000)
    print(len(property_data))
    store_property_data(property_data)
    print("Stored records successfully.")
