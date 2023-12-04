from flask import Flask
from flask import request
import requests
from bs4 import BeautifulSoup
import json
from urllib.request import Request, urlopen

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_stock_info():
    stock    = str(request.args.get('stock')).strip().upper()
    url = f'https://finance.yahoo.com/quote/{stock}?p={stock}'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'}
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return {
        'stock' : url,
        'headers' : header
    }


