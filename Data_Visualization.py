import sqlite3
import matplotlib.pyplot as plt
from collections import defaultdict

DB_PATH = "./FinalProjectDB.db"

def fetch_summary_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

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

    return results

def generate_visualizations(summary_data):
    boroughs = [r[0] for r in summary_data]
    avg_mv = [r[1] for r in summary_data]
    totalCollisionShare = [r[2]*100 for r in summary_data]

    # 1. Bar Chart: Avg Property Value
    plt.figure(figsize=(10, 4))
    bars = plt.bar(boroughs, avg_mv, color='lightgreen', edgecolor='black')
    plt.yscale('log')  # Logarithmic scale

    plt.title("Average Property Value by Borough (Log Scale)")
    plt.xlabel("Borough")
    plt.ylabel("Average Market Value ($, log scale)")
    plt.grid(axis='y', linestyle='--', alpha=0.6)

# Annotate each bar with its value
    for bar, value in zip(bars, avg_mv):
        plt.text(bar.get_x() + bar.get_width() / 2, value,
                 f"${value:,.0f}", ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig("avg_property_value_by_borough_log_annotated.png")
    plt.show()

    # 2. Bar Chart: Avg Crime Count
    plt.figure(figsize=(10, 4))
    plt.bar(boroughs, totalCollisionShare, color='tomato', edgecolor='black')
    plt.title("Share of total Collisions by Borough")
    plt.xlabel("Borough")
    plt.ylabel("Share of total collisions (%)")
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    for bar, value in zip(bars, totalCollisionShare):
        plt.text(bar.get_x() + bar.get_width() / 2, value,
                 f"{value:,.0f}%", ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig("avg_crime_count_by_borough.png")
    plt.show()

    # 3. Scatter Plot: Crime Count vs Property Value
    plt.figure(figsize=(6, 5))
    plt.scatter(totalCollisionShare, avg_mv, s=100, color='mediumslateblue', edgecolor='black')
    for i, boro in enumerate(boroughs):
        plt.annotate(boro, (totalCollisionShare[i]+0.2, avg_mv[i]), fontsize=8)
    plt.title("Crime Count vs Property Value")
    plt.xlabel("Share of Total Collisions (%)")
    plt.ylabel("Average Market Value ($)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("scatter_crime_vs_value.png")
    plt.show()

if __name__ == "__main__":
    summary = fetch_summary_data()
    generate_visualizations(summary)



