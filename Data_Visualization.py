import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

conn = sqlite3.connect("travel_weather.db")

# Query average travel time by location
df_travel = pd.read_sql_query("""
SELECT locations.latitude, locations.longitude, AVG(travel_data.travel_time) AS avg_travel_time 
FROM travel_data 
JOIN locations ON travel_data.location_id = locations.id 
GROUP BY locations.id
""", conn)

plt.figure(figsize=(8, 6))
sns.barplot(data=df_travel, x="latitude", y="avg_travel_time", palette="coolwarm")
plt.title("Average Travel Time by Location")
plt.xlabel("Latitude")
plt.ylabel("Avg Travel Time (s)")
plt.show()

# Query and plot average temperature
df_weather = pd.read_sql_query("""
SELECT locations.latitude, locations.longitude, AVG(weather_data.temperature) AS avg_temperature 
FROM weather_data 
JOIN locations ON weather_data.location_id = locations.id 
GROUP BY locations.id
""", conn)

plt.figure(figsize=(8, 6))
sns.barplot(data=df_weather, x="latitude", y="avg_temperature", palette="magma")
plt.title("Average Temperature by Location")
plt.xlabel("Latitude")
plt.ylabel("Avg Temperature (F)")
plt.show()