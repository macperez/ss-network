"""
This is the start point of the application. From here we invoke several
modules in order to get out the functionality

@author: Manuel Castro
@email: desarrollo@institutoibt.come

"""
import datetime
import pytz
import argparse
from network_engine import compute_network
from datacollector.yahoo_finance import YahooConnector
from gui.nonrealplotting import paint


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--paintnetwork", help="paint the network graph",
                        action="store_true")
    args = parser.parse_args()
    if args.paintnetwork:
        print("Network will be exported to a file")

    start_date = datetime.datetime(2014, 1, 1, 0, 0, 0, 0, pytz.utc)
    end_date = datetime.datetime.today().utcnow()

    conn = YahooConnector('IBEX35')
    close_data_frame = conn.get_data('Close', start_date, end_date)
    close_data_frame_IBEX = conn.get_component_data('^IBEX', 'Close',
                                                    start_date, end_date)

    compute_network.STEP = 3
    compute_network.HISTORIAL_NUMBER_OF_ROWS = 15
    correlation_means, correlation_std = compute_network.\
        build(close_data_frame)

    paint(close_data_frame_IBEX, correlation_means, correlation_std)


if __name__ == '__main__':
    main()
