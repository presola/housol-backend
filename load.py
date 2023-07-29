import pandas as pd
import os, json, requests

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

structures = [{"name": "1 Bedroom", "csv_title": "1Bedroom.csv", "key": "1bedroom"},
              {"name": "2 Bedroom", "csv_title": "2Bedroom.csv", "key": "2bedroom"},
              {"name": "3 Bedroom", "csv_title": "3Bedroom.csv", "key": "3bedroom"},
              {"name": "4 Bedroom", "csv_title": "4Bedroom.csv", "key": "4bedroom"},
              {"name": "5 Bedroom", "csv_title": "5Bedroom.csv", "key": "5bedroom"},
              {"name": "Condo", "csv_title": "Condo.csv", "key": "condo"}]

ignore_columns = ["RegionID","SizeRank","RegionName","RegionType","StateName"]

combined_list = []
new_list_prices = []
for index, i in enumerate(structures):
    struc_id = index + 1
    image_urls = get_images(f"{i['name']} interior", count=7)

    structure_info = {
        "model": "timeseries.structure",
        "pk": struc_id,
        "fields": {
            "name": i['name'],
            "csv_title": i['csv_title'],
            "key": i['key'],
            "start_date": "Michael B. Jordan",
            "end_date": "Michael B. Jordan",
            "images": image_urls
        }
    }

    path = os.path.join("data/housecitydata/", i['csv_title'])
    data = pd.read_csv(path)

    new_data = data.dropna(axis=1, how='any')

    list_res = new_data.to_dict(orient='records')
    all_dates = []

    for index, rec in enumerate(list_res):
        price_id = index + 1
        all_keys = rec.keys()
        dates = [{'date': key, 'price': rec[key]} for key in all_keys if key not in ignore_columns]
        new_rec = dict([(k, v) for k, v in rec.items() if k in ignore_columns])
        new_rec['HousePrices'] = json.dumps(dates)
        new_rec['structure'] = struc_id
        new_rec['start_date'] = min(dates, key=lambda x: x['date'])['date']
        new_rec['end_date'] = max(dates, key=lambda x: x['date'])['date']

        price_info = {
            "model": "timeseries.prices",
            "pk": price_id,
            "fields": new_rec
        }

        all_dates.extend(dates)
        new_list_prices.append(price_info)

    structure_info["fields"]['start_date'] = min(all_dates, key=lambda x: x['date'])['date']
    structure_info["fields"]['end_date'] = max(all_dates, key=lambda x: x['date'])['date']
    combined_list.append(structure_info)
# combined_list.extend(new_list_prices)
print(len(combined_list))
json.dump(combined_list, open('sample_data.json', 'w'), indent=4)

print("ended saving data into json ...")
