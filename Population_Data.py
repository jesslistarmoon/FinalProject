import requests
import sqlite3
from collections import defaultdict

DB_PATH = "./FinalProjectDB.db"
POPULATION_API_URL = "https://data.cityofnewyork.us/resource/xywu-7bv9.json"

def fetch_property_data():
    response = requests.get(POPULATION_API_URL)
    response.raise_for_status()
    return response.json()

def store_property_data(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for entry in data:
        try:
            borough = entry.get("borough", "UNKNOWN")
            if borough == "UNKNOWN" or borough == "NYC Total":
                continue
            borough = borough.lstrip().upper()
            print("Getting", borough, "...")

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

            population = int(entry.get("_2020"))

            cur.execute("SELECT 1 FROM borough_population WHERE id = ?", (borough_id,))
            if cur.fetchone() is not None:
                continue
            cur.execute("""
                INSERT INTO borough_population
                (id, population)
                VALUES (?, ?)
            """, (
                borough_id, population
            ))

        except Exception as e:
            print("Skipping entry due to error:", e)
            raise e

    conn.commit()
    conn.close()
    return

if __name__ == "__main__":
    print("Fetching NY Population Data...")
    population_data = fetch_property_data()
    store_property_data(population_data)
    print("Stored records successfully.")
