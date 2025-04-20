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

    query = '''
        SELECT
            b.borough_name,
            bp.population
        FROM boroughs b
        JOIN borough_population bp ON b.id = bp.id;
    '''
    cur.execute(query)
    populations = cur.fetchall()

    query = '''
        SELECT
            b.borough_name,
            COUNT(p.id) AS park_count
        FROM boroughs b
        LEFT JOIN parks p ON b.id = p.borough_id
        GROUP BY b.id, b.borough_name
        ORDER BY b.borough_name;
    '''
    cur.execute(query)
    parks = cur.fetchall()
    conn.close()

    boroughCollisions = defaultdict(int)
    boroughPropertyValue = defaultdict(list)
    boroughParks = defaultdict(int)
    boroughPopulation = defaultdict(int)

    for _, borough, collision_id, market_value in rows:
        boroughCollisions[borough]+=1
        boroughPropertyValue[borough].append(market_value)

    for borough, population in populations:
        boroughPopulation[borough] = population

    for borough, count in parks:
        boroughParks[borough] = count

    results = {}
    for borough in boroughCollisions:
        results[borough] = {}
        results[borough]["marketValue"] = sum(boroughPropertyValue[borough])/len(boroughPropertyValue[borough])
        results[borough]["collisionPerCapita"] = boroughCollisions[borough]/boroughPopulation[borough]
        results[borough]["parksPerCapita"] = boroughParks[borough]/boroughPopulation[borough]

    return results

def generate_visualizations(summary_data):
    boroughs = [r for r in summary_data.keys()]
    avg_mv = [r["marketValue"] for r in summary_data.values()]
    totalCollisionShare = [r["collisionPerCapita"]*100000 for r in summary_data.values()]
    parksPerCapita = [r["parksPerCapita"]*100000 for r in summary_data.values()]

    # 1. Bar Chart: Avg Property Value
    plt.figure(figsize=(10, 4))
    bars = plt.bar(boroughs, avg_mv, color='lightgreen', edgecolor='black')

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

    # 2. Bar Chart: Collision poer capita
    plt.figure(figsize=(10, 4))
    plt.bar(boroughs, totalCollisionShare, color='tomato', edgecolor='black')
    plt.title("Collision per Capita (100000) by Borough")
    plt.xlabel("Borough")
    plt.ylabel("Collision per Capita (100000)")
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    for bar, value in zip(bars, totalCollisionShare):
        plt.text(bar.get_x() + bar.get_width() / 2, value,
                 f"{value:,.0f}", ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig("collision_per_capita.png")
    plt.show()

    # 3. Bar Chart: Parks per capita
    plt.figure(figsize=(10, 4))
    plt.bar(boroughs, parksPerCapita, color='tomato', edgecolor='black')
    plt.title("Parks per Capita (100000) by Borough")
    plt.xlabel("Borough")
    plt.ylabel("Parks per Capita (100000)")
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    for bar, value in zip(bars, parksPerCapita):
        plt.text(bar.get_x() + bar.get_width() / 2, value,
                 f"{value:,.0f}", ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig("parks_per_capita.png")
    plt.show()

    # 4. Scatter Plot: Callision Count vs Property Value
    plt.figure(figsize=(6, 5))
    plt.scatter(totalCollisionShare, avg_mv, s=100, color='mediumslateblue', edgecolor='black')
    for i, boro in enumerate(boroughs):
        plt.annotate(boro, (totalCollisionShare[i]+0.2, avg_mv[i]), fontsize=8)
    plt.title("Collision Per Capita (100000) vs Property Value")
    plt.xlabel("Collision Per Capita (100000)")
    plt.ylabel("Average Market Value ($)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("scatter_collision_vs_value.png")
    plt.show()

    # 5. Scatter Plot: Parkesr per capita vs Property value
    plt.figure(figsize=(6, 5))
    plt.scatter(parksPerCapita, avg_mv, s=100, color='mediumslateblue', edgecolor='black')
    for i, boro in enumerate(boroughs):
        plt.annotate(boro, (parksPerCapita[i]+0.2, avg_mv[i]), fontsize=8)
    plt.title("Parks Per Capita (100000) vs Property Value")
    plt.xlabel("Parks Per Capita (100000)")
    plt.ylabel("Average Market Value ($)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("scatter_parks_vs_value.png")
    plt.show()

if __name__ == "__main__":
    summary = fetch_summary_data()
    generate_visualizations(summary)

