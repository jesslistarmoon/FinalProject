import sqlite3
import json

def insert_data():
    conn = sqlite3.connect("travel_weather.db")
    cursor = conn.cursor()

    with open("data.json", "r") as f:
        data = json.load(f)

    inserted_count = 0
    for entry in data["travel"]:
        cursor.execute("INSERT OR IGNORE INTO locations (latitude, longitude) VALUES (?, ?)",
                       (entry["latitude"], entry["longitude"]))
        cursor.execute("SELECT id FROM locations WHERE latitude = ? AND longitude = ?",
                       (entry["latitude"], entry["longitude"]))
        location_id = cursor.fetchone()[0]
