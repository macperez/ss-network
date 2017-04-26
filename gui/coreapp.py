#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Skeleton of the application

author: Manuel Antonio Castro
website: www.institutoibt.com
last edited: March 31,  2017
"""

import sys
import logging

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction,\
                            QApplication, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    '''
    The main window cointains all the execution environment.
    Several parts are criticall
    '''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # textEdit = QTextEdit()
        # self.setCentralWidget(textEdit)
        self.exitAction = QAction(QIcon('images/exit24'), 'Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)

        self.__init_menu()
        self.statusBar()


        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.exitAction)

        self.resize(600, 500)
        self.__center()
        self.setWindowTitle('Scientia Network Tool')
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     'Are you sure to quit?',
                                     QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def __init_menu(self):
        self.menubar = self.menuBar()

        filemenu = self.menubar.addMenu('&File')
        filemenu.addAction(self.exitAction)



    def __center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def startapp():
    app = QApplication(sys.argv)
    # muy importante instanciar y asignar a una variable porque si no, no se
    # pinta la ventana
    logger = logging.getLogger('simpleDevelopment')
    logger.info('Starting application...')
    main = MainWindow()
    sys.exit(app.exec_())
    return app


if __name__ == '__main__':
    startapp()
