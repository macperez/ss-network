"""
Yahoo finance function utilities
The data coming from here come from Yahoo servers but they are not
real-time data, but it provides convenient apis to fetch historical day-by-day
stock data. They are useful for past-case studies.

@author: Manuel Castro
@email: desarrollo@institutoibt.come

"""

import datetime as dt
import urllib.request as req
import pytz
import pandas as pd
from bs4 import BeautifulSoup


from pandas_datareader import DataReader


INDEX_SITES = {
    'IBEX35': 'https://es.wikipedia.org/wiki/IBEX_35',
}


class YahooConnector (object):
    """
    A base storage class, providing some default behaviors that all other
    storage systems can inherit or override, as necessary.
    A Yahoo connector class, providing all the data of a given index.
    Use a scraping system in order to collect the index components.
    """

    def __init__(self, start_date, end_date, step=1):
         self.start_date = start_date
         self.end_date = end_date
         self.step = step


    def scrape_list_IBEX(self):
        """
        Scrape the web source for obtaining the componentes of a given index
        """
        hdr = {'User-Agent': 'Mozilla/5.0'}
        request = req.Request('https://es.wikipedia.org/wiki/IBEX_35', headers=hdr)
        page = req.urlopen(request)
        soup = BeautifulSoup(page, "html.parser")

        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = {}
        for row in table.findAll('tr'):
            col = row.findAll('td')
            if len(col) > 0:
                ticker = str(col[0].string.strip())
                name = str(col[1].string.strip())
                tickers[ticker] = name
        return tickers

    def get_ibex35_data(self, type):
        tickers = self.scrape_list_IBEX()
        data = DataReader(list(tickers.keys()), 'yahoo', self.start_date,
            self.end_date)
        #close_df = data['Close']
        type_data = data[type].iloc[::step]
        return type_data



if __name__ == '__main__':
    START = dt.datetime(2017, 1, 1, 0, 0, 0, 0, pytz.utc)
    END = dt.datetime.today().utcnow()
    yahoo = YahooConnector(START, END )
    df = yahoo.get_ibex35_data('Close')
    print df
