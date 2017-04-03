import unittest
import datetime
import pytz
from datacollector.yahoo_finance import YahooConnector


class YahooFinanceTestCase(unittest.TestCase):

     def setUp(self):
         self.connector = YahooConnector('IBEX35')

    def test_get_IBEX_components(self):
        components = self.connector.get_components()
        # En el caso del IBEX tenemos que tener 35 componentes
        self.assertEqual(len(components), 35)

    def test_get_IBEX_number_of_days(self):
        # Obtenemos un pandas dataframe con los datos de cierre
        start_date = datetime.datetime(2017, 1, 1, 0, 0, 0, 0, pytz.utc)
        end_date = datetime.datetime.today().utcnow()

        closedata = self.connector.get_data()


    # def tearDown(self):
    #     self.connector.close()
