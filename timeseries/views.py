from django.http import JsonResponse, HttpResponse

from housol.settings import TIDB_PUBLIC_KEY, TIDB_PRIVATE_KEY
from .functions.general import format_structures, format_date
from requests.auth import HTTPDigestAuth
import pandas as pd
import statsmodels.api as sm
from datetime import datetime
import copy

def index(request):
    return HttpResponse("Welcome to housol, login using https://housol.vercel.app")

import requests
from rest_framework import status
from django.http import JsonResponse
from .functions.general import format_structures

API_BASE_URL = 'https://eu-central-1.data.tidbcloud.com/api/v1beta/app/dataapp-SRymGIuj/endpoint/v1/'


def fetch_data_from_api(endpoint):
    url = API_BASE_URL + endpoint
    try:
        response = requests.get(url, auth=HTTPDigestAuth(TIDB_PUBLIC_KEY, TIDB_PRIVATE_KEY))

        response.raise_for_status()
        return response.json()['data']['rows']
    except requests.exceptions.RequestException as e:
        error_message = f"Error occurred while fetching data from the API: {str(e)}"
        return {"error": error_message}


def get_prices(structure):
    endpoint = f"prices?structure={structure}"
    data = fetch_data_from_api(endpoint)
    if "error" in data:
        return JsonResponse(data, safe=False, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse(data, safe=False, status=status.HTTP_200_OK)


def get_structures():
    endpoint = f"structures"
    data = fetch_data_from_api(endpoint)
    if "error" in data:
        return JsonResponse(data, safe=False, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse(data, safe=False, status=status.HTTP_200_OK)


def get_struc(kwargs):
    if 'id' in kwargs:
        # Fetch data for a specific structure
        structure_id = kwargs["id"]
        endpoint = f'prices_structures?structure={structure_id}'
        data = fetch_data_from_api(endpoint)
    else:
        # Fetch data for top 10 structures
        endpoint = 'prices_structures_meta'
        data = fetch_data_from_api(endpoint)

    if "error" in data:
        return JsonResponse(data, safe=False, status=status.HTTP_400_BAD_REQUEST)

    # Successful response
    return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

'''
    Predict house prices
'''
def predict_prices(data, start, end):
    new_list = []
    try:
        for i in data:
            start_d = datetime.strptime(copy.deepcopy(i['end_date']), '%Y-%m')
            end_d = datetime.strptime(copy.deepcopy(end), '%Y-%m')
            date_rng = pd.date_range(start=start_d, end=end_d, freq='m')
            len_date_rng = len(date_rng)

            house_prices = i['HousePrices']
            df = pd.DataFrame(house_prices)
            df['datetime'] = pd.to_datetime(df['date'])
            df.drop(['date'], axis=1, inplace=True)
            df['date'] = df['datetime'] 
            df.drop(['datetime'], axis=1, inplace=True)
            df = df.set_index('date')
            mod = sm.tsa.statespace.SARIMAX(df,
                                    order=(1, 1, 1),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)

            results = mod.fit()
            
            len_date_rng = len_date_rng + 1

            pred_uc = results.get_forecast(steps=len_date_rng)
            
            new_df = pd.DataFrame(pred_uc.predicted_mean)
            new_df.reset_index(inplace=True)
            new_df.columns = ['date', 'price']
            datetimes = [start, end]
            list_dates = pd.to_datetime(datetimes).tolist()
            new_df = new_df[(new_df['date'] >= list_dates[0]) & (new_df['date'] <= list_dates[1])]

            new_df['date'] = new_df['date'].map(lambda x: x.strftime('%Y-%m'))

            new_df['price'] = new_df['price'].round(2)
            new_prices = new_df.to_dict(orient='records')
            
            
            i['HousePrices'] = new_prices

            new_list.append(i)
    except Exception as e:
        print(e)

    return new_list

'''
    Filter or predict Structures
'''
def process_structure(request, id):
    parameters = request.data

    prices = get_prices(id)
    result = format_structures(prices)

    if 'predict' in parameters and parameters['predict']:
        new_list = []
        if len(result) > 0:
            new_list = predict_prices(list(result), parameters['start_date'], parameters['end_date'])
    else:
        new_list = format_date(result, parameters['start_date'], parameters['end_date'])

    return JsonResponse(new_list, safe=False)
