import requests
import json
import re
import folium
from pprint import pprint

with open('C:/Users/mhammed/Downloads/comments_export2.json', 'r') as f:
        data = json.load(f)
bbox = "9.8,53.4,10.3,53.7"
Straßen_Kordinaten = {}
for key in data:
    text = data[key]['text']
    special_char_map = {ord('ä'): 'ae', ord('ü'): 'ue', ord('ö'): 'oe', ord('Ö'): 'Oe', ord('ß'): 'ss'}
    text = text.translate(special_char_map)
    data[key]['text'] = text
    street_names = re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)*(?:strasse|weg|platz|allee|park)\b", text)
        for street_name in street_names:
            url = f"https://nominatim.openstreetmap.org/search?format=json&q={street_name}&city=hamburg&country=Germany&bounded=1&viewbox={bbox}"
            response = requests.get(url)
            response_data = response.json()
            if response_data:
                lat = response_data[0]["lat"]
                lon = response_data[0]["lon"]
                Straßen_Kordinaten[street_name] = {"latitude": lat, "longitude": lon}

pprint(Straßen_Kordinaten)

map_center = [53.5671 , 10.0271]
map_osm = folium.Map(location=map_center, zoom_start=13)
for street_name, coords in Straßen_Kordinaten.items():
    lat = float(coords['latitude'])
    lon = float(coords['longitude'])
    marker = folium.Marker([lat, lon], popup=street_name)
    marker.add_to(map_osm)

map_osm

