import requests
import json
import time

# API Keys (Replace with actual keys)
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
TOMORROW_IO_API_KEY = "YOUR_TOMORROW_IO_API_KEY"

# Locations for Data Collection
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
        if response.status_code == 200:
            result = response.json()
            if "routes" in result and result["routes"]:
                duration = result["routes"][0]["legs"][0]["duration"]["value"]
                data.append({
                    "latitude": loc["lat"],
                    "longitude": loc["lng"],
                    "destination_latitude": 42.3314,
                    "destination_longitude": -83.0458,
                    "travel_time": duration,
                    "traffic_impact": "Moderate"
                })
        time.sleep(1)
    return data

# Fetch weather data from OpenWeather API
def fetch_weather_data():
    data = []
    for loc in LOCATIONS:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={loc['lat']}&lon={loc['lng']}&appid={OPENWEATHER_API_KEY}&units=imperial"
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            data.append({
                "latitude": loc["lat"],
                "longitude": loc["lng"],
                "temperature": result["main"]["temp"],
                "feels_like": result["main"]["feels_like"],
                "humidity": result["main"]["humidity"],
                "weather_description": result["weather"][0]["description"]
            })
        time.sleep(1)
    return data

# Fetch additional weather data from Tomorrow.io API
def fetch_tomorrow_io_data():
    data = []
    for loc in LOCATIONS:
        url = f"https://api.tomorrow.io/v4/weather/realtime?location={loc['lat']},{loc['lng']}&apikey={TOMORROW_IO_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            data.append({
                "latitude": loc["lat"],
                "longitude": loc["lng"],
                "uv_index": result["data"]["values"]["uvIndex"]
            })
        time.sleep(1)
    return data

if __name__ == "__main__":
    travel_data = fetch_travel_data()
    weather_data = fetch_weather_data()
    tomorrow_data = fetch_tomorrow_io_data()

    with open("data.json", "w") as f:
        json.dump({"travel": travel_data, "weather": weather_data, "tomorrow": tomorrow_data}, f, indent=4)
