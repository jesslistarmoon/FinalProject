import sqlite3
import os
import matplotlib.pyplot as plt

def fetch_summary_data(db_name="NYC_Data.db"):
    path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(path, db_name)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Join and aggregate values by borough ZIP ranges
    query = '''
    SELECT z.zip, z.lat, z.long, n.avg_mv, c.crime_count
    FROM zips_and_coordinates z
    JOIN nycdata n ON z.zip = n.zip_code
    JOIN crime_data c ON z.zip = c.zip_code
    '''
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    # Group by borough
    boroughs = {
        "Manhattan": range(10001, 10283),
        "Bronx": range(10451, 10476),
        "Brooklyn": range(11201, 11257),
        "Queens": range(11001, 11698),
        "Staten Island": range(10301, 10315)
    }

    grouped = {boro: [] for boro in boroughs}
    for row in rows:
        zip_code = int(row[0])
        mv = row[3]
        crimes = row[4]
        for boro, zip_range in boroughs.items():
            if zip_code in zip_range:
                grouped[boro].append((mv, crimes))
                break

    summary = []
    for boro, data in grouped.items():
        if data:
            total_mv = sum(v[0] for v in data)
            total_crimes = sum(v[1] for v in data)
            count = len(data)
            summary.append((boro, round(total_mv / count, 2), round(total_crimes / count, 2)))
        else:
            summary.append((boro, 0, 0))

    return summary

def generate_visualizations(summary_data):
    boroughs = [r[0] for r in summary_data]
    avg_mv = [r[1] for r in summary_data]
    avg_crimes = [r[2] for r in summary_data]

    # 1. Bar Chart: Avg Property Value
    plt.figure(figsize=(10, 4))
    plt.bar(boroughs, avg_mv, color='lightgreen', edgecolor='black')
    plt.title("Average Property Value by Borough")
    plt.xlabel("Borough")
    plt.ylabel("Average Market Value ($)")
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("avg_property_value_by_borough.png")
    plt.show()

    # 2. Bar Chart: Avg Crime Count
    plt.figure(figsize=(10, 4))
    plt.bar(boroughs, avg_crimes, color='tomato', edgecolor='black')
    plt.title("Average Crime Count by Borough")
    plt.xlabel("Borough")
    plt.ylabel("Average Crime Count")
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("avg_crime_count_by_borough.png")
    plt.show()

    # 3. Scatter Plot: Crime Count vs Property Value
    plt.figure(figsize=(6, 5))
    plt.scatter(avg_crimes, avg_mv, s=100, color='mediumslateblue', edgecolor='black')
    for i, boro in enumerate(boroughs):
        plt.annotate(boro, (avg_crimes[i]+0.2, avg_mv[i]), fontsize=8)
    plt.title("Crime Count vs Property Value")
    plt.xlabel("Average Crime Count")
    plt.ylabel("Average Market Value ($)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("scatter_crime_vs_value.png")
    plt.show()

    # ⭐ BONUS: Stacked Bar – Crime Rate and Property Value Together
    plt.figure(figsize=(10, 5))
    bar_width = 0.35
    x = range(len(boroughs))

    plt.bar(x, avg_mv, width=bar_width, color='cornflowerblue', label='Avg Market Value')
    plt.bar([p + bar_width for p in x], avg_crimes, width=bar_width, color='orange', label='Avg Crime Count')

    plt.xlabel("Borough")
    plt.ylabel("Value")
    plt.title("Property Value vs Crime Count (Side-by-Side)")
    plt.xticks([p + bar_width / 2 for p in x], boroughs)
    plt.legend()
    plt.tight_layout()
    plt.savefig("side_by_side_value_crime.png")
    plt.show()

if __name__ == "__main__":
    summary = fetch_summary_data("NYC_Data.db")
    generate_visualizations(summary)



