import requests
import json
import time

# API Keys Not sure what API key yet
GOOGLE_API_KEY = "GOOGLE_API_KEY"
OPENWEATHER_API_KEY = "OPENWEATHER_API_KEY"
TOMORROW_IO_API_KEY = "TOMORROW_IO_API_KEY"

# Locations to Fetch Data For
LOCATIONS = [
    {"lat": 42.2808, "lng": -83.7430},  # Ann Arbor, MI
    {"lat": 40.7128, "lng": -74.0060},  # New York, NY
]

# Fetch travel data from Google Maps API
def fetch_travel_data():
    data = []
    for loc in LOCATIONS:
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={loc['lat']},{loc['lng']}&destination=42.3314,-83.0458&key={GOOGLE_API_KEY}"
        response = requests.get(url)
        #
    return data

# Fetch weather data from OpenWeather API
def fetch_weather_data():
    data = []
    for loc in LOCATIONS:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={loc['lat']}&lon={loc['lng']}&appid={OPENWEATHER_API_KEY}&units=imperial"
        response = requests.get(url)
        #
    return data

if __name__ == "__main__":
    travel_data = fetch_travel_data()
    weather_data = fetch_weather_data()

    # Save data to a JSON file for insertion
    with open("data.json", "w") as f:
        json.dump({"travel": travel_data, "weather": weather_data}, f, indent=4)
