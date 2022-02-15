from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import ssl
import matplotlib.pyplot as plt

#handling ssl error we kept getting 
ssl._create_default_https_context = ssl._create_unverified_context

## Getting Finviz Article Data
finvis_url = 'https://finviz.com/quote.ashx?t='
tickers = ['AAPL', 'NVDA', 'SPY', 'FB', 'AMD']

news_tables = {}
for ticker in tickers:
    url = finvis_url + ticker

    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response,features="lxml")
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table
    

## Parsing and Manipulating Finviz Data
# Parse data that we have gotten from Beautiful Soup
# Then get it into an understandable format that we can extract the title, timestamp
# so we can apply Sentimental analysis on.

parsed_data = []

for ticker, news_table in news_tables.items():
#iterating over our dictionary
#iterating over key value pairs


    for row in news_table.findAll('tr'):
#for all the rows that we can find we scrape
#anchor tag
        title = row.a.text
        date_data = row.td.text.split(' ')

#either singular timestamp 04:00
#or timestamp with data Jun-18-21 04:00
        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

#for each row, we append the data we want
        parsed_data.append([ticker, date, time, title])

#Creating our Pandas data frame and setting our columns
df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])
#print(df.head)

#Applying Sentimental Analysis
#Goal is to apply the sentimental analysis on the news titles we are obtaining

vader = SentimentIntensityAnalyzer()
#lamba function give me the polairty score but i dont care about all the values just the compund score
f = lambda title: vader.polarity_scores(title)['compound']
#Now we can apply the function on our dataframe
df['compound'] = df['title'].apply(f)
print(df)

df['date'] = pd.to_datetime(df.date).dt.date
plt.figure(figsize=(16,14))
mean_df = df.groupby(['ticker', 'date']).mean()
mean_df = mean_df.unstack()
mean_df = mean_df.xs('compound', axis="columns").transpose()
mean_df.plot(kind='bar')
plt.show()
#print(mean_df)









