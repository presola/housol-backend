import os
import json
import requests
import pandas as pd

# Replace "YOUR_UNSPLASH_ACCESS_KEY" with your actual Unsplash API access key
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')

def get_images(query, count=10):
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    params = {
        "query": query,
        "per_page": count
    }
    url = "https://api.unsplash.com/search/photos"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return [image["urls"]["regular"] for image in data["results"]]
    else:
        print("Failed to fetch images:", response.status_code)
        return []

print("loading data from CSV ...")
# Startup code

structures = [
    {"name": "1 Bedroom", "csv_title": "1Bedroom.csv", "key": "1bedroom"},
    {"name": "2 Bedroom", "csv_title": "2Bedroom.csv", "key": "2bedroom"},
    {"name": "3 Bedroom", "csv_title": "3Bedroom.csv", "key": "3bedroom"},
    {"name": "4 Bedroom", "csv_title": "4Bedroom.csv", "key": "4bedroom"},
    {"name": "5 Bedroom", "csv_title": "5Bedroom.csv", "key": "5bedroom"},
    {"name": "Condo", "csv_title": "Condo.csv", "key": "condo"},
]

combined_list = []

for index, i in enumerate(structures):
    struc_id = index + 1
    structure_info = {
        "model": "timeseries.structure",
        "pk": struc_id,
        "fields": {
            "name": i['name'],
            "csv_title": i['csv_title'],
            "key": i['key'],
            "start_date": "2009-01-31",  # Modify as needed
            "end_date": "2023-06-30",    # Modify as needed
            "images": get_images(f"{i['name']} interior", count=10)
        }
    }
    combined_list.append(structure_info)

print(len(combined_list))
json.dump(combined_list, open('structures_data.json', 'w'), indent=4)

print("ended saving data into json ...")
