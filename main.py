"""
This is the start point of the application. From here we invoke several
modules in order to get out the functionality

@author: Manuel Castro
@email: desarrollo@institutoibt.come

"""
import datetime
import pytz
from network_engine import compute_network
from datacollector.yahoo_finance import YahooConnector
from gui.nonrealplotting import paint

def main():
    start_date = datetime.datetime(2017, 1, 1, 0, 0, 0, 0, pytz.utc)
    end_date = datetime.datetime.today().utcnow()

    conn = YahooConnector('IBEX35')
    close_data_frame = conn.get_data(start_date, end_date, 1, 'Close')
    print (close_data_frame)

    compute_network.STEP = 2
    compute_network.HISTORIAL_NUMBER_OF_ROWS = 14
    matrix = compute_network.build(close_data_frame)

    #paint(graphical_set_of_data)



if __name__== '__main__':
    main()
