import os
import sqlite3
import matplotlib.pyplot as plt

def fetch_joined_data(db_path):
    """Fetch avg_mv and crime_count from joined tables by zip_code."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = '''
    SELECT n.zip_code, n.avg_mv, c.crime_count
    FROM nycdata n
    JOIN crime_data c ON n.zip_code = c.zip_code
    ORDER BY n.zip_code ASC
    '''
    cur.execute(query)
    data = cur.fetchall()
    conn.close()
    return data

def plot_crime_vs_property(db_filename):
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_filename)
    data = fetch_joined_data(db_path)

    zip_codes = [str(row[0]) for row in data]
    avg_mv = [row[1] for row in data]
    crime_counts = [row[2] for row in data]

    plt.figure(figsize=(14, 4))

    # 1. Property Value Bar Chart
    plt.subplot(1, 3, 1)
    plt.barh(zip_codes, avg_mv, color='skyblue')
    plt.xlabel("Avg Market Value ($)")
    plt.title("Avg Property Value by ZIP Code")
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    # 2. Crime Count Bar Chart
    plt.subplot(1, 3, 2)
    plt.barh(zip_codes, crime_counts, color='salmon')
    plt.xlabel("Crime Count (last 25 incidents)")
    plt.title("Crime Count by ZIP Code")
    plt.xticks(fontsize=8)
    plt.yticks([])

    # 3. Scatter Plot: Crime vs. Property Value
    plt.subplot(1, 3, 3)
    plt.scatter(crime_counts, avg_mv, color='purple')
    for i, txt in enumerate(zip_codes):
        plt.annotate(txt, (crime_counts[i], avg_mv[i]), fontsize=6, alpha=0.7)
    plt.xlabel("Crime Count")
    plt.ylabel("Avg Market Value ($)")
    plt.title("Crime vs Property Value")

    plt.tight_layout()
    plt.show()

# Example usage
plot_crime_vs_property(db_filename='project_data.db')



