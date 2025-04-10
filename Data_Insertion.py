import sqlite3
import json
import matplotlib.pyplot as plt

def create_tables():
    conn = sqlite3.connect("travel_weather.db")
    cur = conn.cursor()

# Locations
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Locations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            latitude REAL,
            longitude REAL
        );
    """)

# Travel Times
    cur.execute("""
        CREATE TABLE IF NOT EXISTS TravelTimes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER,
            mode TEXT,
            travel_time INTEGER,
            timestamp TEXT,
            FOREIGN KEY (location_id) REFERENCES Locations(id)
        );
    """)    

 # Weather Conditions
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER,
            temperature REAL,
            humidity REAL,
            condition TEXT,
            timestamp TEXT,
            FOREIGN KEY (location_id) REFERENCES Locations(id)
        );
    """)

    conn.commit()
    conn.close()

def insert_location(name, lat, lon):
    conn = sqlite3.connect("travel_weather.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Locations (name, latitude, longitude)
        VALUES (?, ?, ?);
    """, (name, lat, lon))
    conn.commit()
    conn.close()


def insert_travel_time(location_id, mode, time, timestamp):
    conn = sqlite3.connect("travel_weather.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO TravelTimes (location_id, mode, travel_time, timestamp)
        VALUES (?, ?, ?, ?);
    """, (location_id, mode, time, timestamp))
    conn.commit()
    conn.close()


def insert_weather(location_id, temp, humidity, condition, timestamp):
    conn = sqlite3.connect("travel_weather.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Weather (location_id, temperature, humidity, condition, timestamp)
        VALUES (?, ?, ?, ?, ?);
    """, (location_id, temp, humidity, condition, timestamp))
    conn.commit()
    conn.close()
