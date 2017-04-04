import unittest
import datetime
import pytz
import pandas as pd
import numpy as np
from datacollector.yahoo_finance import YahooConnector


class YahooFinanceTestCase(unittest.TestCase):

    def setUp(self):
         self.connector = YahooConnector('IBEX35')

    def test_get_IBEX_components(self):
        import ipdb; ipdb.set_trace()
        components = self.connector.get_components()

        # En el caso del IBEX tenemos que tener 35 componentes
        self.assertEqual(len(components), 35)

    def _test_get_IBEX_number_of_days(self):
        # Obtenemos un pandas dataframe con los datos de cierre
        start_date = datetime.datetime(2017, 1, 1, 0, 0, 0, 0, pytz.utc)
        end_date = datetime.datetime.today().utcnow()
        closedata = self.connector.get_data()

    # def tearDown(self):
    #     self.connector.close()

class NetworkTestCase(unittest.TestCase):


    def test_total_correlation(self):
        dates = pd.date_range('20130101', periods=4)
        df = pd.DataFrame(np.ones((4,3)),
                          index=dates,
                          columns=list('ABC'))
        # En el caso del IBEX tenemos que tener 35 componentes
        print (df)
        #self.assertEqual(len(components), 35)