import unittest
from datacollector.yahoo_finance import YahooConnector


class YahooFinanceTestCase(unittest.TestCase):

     def setUp(self):
         self.connector = YahooConnector('IBEX35')

    def test_get_IBEX_components(self):
        components = self.connector.get_components()
        # En el caso del IBEX tenemos que tener 35 componentes
        self.assertEqual(len(components), 35)

    def test_get_IBEX_number_of_days(self):
        
        self.connector.get_data()
