import sqlite3
import json

def insert_data():
    conn = sqlite3.connect("travel_weather.db")
    cursor = conn.cursor()

    with open("data.json", "r") as f:
        data = json.load(f)