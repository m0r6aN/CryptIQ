import requests

def fetch_market_data(symbol):
    response = requests.get(f'https://api.coingecko.com/api/v3/simple/price', params={
        'ids': symbol,
        'vs_currencies': 'usd',
    })
    return response.json()
