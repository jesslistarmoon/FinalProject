import sqlite3
from collections import defaultdict
import json
import folium

# ✅ Your updated API key
API_KEY = "YAIzaSyDoqB0LkalbSFcoDhZVkdf8MnBg63Kx2z0"
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


    results = {}
    for borough in boroughCollisions:
        results[borough] = {}
        results[borough]["marketValue"] = sum(boroughPropertyValue[borough])/len(boroughPropertyValue[borough])
        results[borough]["collisionShare"] = (len(boroughCollisions[borough])/len(rows))

    return results

def generate_visualiation(borough_stats):
    nyc_coords = [40.7128, -74.0060]

    # Stats per borough
    borough_stats = {
        "BROOKLYN": {"marketValue": 1147861.05, "collisionShare": 0.32},
        "BRONX": {"marketValue": 262617562.55, "collisionShare": 0.10},
        "MANHATTAN": {"marketValue": 82800.00, "collisionShare": 0.11},
        "QUEENS": {"marketValue": 390778378.90, "collisionShare": 0.15},
        "STATEN ISLAND": {"marketValue": 3337201.50, "collisionShare": 0.05}
    }

    # Load GeoJSON
    with open("boroughs.geojson") as f:
        borough_geojson = json.load(f)
    # Create folium map
    m = folium.Map(location=nyc_coords, zoom_start=10, tiles="CartoDB positron")

    # Color function based on collision share
    def style_function(feature):
        name = feature["properties"]["name"].upper()
        stats = borough_stats.get(name, {})
        share = stats.get("collisionShare", 0)
        # Normalize color opacity from collisionShare
        return {
            "fillOpacity": 0.6,
            "weight": 1,
            "color": "black",
            "fillColor": f"rgba(255, 0, 0, {min(share + 0.2, 1.0)})"
        }

    # Popup with stats
    def popup_html(name):
        stats = borough_stats.get(name.upper())
        if not stats:
            return f"<strong>{name}</strong><br>No data available"
        return f"""
            <strong>{name}</strong><br>
            Avg Market Value: ${stats['marketValue']:,.2f}<br>
            Share of Collisions: {stats['collisionShare']*100:.2f}%
        """

    # Add GeoJson with popups
    for feature in borough_geojson["features"]:
        boro_name = feature["properties"]["name"]
        folium.GeoJson(
            feature,
            style_function=style_function,
            tooltip=popup_html(boro_name)
        ).add_to(m)

# Save map
    m.save("borough_stats_map.html")

if __name__ == "__main__":
    data = fetch_summary_data()
    generate_visualiation(data)
