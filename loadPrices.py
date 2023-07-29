import pandas as pd

from housol.wsgi import *
from timeseries.models import Structure, Prices


def start_load():
    print("loading prices into db ...")
    # Startup code
    structures = [{"name": "1 Bedroom", "csv_title": "1Bedroom.csv", "key": "1bedroom"},
                  {"name": "2 Bedroom", "csv_title": "2Bedroom.csv", "key": "2bedroom"},
                  {"name": "3 Bedroom", "csv_title": "3Bedroom.csv", "key": "3bedroom"},
                  {"name": "4 Bedroom", "csv_title": "4Bedroom.csv", "key": "4bedroom"},
                  {"name": "5 Bedroom", "csv_title": "5Bedroom.csv", "key": "5bedroom"},
                  {"name": "Condo", "csv_title": "Condo.csv", "key": "condo"}]

    ignore_columns = ["RegionID","SizeRank","RegionName","RegionType","StateName"]
    structure_filter = Structure.objects.filter(key=structures[0]['key'])
    if structure_filter.count() > 0:
        for i in structures:
            structure = Structure.objects.filter(key=i['key'])
            if structure.count() > 0:
                prices = Prices.objects.filter(structure=structure.get())
                if prices.count() < 1:
                    path = os.path.join("data/housecitydata/", i['csv_title'])
                    data = pd.read_csv(path)
                    # data.dropna()
                    # data.fillna(0, inplace=True)
                    new_data = data.dropna(axis=1, how='any')

                    list_res = new_data.to_dict(orient='records')
                    all_dates = []

                    new_list_res = []
                    for rec in list_res:
                        all_keys = rec.keys()
                        dates = [{'date': key, 'price': rec[key]} for key in all_keys if key not in ignore_columns]
                        new_rec = dict([(k, v) for k, v in rec.items() if k in ignore_columns])
                        new_rec['HousePrices'] = dates
                        new_rec['start_date'] = min(dates, key=lambda x: x['date'])['date']
                        new_rec['end_date'] = max(dates, key=lambda x: x['date'])['date']
                        Prices.objects.create(structure=structure.get(), **new_rec)

    print("ended loading prices into db ...")

start_load()
