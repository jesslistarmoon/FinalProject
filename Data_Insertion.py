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

    cursor.execute('''INSERT INTO travel_data (location_id, destination_latitude, destination_longitude, 
                         travel_time, traffic_impact) 
                         VALUES (?, ?, ?, ?, ?)''',
                       (location_id, entry["destination_latitude"], entry["destination_longitude"],
                        entry["travel_time"], entry["traffic_impact"]))
    inserted_count += 1
    if inserted_count >= 25:
        break

    inserted_count = 0
    for entry in data["weather"]:
        cursor.execute("INSERT OR IGNORE INTO locations (latitude, longitude) VALUES (?, ?)",
                       (entry["latitude"], entry["longitude"]))
        cursor.execute("SELECT id FROM locations WHERE latitude = ? AND longitude = ?",
                       (entry["latitude"], entry["longitude"]))
        location_id = cursor.fetchone()[0]

        cursor.execute('''INSERT INTO weather_data (location_id, temperature, feels_like, humidity, weather_description) 
                         VALUES (?, ?, ?, ?, ?)''',
                       (location_id, entry["temperature"], entry["feels_like"], entry["humidity"], entry["weather_description"]))
        inserted_count += 1
        if inserted_count >= 25:
            break

    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_data()