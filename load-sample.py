import pandas as pd
import json

def json_to_csv(json_filename, csv_filename):
    try:
        with open(json_filename, "r") as json_file:
            json_data = json.load(json_file)

        data_for_csv = []

        for item in json_data:
            fields = item["fields"]
            data_for_csv.append(fields)

        df = pd.DataFrame(data_for_csv)
        df.to_csv(csv_filename, index=False)

        print("Data saved to CSV file successfully:", csv_filename)
    except Exception as e:
        print("An error occurred while saving data:", str(e))

if __name__ == "__main__":
    json_filename = "sample_data.json"
    csv_filename = "output_data.csv"
    json_to_csv(json_filename, csv_filename)
