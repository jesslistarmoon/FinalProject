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
        select
            b.id as borough_id,
            b.borough_name,
            c.id as collision_id,
            p.market_value as property_market_value
        from boroughs b
        join collisions c on b.id = c.borough_id
        join properties p on b.id = p.borough_id
        order by b.id;
    '''
    cur.execute(query)
    rows = cur.fetchall()

    query = '''
        select
            b.borough_name,
            bp.population
        from boroughs b
        join borough_population bp on b.id = bp.id;
    '''
    cur.execute(query)
    populations = cur.fetchall()

    query = '''
        select
            b.borough_name,
            count(p.id) as park_count
        from boroughs b
        left join parks p on b.id = p.borough_id
        group by b.id, b.borough_name
        order by b.borough_name;
    '''
    cur.execute(query)
    parks = cur.fetchall()
    conn.close()

    boroughcollisions = defaultdict(int)
    boroughpropertyvalue = defaultdict(list)
    boroughparks = defaultdict(int)
    boroughpopulation = defaultdict(int)

    for _, borough, collision_id, market_value in rows:
        boroughcollisions[borough]+=1
        boroughpropertyvalue[borough].append(market_value)

    for borough, population in populations:
        boroughpopulation[borough] = population

    for borough, count in parks:
        boroughparks[borough] = count

    results = {}
    for borough in boroughcollisions:
        results[borough] = {}
        results[borough]["marketValue"] = sum(boroughpropertyvalue[borough])/len(boroughpropertyvalue[borough])
        results[borough]["collisionPerCapita"] = boroughcollisions[borough]/boroughpopulation[borough]
        results[borough]["parksPerCapita"] = boroughparks[borough]/boroughpopulation[borough]

    return results

def generate_visualiation(borough_stats):
    nyc_coords = [40.7128, -74.0060]

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
            Collision Per Capita (100000): {stats['collisionPerCapita']*100000:.2f}<br>
            Parks Per Capita (100000): {stats['parksPerCapita']*100000:.2f}
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
