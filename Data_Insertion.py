import sqlite3
from collections import defaultdict

DB_PATH = "./FinalProjectDB.db"

def calculate_borough_averages(output_txt="summary_results.txt"):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Join across 3 tables: coordinates + property value + crime
    query = '''
        SELECT
            b.id AS borough_id,
            b.borough_name,
            c.id AS collision_id,
            p.market_value AS property_market_value
        FROM boroughs b
        JOIN collisions c ON b.id = c.borough_id
        JOIN properties p ON b.id = p.borough_id
        ORDER BY b.id;
    '''
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    boroughCollisions = defaultdict(list)
    boroughPropertyValue = defaultdict(list)

    for _, borough, collision_id, market_value in rows:
        boroughCollisions[borough].append(collision_id)
        boroughPropertyValue[borough].append(market_value)


    results = []
    for borough in boroughCollisions:
        shareofTotalCollisions = (len(boroughCollisions[borough])/len(rows))
        averageMarketValue = sum(boroughPropertyValue[borough])/len(boroughPropertyValue[borough])
        results.append([borough, averageMarketValue, shareofTotalCollisions])

    # Write to file
    with open(output_txt, "w") as f:
        f.write(f"{'Borough':<15} | {'Avg Market Value ($)':>22} | {'Share of Total Collisions (%)':>28}\n")
        f.write(f"{'-' * 16}|{'-' * 24}|{'-' * 29}\n")
        for r in results:
            f.write(f"{r[0]:<15} | ${r[1]:>21,.2f} | {r[2] * 100:>27.2f}%\n")

    print(f"Results written to {output_txt}")

# Example usage
if __name__ == "__main__":
    summary = fetch_summary_data()
