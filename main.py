"""
This is the start point of the application. From here we invoke several
modules in order to get out the functionality

@author: Manuel Castro
@email: desarrollo@institutoibt.come

"""
from datacollector.yahoo_finance import YahooConnector
from network_engine import compute_network
from gui.nonrealplotting import paint

def main():
    start_date = dt.datetime(2017, 1, 1, 0, 0, 0, 0, pytz.utc)
    end_date = dt.datetime.today().utcnow()
    step = 2
    financial_connector = YahooConnector(start_date, end_date, step)

    close_data_frame = financial_connector.get_ibex35_data('Close')

    graphical_set_of_data = compute_network.build(close_data_frame)

    paint(graphical_set_of_data)



if __name__== '__main__':
    main()
