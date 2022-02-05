from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


finvis_url = 'https://finviz.com/quote.ashx?t='
tickers = ['SPY', 'AAPL', 'FB']

news_tables = {}
for ticker in tickers:
    url = finvis_url + ticker

    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response, 'html')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table

    #print(html)
    break
print(news_tables)