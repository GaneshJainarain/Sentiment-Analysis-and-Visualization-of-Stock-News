from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

## Getting Finviz Article Data
finvis_url = 'https://finviz.com/quote.ashx?t='
tickers = ['SPY', 'AAPL', 'FB']

news_tables = {}
for ticker in tickers:
    url = finvis_url + ticker

    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response,features="lxml")
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table
    break

## Parsing and Manipulating Finviz Data
# Parse data that we have gotten from Beautiful Soup
# Then get it into an understandable format that we can extract the title, timestamp
# so we can apply Sentimental analysis on.
parsed_data = []

for ticker, news_table in news_tables.items():

    for row in news_table.findAll('tr'):

        title = row.a.text
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([ticker, date, time, title])
print(parsed_data)







