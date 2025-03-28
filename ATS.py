import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import yfinance as yf
import numpy as np
import datetime as dt
import pandas_ta as ta
from tqdm import tqdm

# Change the sdate and edate value for month and year only do not hamper the date

sdate = '2023-07-01' 
edate = '2023-07-31' 

#****************Actual Code starts*********************# do not change any thing below this line
# use to fetch latest data of stock
start_date = dt.datetime(2023, 1, 1)
end_date = dt.datetime(2050, 8, 18) 
# use to specify the end date only for supertrend
end_date_supertrend = '2050-07-3' 
# use to specify the date of pivot points 
def fetch_dates():
    today = dt.date.today()
    current_month = today.month
    current_year = today.year
    return current_month, current_year

if __name__ == "__main__":
    currrent_month,current_year = fetch_dates()

# Fetching data from chartink
url = "https://chartink.com/screener/process" 
condition1 = {"scan_clause": "( {cash} ( ( {cash} ( latest supertrend( 21,1 ) <= latest close and latest supertrend( 14,2 ) < latest close and 1 day ago  supertrend( 14,2 ) >= 1 day ago  close and latest supertrend( 7 , 3 ) <= latest close and latest volume > 200000 and latest close - 1 candle ago close / 1 candle ago close * 100 <= 5 and latest close >= 50 and latest close > latest ema( latest close , 22 ) and latest close > latest ema( latest close , 44 ) and latest close >= latest ema( latest close , 100 ) ) ) ) )" } 
condition2 = { "scan_clause": "( {cash} ( ( {cash} ( latest supertrend( 21,1 ) <= latest close and latest supertrend( 14,2 ) <= latest close and latest supertrend( 7 , 3 ) < latest close and 1 day ago  supertrend( 7 , 3 ) >= 1 day ago  close and latest volume > 200000 and latest close - 1 candle ago close / 1 candle ago close * 100 <= 5 and latest close >= 50 and latest close > latest ema( latest close , 22 ) and latest close > latest ema( latest close , 44 ) and latest close >= latest ema( latest close , 100 ) ) ) ) )" }
condition3 = { "scan_clause": "( {cash} ( ( {cash} ( latest supertrend( 21,1 ) < latest close and 1 day ago  supertrend( 21,1 ) >= 1 day ago  close and latest supertrend( 14,2 ) <= latest close and latest supertrend( 7 , 3 ) <= latest close and latest volume > 200000 and latest close - 1 candle ago close / 1 candle ago close * 100 <= 5 and latest close >= 50 and latest close > latest ema( latest close , 22 ) and latest close > latest ema( latest close , 44 ) and latest close >= latest ema( latest close , 100 ) ) ) ) )" }


# chatlink stock names storing in data 1,2 and 3
with requests.session() as s:
    r_data = s.get(url)
    soup = bs(r_data.content, "lxml")
    meta = soup.find("meta", {"name" : "csrf-token"})["content"]
    header = {"x-csrf-token" : meta}
    
    data1 = s.post(url, headers=header, data=condition1).json()
    stock_list1 = pd.DataFrame(data1["data"])
    name_array1 = stock_list1['nsecode'].values
  
    data2 = s.post(url, headers=header, data=condition2).json()
    stock_list2 = pd.DataFrame(data2["data"])
    name_array2 = stock_list2['nsecode'].values

    
    data3 = s.post(url, headers=header, data=condition3).json()
    stock_list3 = pd.DataFrame(data3["data"])
    name_array3 = stock_list3['nsecode'].values

# adding .NS symbole at the end of each stock 
def addNseChartacter(arr, character):
    result = [str(element) + character for element in arr]
    return result
character_to_add = '.NS'
array1 = addNseChartacter(name_array1, character_to_add)
array2 = addNseChartacter(name_array2, character_to_add)
array3 = addNseChartacter(name_array3, character_to_add)

