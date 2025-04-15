import requests
import sqlite3
import os

# NYC Property API (building data)
PROPERTY_API = 'https://data.cityofnewyork.us/resource/8y4t-faws.json'

def fetch_property_data(zip_code, limit=25):
    """Fetch property data for a specific ZIP code."""
    url = f"{PROPERTY_API}?$limit={limit}&zip_code={zip_code}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"Error fetching data for ZIP {zip_code}: {e}")
        return []

def setup_property_table(cur):
    """Create the table for storing property data."""
    cur.execute('''
        CREATE TABLE IF NOT EXISTS nycdata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zip_code INTEGER,
            avg_mv FLOAT,
            avg_sqft FLOAT
        )
    ''')

def insert_property_data(cur, conn):
    """Loop through ZIP codes and insert property stats per ZIP."""
    cur.execute("SELECT zip FROM zips_and_coordinates")
    zip_rows = cur.fetchall()
    
    for row in zip_rows:
        zip_code = row[0]
        data = fetch_property_data(zip_code)
        
        total_mv = 0
        total_sqft = 0
        count = 0

        for record in data:
            try:
                market_value = int(record.get('curmkttot', 0))
                sqft = int(record.get('gross_sqft', 0))
                total_mv += market_value
                total_sqft += sqft
                count += 1
            except:
                continue  # Skip rows with missing or invalid data

        if count > 0:
            avg_mv = total_mv / count
            avg_sqft = total_sqft / count
        else:
            avg_mv = 0
            avg_sqft = 0

        cur.execute('''
            INSERT INTO nycdata (zip_code, avg_mv, avg_sqft)
            VALUES (?, ?, ?)
        ''', (zip_code, avg_mv, avg_sqft))

    conn.commit()
    print("NYC property data successfully inserted.")

def run_property_pipeline():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/project_data.db')
    cur = conn.cursor()

    setup_property_table(cur)
    insert_property_data(cur, conn)

    conn.close()

if __name__ == "__main__":
    run_property_pipeline()


