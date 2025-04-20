import requests
import sqlite3

DB_PATH = "./FinalProjectDB.db"
PARK_API_URL = "https://data.cityofnewyork.us/resource/enfh-gkve.json"

def fetch_park_data(limit=100):
    """Fetch crime data from NYC Open Data (NYPD API)"""
    params = {
        "$limit": limit,
        "$where": "borough IS NOT NULL"
    }

    response = requests.get(PARK_API_URL, params=params)
    response.raise_for_status()
    return response.json()

boroughCodeToName = {
    "UNKNOWN": "UNKNOWN",
    "M": "MANHATTAN",
    "X": "BRONX",
    "B": "BROOKLYN",
    "Q": "QUEENS",
    "R": "STATEN ISLAND"
}

def store_park_data(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    count = 0
    for entry in data:
        if count == 25:
            break
        try:
            id = entry.get("omppropid", None)
            if id is None:
                continue
            borough = entry.get("borough", "UNKNOWN")
            borough = boroughCodeToName[borough]

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

            cur.execute("SELECT 1 FROM parks WHERE id = ?", (id,))
            if cur.fetchone() is not None:
                continue
            cur.execute("""
                INSERT INTO parks
                (id, borough_id)
                VALUES (?, ?)
            """, (
                id, borough_id
            ))
            print("Stored", id)
            count+=1

        except Exception as e:
            print("Skipping entry due to error:", e)
            continue

    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Fetching Park Data...")
    park_data = fetch_park_data(limit=100000)
    store_park_data(park_data)
    print("Stored records successfully.")
