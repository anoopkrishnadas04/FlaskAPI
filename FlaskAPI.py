from flask import Flask
from flask import request
import requests
from bs4 import BeautifulSoup
import json
from urllib.request import Request, urlopen

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_stock_info():
    stock = str(request.args.get('stock')).strip().upper()
    range = str(request.args.get('range')).strip()
    
    input_status = "VALID"
    #print(stock)
    if stock == "NONE" or stock == "":
        input_status = "INVALID"
        return {'input-status' : input_status}

    #ACCESSING STOCK DATA 
    url = f'https://finance.yahoo.com/quote/{stock}?p={stock}'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'}
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    market_price = ""
    market_change = ""
    market_percentage = ""
    for row in soup.find_all('fin-streamer'):
        if row["data-field"]=="regularMarketPrice" and row["data-symbol"]==stock:
            if row.contents[0].name == 'span':
                market_price = row.contents[0].contents[0]
            else:
                market_price = row.contents[0]
            
        if row["data-field"]=="regularMarketChange" and row["data-symbol"]==stock:
            if row.contents[0].name == 'span':
                market_change = row.contents[0].contents[0]
            else:
                market_change = row.contents[0]
        
        if row["data-field"]=="regularMarketChangePercent" and row["data-symbol"]==stock:
            if row.contents[0].name == 'span':
                market_percentage = row.contents[0].contents[0]
            else:
                market_percentage = row.contents[0]

    #ACCESSING GRAPH DATA
    graph_url = ""
    valid_ranges = ["1d", "5d", "1mo", "6mo", "1y", "5y", "ytd"]
    for rng in valid_ranges:
        if rng == range:
            interval = ""
            if(range == "1d"):
                interval = "2m"
            if(range == "5d"):
                interval = "15m"
            if(range == "1mo"):
                interval = "1h"
            if(range == "6mo"):
                interval = "1d"
            if(range == "1y"):
                interval = "1d"
            if(range == "5y"):
                interval = "1wk"
            if(range == "ytd"):
                interval = "3mo"
            graph_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock}?region=US&lang=en-US&includePrePost=false&interval={interval}&useYfid=true&range={range}&corsDomain=finance.yahoo.com&.tsrc=finance"
    
    if graph_url != "":
        data_request = Request(graph_url, headers=headers)
        page = urlopen(data_request)
        graph_json = page.read().decode("utf-8")
    
    #ACCESSING TABLE DATA
    table_json = {}
    table_data = soup.find_all('td')
    table_headers = [
        "Previous Close",
        "Open",
        "Bid",
        "Ask",
        "Day's Range",
        "52 Week Range",
        "Volume",
        "Avg. Volume",
        "Market Cap",
        "Beta (5Y Monthly)",
        "PE Ratio (TTM)",
        "EPS (TTM)",
        "Earnings Date",
        "Forward Dividend & Yield",
        "Ex-Dividend Date",
        "1y Target Est"
    ]
    table_values = {
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    }
    counter = 0
    for td in table_data:
        if td['class'] == "Ta(end)":
            table_values[counter] = td.contents
            print(table_values[counter])
            counter += 1

    #FIX TABLE


    #RETURN JSON
    return {
        'input-status' : input_status,
        'url' : url,
        'headers' : headers,
        'market-price' : market_price,
        'market-change' : market_change,
        'market-percentage' : market_percentage,
        
        'graph-url' : graph_url,
        'interval' : interval,
        'range' : range,
        'graph-json' : graph_json,

        'table-json' : table_json
    }

if __name__ == "__main__":
    app.run(port=5000)
    #app.run(host="192.168.86.84", port=5000)