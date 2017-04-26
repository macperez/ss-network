#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Skeleton of the application

author: Manuel Antonio Castro
website: www.institutoibt.com
last edited: March 31,  2017
"""
import os
import sys
import logging
import pkgutil
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction,\
                            QApplication, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QIcon
import datacollector

logging.config.fileConfig('logging.conf')
LOGGER = logging.getLogger('simpleDevelopment')

AVAILABLE_CONNECTORS = {}

for importer, modname, ispkg in \
    pkgutil.iter_modules(datacollector.__path__):
    LOGGER.debug("Found submodule {} (is a package: {})"\
        .format(modname,ispkg))
    module = __import__(modname)
    if not ispkg:
        AVAILABLE_CONNECTORS[modname] = module
    LOGGER.debug("Imported {0}".format(module))


class MainWindow(QMainWindow):
    '''
    The main window cointains all the execution environment.
    Several parts are critical and need to be here.
    '''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.__init_actions()
        self.__init_menu()

        self.statusBar()  # La primera llamada lo crea, las siguientes
                          # lo invocan solamente


        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.exitAction)

        self.resize(600, 500)
        self.__center()
        self.setWindowTitle('Scientia Network Tool')
        self.show()

    # FIXME: temporalmente desactivado
    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'Message',
    #                                  'Are you sure to quit?',
    #                                  QMessageBox.Yes |
    #                                  QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def __init_actions(self):
        self.exitAction = QAction(QIcon('gui/images/exit24.png'), 'Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)

        if 'yahoo_finance' in AVAILABLE_CONNECTORS:
            self.yahoo_connector_action = \
                QAction(QIcon('gui/images/yahoo_conn24.png'),
                              'Yahoo connector', self)
            self.yahoo_connector_action.setShortcut('Ctrl+Y')
            self.yahoo_connector_action.setStatusTip('Yahoo connection')
            self.yahoo_connector_action.triggered.\
                connect(self.__yahoo_connector)

    def __yahoo_connector(self):
        '''
        When the the Yahoo connection item is clicked come to here.
        '''
        yahoo_finance_module = AVAILABLE_CONNECTORS['yahoo_finance']
        # TODO: ver que hacer con el modulo aquí
        self.statusBar().clearMessage()
        self.statusBar().showMessage('Connected to Yahoo finance')


    def __init_menu(self):
        '''
        Initialize the menubar and its components.
        '''
        self.menubar = self.menuBar()
        filemenu = self.menubar.addMenu('&File')
        new_datasource_menu = filemenu.addMenu('&New Data source')
        new_datasource_menu.addAction(self.yahoo_connector_action)
        filemenu.addAction(self.exitAction)



    def __center(self):
        '''
        Center the main window in the middle of the screen.
        '''
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



def startapp():
    app = QApplication(sys.argv)
    # muy importante instanciar y asignar a una variable porque si no, no se
    # pinta la ventana

    LOGGER.info('Starting application...')
    main = MainWindow()
    sys.exit(app.exec_())
    return app


if __name__ == '__main__':
    startapp()