# getting all the data about the stock like opening close high low 
def get_opening_price(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        history = stock.history(period="1d")  
        opening_price = history['Open'][0]
        return opening_price
    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")
        return None
    
def get_closing_price(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        history = stock.history(period="1d")  
        closing_price = history['Close'][0]
        return closing_price
    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")
        return None
    
def get_high_price(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        history = stock.history(period="1d") 
        high_price = history['High'][0]
        return high_price
    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")
        return None
    
def get_low_price(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        history = stock.history(period="1d")
        low_price = history['Low'][0]
        return low_price
    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")
        return None

# supretrend calculate
def supertrend1(stock_symbol):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date_supertrend)
    supertrend_period = 7
    multiplier = 3.0 
    supertrend_data = ta.supertrend(stock_data['High'], stock_data['Low'], stock_data['Close'], length=supertrend_period, multiplier=multiplier)
    supertrend_values = supertrend_data['SUPERT_'+str(supertrend_period)+'_'+str(multiplier)]
    latest_supertrend = float(supertrend_values.iloc[-1])
    return latest_supertrend
def supertrend2(stock_symbol):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date_supertrend)
    supertrend_period = 14
    multiplier = 2.0 
    supertrend_data = ta.supertrend(stock_data['High'], stock_data['Low'], stock_data['Close'], length=supertrend_period, multiplier=multiplier)
    supertrend_values = supertrend_data['SUPERT_'+str(supertrend_period)+'_'+str(multiplier)]
    latest_supertrend = float(supertrend_values.iloc[-1])
    return latest_supertrend
def supertrend3(stock_symbol):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date_supertrend)
    supertrend_period = 21
    multiplier = 1.0 
    supertrend_data = ta.supertrend(stock_data['High'], stock_data['Low'], stock_data['Close'], length=supertrend_period, multiplier=multiplier)
    supertrend_values = supertrend_data['SUPERT_'+str(supertrend_period)+'_'+str(multiplier)]
    latest_supertrend = float(supertrend_values.iloc[-1])
    return latest_supertrend
# pivot points
def calculate_fibonacci_pivot_points(data):
    high = data['High']
    low = data['Low']
    close = data['Close']
    pivot = (high + low + close) / 3
    r2 = pivot + ((high - low)*0.618)
    r1 = pivot + ((high - low)*0.382)
    return r2,r1

symbole_array = []
entry_array = []
Stoploss_array = []
target1_array = []
target2_array = []
rr_array = []
for symbol in tqdm(array1, desc="Scanning Array 1", miniters=1):
    open = get_opening_price(symbol)
    close = get_closing_price(symbol)
    high = get_high_price(symbol)
    low= get_low_price(symbol)
    hc= high-close
    co = close-open
    if(open<close):
        if(hc<=co):
            st1 = supertrend1(symbol)
            st2 = supertrend2(symbol)
            st3 = supertrend3(symbol)
            stop_loss = max(st1, st2, st3)
            data = yf.download(symbol, start=sdate, end=edate, interval='1mo')
            r2,r1 = calculate_fibonacci_pivot_points(data)
            target1 = float(r1)
            target2 = float(r2)
            reward = target2-close
            risk=close-stop_loss
            rr = (reward/risk)
            if(rr>1.0 and rr<4.0):
                symbole_array.append(symbol)
                entry_array.append(close)
                Stoploss_array.append(stop_loss)
                target1_array.append(target1)
                target2_array.append(target2)
                rr_array.append(rr)
           


for symbol in tqdm(array2, desc="Scanning Array 2", miniters=1):
    open = get_opening_price(symbol)
    close = get_closing_price(symbol)
    high = get_high_price(symbol)
    low= get_low_price(symbol)
    hc= high-close
    co = close-open
    if(open<close):
        if(hc<=co):
            st1 = supertrend1(symbol)
            st2 = supertrend2(symbol)
            st3 = supertrend3(symbol)
            stop_loss = max(st1, st2, st3)
            data = yf.download(symbol, start=sdate, end=edate, interval='1mo')
            r2,r1 = calculate_fibonacci_pivot_points(data)
            target1 = float(r1)
            target2 = float(r2)
            reward = target2-close
            risk=close-stop_loss
            rr = (reward/risk)
            if(rr>1.0 and rr<4.0):
                symbole_array.append(symbol)
                entry_array.append(close)
                Stoploss_array.append(stop_loss)
                target1_array.append(target1)
                target2_array.append(target2)
                rr_array.append(rr)
                


for symbol in tqdm(array3, desc="Scanning Array 3", miniters=1):
    open = get_opening_price(symbol)
    close = get_closing_price(symbol)
    high = get_high_price(symbol)
    low= get_low_price(symbol)
    hc= high-close
    co = close-open
    if(open<close):
        if(hc<=co):
            st1 = supertrend1(symbol)
            st2 = supertrend2(symbol)
            st3 = supertrend3(symbol)
            stop_loss = max(st1, st2, st3)
            data = yf.download(symbol, start=sdate, end=edate, interval='1mo')
            r2,r1 = calculate_fibonacci_pivot_points(data)
            target1 = float(r1)
            target2 = float(r2)
            reward = target2-close
            risk=close-stop_loss
            rr = (reward/risk)
            if(rr>1.0 and rr<4.0):
                symbole_array.append(symbol)
                entry_array.append(close)
                Stoploss_array.append(stop_loss)
                target1_array.append(target1)
                target2_array.append(target2)
                rr_array.append(rr)

def round_to_nearest_multiple(value, multiple):
    return round(value / multiple) * multiple
def round_array_to_multiple(arr, multiple):
    array = [round_to_nearest_multiple(val, multiple) for val in arr]
    return array

entry_array = round_array_to_multiple(entry_array, 0.05)
Stoploss_array = round_array_to_multiple(Stoploss_array, 0.05)
target1_array = round_array_to_multiple(target1_array, 0.05)
target2_array = round_array_to_multiple(target2_array, 0.05)
rr_array = round_array_to_multiple(rr_array, 0.05)

# removes the NSE symbole at the last of the array 
def remove_similar_character(arr, char_to_remove):
    modified_arr = [s.replace(char_to_remove, '') for s in arr]
    return modified_arr
character_to_remove = ".NS"
symbole_array = remove_similar_character(symbole_array, character_to_remove)
                
for i in range(len(symbole_array)):
    print("Stock Name: ", symbole_array[i])
    print("Entry:", "{:.2f}".format(entry_array[i]))
    print("Stop-loss: ","{:.2f}".format(Stoploss_array[i]))         
    print("Target 1: ","{:.2f}".format(target1_array[i]))
    print("Target 2: ","{:.2f}".format(target2_array[i]))
    print("Risk:Reward ","{:.2f}".format(rr_array[i]))
    print("\n")
    