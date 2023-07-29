import pandas as pd
import os
import json

def start_load():
    print("loading prices into JSON file...")
    # Startup code
    structures = [
        {"name": "1 Bedroom", "csv_title": "1Bedroom.csv", "key": "1bedroom"},
        {"name": "2 Bedroom", "csv_title": "2Bedroom.csv", "key": "2bedroom"},
        {"name": "3 Bedroom", "csv_title": "3Bedroom.csv", "key": "3bedroom"},
        {"name": "4 Bedroom", "csv_title": "4Bedroom.csv", "key": "4bedroom"},
        {"name": "5 Bedroom", "csv_title": "5Bedroom.csv", "key": "5bedroom"},
        {"name": "Condo", "csv_title": "Condo.csv", "key": "condo"},
    ]

    ignore_columns = ["RegionID", "SizeRank", "RegionName", "RegionType", "StateName"]
    prices_data_for_json = []

    # Read the existing structure data from the samples.json file
    with open("sample_data.json", "r") as json_file:
        existing_structure_data = json.load(json_file)

    for i in structures:
        for structure_info in existing_structure_data:
            if structure_info["fields"]["key"] == i["key"]:
                path = os.path.join("data/housecitydata/", i["csv_title"])
                data = pd.read_csv(path)
                new_data = data.dropna(axis=1, how="any")

                list_res = new_data.to_dict(orient="records")
                for rec in list_res:
                    all_keys = rec.keys()
                    dates = [{"date": key, "price": rec[key]} for key in all_keys if key not in ignore_columns]
                    new_rec = dict([(k, v) for k, v in rec.items() if k in ignore_columns])
                    new_rec["HousePrices"] = dates
                    new_rec["start_date"] = min(dates, key=lambda x: x["date"])["date"]
                    new_rec["end_date"] = max(dates, key=lambda x: x["date"])["date"]

                    # Append the prices data to the list for JSON
                    prices_info_for_json = {
                        "model": "timeseries.prices",
                        "fields": {
                            "structure": structure_info["pk"],
                            "RegionName": new_rec["RegionName"],
                            "State": new_rec["State"] if 'State' in new_rec else "",
                            "Metro": new_rec["Metro"] if 'Metro' in new_rec else "",
                            "RegionID": new_rec["RegionID"] if 'RegionID' in new_rec else "",
                            "RegionType": new_rec["RegionType"] if 'RegionType' in new_rec else "",
                            "SizeRank": new_rec["SizeRank"] if 'SizeRank' in new_rec else "",
                            "start_date": str(new_rec["start_date"]),
                            "end_date": str(new_rec["end_date"]),
                            "HousePrices": new_rec["HousePrices"],
                        }
                    }
                    prices_data_for_json.append(prices_info_for_json)

    # Write the prices data to a JSON file
    json_filename = "prices_data.json"
    with open(json_filename, "w") as json_file:
        json.dump(prices_data_for_json, json_file, indent=4)

    print("ended loading prices into JSON file:", json_filename)


start_load()
