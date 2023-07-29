import os

import pandas as pd
import json

def save_inflation_data_to_json(json_filename):
    print("loading inflation data from CSV and creating JSON file ...")
    try:
        path = os.path.join("data/inflation.csv")
        data = pd.read_csv(path)
        inflation_data_for_json = []

        for index, row in data.iterrows():
            year = int(row["Year"])
            rate = float(row["Rate"])
            funds_rate = float(row["Funds rate"])
            gdp_growth = str(row["Gdp growth"])
            events = str(row["Events"])

            # Append the data to the list for JSON
            inflation_info_for_json = {
                "model": "timeseries.inflation",
                "pk": year,  # Using the year as the primary key
                "fields": {
                    "year": year,
                    "rate": rate,
                    "funds_rate": funds_rate,
                    "gdp_growth": gdp_growth,
                    "events": events
                }
            }
            inflation_data_for_json.append(inflation_info_for_json)

        # Write the inflation data to a JSON file
        with open(json_filename, "w") as json_file:
            json.dump(inflation_data_for_json, json_file, indent=4)

        print("Data saved to JSON file successfully:", json_filename)
    except Exception as e:
        print("An error occurred while saving data:", str(e))

if __name__ == "__main__":
    # Replace "inflation_data.csv" with the actual filename of your CSV file
    csv_filename = "inflation.csv"
    # Replace "inflation_data.json" with the desired JSON filename
    json_filename = "inflation_data.json"
    save_inflation_data_to_json(json_filename)
