#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Skeleton of the application

author: Manuel Antonio Castro
last edited: March 31,  2017
"""
import os
import sys
import logging
import pkgutil

from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QWidget,\
                            QApplication, QDesktopWidget, QMessageBox,\
                            QFrame, QSplitter, QHBoxLayout, QTextEdit,\
                            QVBoxLayout, QStyleFactory, QPushButton, \
                            QHeaderView, QGridLayout, QProgressBar


from PyQt5.QtGui import QIcon


from gui import models, views, dialogs, connection

import datacollector

log = logging.getLogger('simpleDevelopment')


AVAILABLE_CONNECTORS = {}

for importer, modname, ispkg in pkgutil.iter_modules(datacollector.__path__):
    log.debug("Found submodule {} (is a package: {})".format(modname, ispkg))
    module = __import__(modname)
    if not ispkg:
        AVAILABLE_CONNECTORS[modname] = module
    log.debug("Imported {0}".format(module))






class MainWindow(QMainWindow):
    '''
    The main window cointains all the execution environment.
    Several parts are critical and need to be here.
    '''
    def __init__(self):
        super().__init__()
        connected, db = connection.createConnection()
        if not connected:
            sys.exit(1)
        self.connection = db
        self.initUI()

        self.customnetwork_id_selected = -1

    def initUI(self):

        self.__init_actions()
        self.__init_menu()

        self.statusBar()  # La primera llamada lo crea, las siguientes
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.exitAction)
        self.toolbar.addAction(self.calculateNetworkAction)
        self.toolbar.addAction(self.exportNetworkAction)
        self.containerWidget = ContainerWidget(self)
        self.setCentralWidget(self.containerWidget)
        self.resize(900, 500)
        self.__center()
        self.setWindowTitle('Open Graph network Tool')
        self.show()
        self.connection.close()
        # self.customnetwork_id_selected = None

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     'Are you sure to quit?',
                                     QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.connection.close()
            event.accept()
        else:
            event.ignore()

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

        self.calculateNetworkAction = \
            QAction(QIcon('gui/images/calculation24.png'), 'Compute Network',
                    self)
        self.calculateNetworkAction.setShortcut('Ctrl+C')
        self.calculateNetworkAction.setStatusTip('Compute Network')
        self.calculateNetworkAction.triggered.connect(self.computeNetworkSlot)
        self.calculateNetworkAction.setEnabled(False)
        self.exportNetworkAction = \
            QAction(QIcon('gui/images/export24.png'), 'Export Network', self)
        self.exportNetworkAction.setShortcut('Ctrl+X')
        self.exportNetworkAction.setStatusTip('Export Network')
        self.exportNetworkAction.triggered.connect(self.exportNetworkSlot)
        self.exportNetworkAction.setEnabled(False)

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

    def computeNetworkSlot(self, event):
        log.debug("Opening network building preferences")
        step, history, start_date, end_date, ok = \
            dialogs.NetWorkParametersFormDialog.getData(self)
        if ok:
            log.debug("Opening network building preferences")
            pbb = dialogs.BackGroundTaskDialog.open(self)

    def exportNetworkSlot(self, event):
        pass


class ContainerWidget(QWidget):
    '''
    Main container of the center of the application
    It lay out all the subcontainers over the screens
    '''

    def __init__(self, main_window):
        super().__init__()
        self.parent = main_window
        self.connection = self.parent.connection
        self.cncview = views.CustomNetworkComponentView(self)
        self.cnview = views.CustomNetworkView(self)
        self.editbutton = None
        self.deletebutton = None
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)
        topleft = QFrame()
        topleft.setFrameShape(QFrame.StyledPanel)

        bottom = QFrame()
        bottom.setFrameShape(QFrame.StyledPanel)
        splitter1 = QSplitter(Qt.Horizontal)
        self.compmodel = models.Components(self.connection)
        self._setlayoutTopleft(topleft)
        splitter1.addWidget(topleft)
        splitter1.addWidget(self.cnview.getView())
        splitter1.setSizes([100, 200])

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)
        hbox.addWidget(splitter2)
        self.setLayout(hbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

    def _setlayoutTopleft(self, topleft_frame):

        horizontal_layout = QHBoxLayout()
        vertical_layout = QVBoxLayout()

        newbutton = QPushButton()
        newbutton.setIcon(QIcon('gui/images/plus-sign24.png'))
        self.editbutton = QPushButton()
        self.editbutton.setIcon(QIcon('gui/images/edit24.png'))
        self.editbutton.setEnabled(False)
        self.deletebutton = QPushButton()
        self.deletebutton.setIcon(QIcon('gui/images/delete24.png'))
        self.deletebutton.setEnabled(False)
        newbutton.clicked.connect(self.new_customnetwork_action)
        self.editbutton.clicked.connect(self.edit_customnetwork_action)
        self.deletebutton.clicked.connect(self.delete_action)

        vertical_layout.addWidget(newbutton)
        vertical_layout.addWidget(self.editbutton)
        vertical_layout.addWidget(self.deletebutton)
        horizontal_layout.addWidget(self.cncview.getView())
        horizontal_layout.addLayout(vertical_layout)
        topleft_frame.setLayout(horizontal_layout)

    def new_customnetwork_action(self):
        log.debug("new custom network action event")
        name, description, tickets, ok = \
            dialogs.CustomNetworkFormDialog.getData(self)
        if ok:
            customnetwork_id = self.cnview.cnmodel.create(name, description)
            self.cncview.cnmodel.create(customnetwork_id, tickets)

    def edit_customnetwork_action(self):
        log.debug("edit custom network action event")
        customnetwork_id = self.cnview.get_selected_custom_network()
        name, description, components, ok = \
            dialogs.CustomNetworkFormDialog.getData(self, customnetwork_id)
        if ok:
            ok = self.cnview.cnmodel.update(customnetwork_id,
                                            name, description)
            self.cncview.cnmodel.update_components(customnetwork_id,
                                                   components)

    def delete_action(self):
        self.cnview.remove()


def startapp():
    app = QApplication(sys.argv)
    # muy importante instanciar y asignar a una variable porque si no, no se
    # pinta la ventana
    main = MainWindow()
    sys.exit(app.exec_())
    return app




if __name__ == '__main__':
    startapp()
