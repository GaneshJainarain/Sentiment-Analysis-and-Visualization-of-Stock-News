from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


finvis_url = 'https://finviz.com/quote.ashx?t='
tickers = ['SPY', 'AAPL', 'FB']

for ticker in tickers:
    url = finvis_url + ticker

    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)
    html = BeautifulSoup(response, 'html')
    print(html)

    break