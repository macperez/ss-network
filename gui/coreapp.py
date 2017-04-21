#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Skeleton of the application

author: Manuel Antonio Castro
website: www.institutoibt.com
last edited: March 31,  2017
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # textEdit = QTextEdit()
        # self.setCentralWidget(textEdit)

        exitAction = QAction(QIcon('images/exit24'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()
        self.menubar = self.menuBar()
        filemenu = self.menubar.addMenu('&File')
        filemenu.addAction(exitAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        self.setGeometry(500, 300, 350, 250)
        self.setWindowTitle('Scientia Network Tool')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # muy importante instanciar y asignar a una variable porque si no, no se
    # pinta la ventana
    main = MainWindow()
    sys.exit(app.exec_())
