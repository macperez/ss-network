"""
Yahoo finance function utilities
The data coming from here come from Yahoo servers but they are not
real-time data, but it provides convenient apis to fetch historical day-by-day
stock data. They are useful for past-case studies.

:author: Manuel Castro
:email: desarrollo@institutoibt.come

"""
import urllib.request as req
import pandas as pd
from bs4 import BeautifulSoup
from pandas_datareader import DataReader


INDEX_SITES = {
    'IBEX35': 'https://es.wikipedia.org/wiki/IBEX_35',
    'DAX30' : 'https://es.wikipedia.org/wiki/DAX'
}


class YahooConnector:
    """
    A base storage class, providing some default behaviors that all other
    storage systems can inherit or override, as necessary.
    A Yahoo connector class, providing all the data of a given index.
    Use a scraping system in order to collect the index components.
    """

    def __init__(self):
        pass
    def __init__(self, indexname):
        self.indexname = indexname

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
                ticker = str(col[0].string.strip()) + '.MC'
                name = str(col[1].string.strip())
                tickers[ticker] = name
        return tickers

    def get_component_data(self, component_symbol, type, startdate, enddate):
        '''
        Get the data of a given component.
        '''
        data = DataReader(component_symbol, 'yahoo', startdate,
            enddate)
        return data[type]

    def get_components(self):
        '''
        Get the components of a given index
        '''
        if self.indexname == 'IBEX35':
            components = self.scrape_list_IBEX()

        return components

    def get_data(self, type, startdate, enddate):
        '''
        Return the data of interest.
        :param startdate: the initial date for the set
        :param enddate: the final date for the set
        :param step: the minimal amount of time. For yahoo api is one day. So
            step is the multiple of this unit.
        :param type: the final date for the set

        '''
        tickers = self.get_components()
        data = DataReader(list(tickers.keys()), 'yahoo', startdate,
            enddate)
        return data[type]
