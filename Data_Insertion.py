import os
import sqlite3

def calculate_borough_averages(db_filename, output_txt="summary_results.txt"):
    path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(path, db_filename)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Join across 3 tables: coordinates + property value + crime
    query = '''
    SELECT z.zip, z.lat, z.long, n.avg_mv, c.crime_count
    FROM zips_and_coordinates z
    JOIN nycdata n ON z.zip = n.zip_code
    JOIN crime_data c ON z.zip = c.zip_code
    '''
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
