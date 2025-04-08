import requests
import json

# get the data
response = requests.get('https://maps.googleapis.com/maps/api/')
data = response.text
in_dict = json.loads(data)
print(in_dict.get(""))