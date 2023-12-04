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
    graph = str(request.args.get('graph')).strip().upper()
    
    input_status = "VALID"
    print(stock)
    if stock == "NONE" or stock == "":
        input_status = "INVALID"
        return {'input-status' : input_status}
    
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

    graph
    market_graph = ""
    if(graph == "TRUE"):
        market_graph = "YAY"
    
    return {
        'input-status' : input_status,
        'url' : url,
        'headers' : headers,
        'market-price' : market_price,
        'market-change' : market_change,
        'market-percentage' : market_percentage,
        
        'market-graph' : market_graph
    }

if __name__ == "__main__":
    app.run(port=5000)
