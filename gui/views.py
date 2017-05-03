#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
List of views and widgets
author: Manuel Antonio Castro
website: www.institutoibt.com
created: May 3,  2017
"""

import logging
from PyQt5.QtWidgets import QTableView, QHeaderView
from PyQt5.QtSql import QSqlRelationalDelegate
from gui import models

log = logging.getLogger('simpleDevelopment')


class ApplicationTableView(object):
    def __init__(self, view):
        self.view = view
    def getView(self):
        return self.view

    def _formatTable(self):
        maxcols = self.view.horizontalHeader().count()
        log.debug("Number of columns displayed {}".format(maxcols))
        for col in range (maxcols):
            self.view.horizontalHeader().setSectionResizeMode(col,
                                                         QHeaderView.Stretch)

        self.view.hideColumn(0)




class CustomNetworkView(ApplicationTableView):

    def __init__(self, parent):
        self.view = QTableView()
        self.parent = parent
        self.cnmodel = models.CustomNetwork(self.parent.connection)
        self.view.setModel(self.cnmodel.getModel())
        self.view.setItemDelegate(QSqlRelationalDelegate(self.view))
        self._formatTable()
        super().__init__(self.view)



class CustomNetworkComponentView(ApplicationTableView):

    def __init__(self, parent):
        self.view = QTableView()
        self.parent = parent
        self.cnmodel = models.Components(self.parent.connection)
        self.view.setModel(self.cnmodel.getModel())
        self.view.setItemDelegate(QSqlRelationalDelegate(self.view))
        self._formatTable()
        super().__init__(self.view)
