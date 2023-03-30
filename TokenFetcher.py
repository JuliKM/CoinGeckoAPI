# Imports
import requests
from requests.structures import CaseInsensitiveDict
import json
import time
from datetime import datetime
import pandas as pd

# Get token list from API
MAX_CALLS_TO_API = 23
headers = CaseInsensitiveDict()
headers["accept"] = "application/json"

def get_tokens():
    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
    resp = requests.get(url, headers=headers)
    list_all_tokens = resp.content.decode()
    y_list = json.loads(list_all_tokens)
    return y_list

# Get Eth only tokens
def filter_eth_tokens(y_list):
    y_list_w_eth_filtered = []
    for i in range(len(y_list)):
        if  ((y_list[i]['platforms']).get('ethereum'))!= None:
            if (y_list[i]['platforms']).get('ethereum').startswith('0x'):
                y_list_w_eth_filtered.append(y_list[i])
    return y_list_w_eth_filtered

# Get prices for ETH tokens
def fetch_prices_for_eth_tokens(y_list_w_eth_filtered):

    all_prices=[]
    datetimes=[]
    for i in range(MAX_CALLS_TO_API):   #(len(y_list_w_eth_filtered)):
        url = f"https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses={y_list_w_eth_filtered[i]['platforms'].get('ethereum')}&vs_currencies=USD"
        resp = requests.get(url, headers=headers)
        prices = resp.content.decode()
        datetimes.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"))
        all_prices.append(prices)
        time.sleep(3)
    return datetimes, all_prices

#  Format price column to retrieve number with two decimals and fill missing values with 0
def get_two_decimals(all_prices):
    prices_column_list = []
    for i in range(len(all_prices)):
        if "usd" not in all_prices[i]: 
            first_chars = 0
        else:
            all_prices[2].split('"usd":')[1]
            if i!=2: mistring = all_prices[i].split('"usd":')[1]
            first_chars = float(mistring[0:4])   
        prices_column_list.append(first_chars)
    return prices_column_list

# Flatten values into lists from dictionary
def list_definition(y_list_w_eth_filtered):
    names=[]
    symbols =[]
    address =[]
    for i in range(MAX_CALLS_TO_API):
        names.append(y_list_w_eth_filtered[i]['name'])
        symbols.append((y_list_w_eth_filtered[i]['symbol']).upper())
        address.append((y_list_w_eth_filtered[i]['platforms']).get('ethereum'))
    return names, symbols, address

#  Create dataframe
def create_dataframe(names, symbols, address, prices_column_list, datetimes):
    data_tuples = list(zip(names, symbols, address, prices_column_list, datetimes))
    df = pd.DataFrame(data_tuples, columns=['name','symbol', 'address', 'price', 'timestamp'])
    return df

#  Save to csv
def save_to_csv(df):
    current_time = datetime.now().strftime("%d-%m-%Y_%H-%M%SS%f")
    csv_name = f"token_values_{current_time}.csv" 
    df.to_csv(csv_name)

while(True):
    y_list = get_tokens()
    if Api_working==True :
        
        y_list_w_eth_filtered = filter_eth_tokens(y_list)
        datetimes, all_prices = fetch_prices_for_eth_tokens(y_list_w_eth_filtered)
        prices_column_list = get_two_decimals(all_prices)
        names, symbols, address = list_definition(y_list_w_eth_filtered)
        df = create_dataframe(names, symbols, address, prices_column_list, datetimes)
        existing_Df = load_csv
        existing_Df.apped(df)
        save_to_csv(df)
    time.sleep(120)