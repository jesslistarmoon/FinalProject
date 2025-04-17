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

    # Group data by borough (using zip ranges)
    boroughs = {
        "Manhattan": range(10001, 10283),
        "Bronx": range(10451, 10476),
        "Brooklyn": range(11201, 11257),
        "Queens": range(11001, 11698),
        "Staten Island": range(10301, 10315)
    }

    grouped = {
        "Manhattan": [],
        "Bronx": [],
        "Brooklyn": [],
        "Queens": [],
        "Staten Island": []
    }

    for row in rows:
        zip_code = int(row[0])
        mv = row[3]
        crimes = row[4]
        for boro, zip_range in boroughs.items():
            if zip_code in zip_range:
                grouped[boro].append((mv, crimes))
                break

    results = []
    for boro, values in grouped.items():
        if values:
            total_mv = sum(v[0] for v in values)
            total_crimes = sum(v[1] for v in values)
            count = len(values)
            avg_mv = total_mv / count
            avg_crimes = total_crimes / count
            results.append((boro, round(avg_mv, 2), round(avg_crimes, 2)))
        else:
            results.append((boro, 0, 0))

    # Write to file
    with open(output_txt, "w") as f:
        f.write("Borough | Avg Market Value ($) | Avg Crime Count\n")
        f.write("--------|----------------------|------------------\n")
        for r in results:
            f.write(f"{r[0]:<10} | ${r[1]:<20,.2f} | {r[2]}\n")

    print(f"Results written to {output_txt}")

# Example usage
if __name__ == "__main__":
    calculate_borough_averages("project_data.db")