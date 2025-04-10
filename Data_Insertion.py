import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import json

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

    