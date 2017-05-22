"""
This is the start point of the application. From here we invoke several
modules in order to get out the functionality

@author: Manuel Castro
@email: manuel.ant.castro@gmail

"""
import os
import sys
import datetime
import pytz
import argparse

from network_engine import compute_network
from datacollector.yahoo_finance import YahooConnector
from gui.nonrealplotting import paint
from gui import coreapp, connection

import logging.config
logging.config.fileConfig('logging.conf')
log = logging.getLogger('simpleDevelopment')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--migrate", help="Create the tables",
                        action="store_true")
    parser.add_argument("--destroy", help="Destroy database",
                        action="store_true")
    args = parser.parse_args()
    if args.migrate:
        connection.create_database()
    elif args.destroy:
        connection.delete_database()
    else:
        log.info('Starting application...')
        coreapp.startapp()

    # start_date = datetime.datetime(2017, 1, 1, 0, 0, 0, 0, pytz.utc)
    # end_date = datetime.datetime.today().utcnow()
    # conn = YahooConnector('IBEX35')
    # close_data_frame = conn.get_data('Close', start_date, end_date)
    # close_data_frame_IBEX = conn.get_component_data('^IBEX', 'Close',
    #                                                 start_date, end_date)
    # compute_network.STEP = 1
    # compute_network.HISTORIAL_NUMBER_OF_ROWS = 15
    # correlation_means, correlation_std, tree = compute_network.\
    #     build(close_data_frame)
    # # paint(close_data_frame_IBEX, correlation_means, correlation_std)

    # paint_network(tree, close_data_frame.columns.tolist())


if __name__ == '__main__':
    main()
