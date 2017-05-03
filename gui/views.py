#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
List of views and widgets
author: Manuel Antonio Castro
website: www.institutoibt.com
created: May 3,  2017
"""

import logging
from PyQt5.QtCore import Qt
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


class CustomNetworkView(ApplicationTableView):

    def __init__(self, parent):
        self.view = QTableView()
        self.parent = parent
        self.cnmodel = models.CustomNetwork(self.parent.connection)
        self.view.setModel(self.cnmodel.getModel())
        self.view.setItemDelegate(QSqlRelationalDelegate(self.view))
        self._formatTable()
        super().__init__(self.view)
        self.view.selectionModel().selectionChanged.connect(self.selChanged)

    def _formatTable(self):
        super()._formatTable()
        self.view.hideColumn(0)

    def selChanged(self, event, selected):
        import ipdb; ipdb.set_trace()
        log.debug(selected)



class CustomNetworkComponentView(ApplicationTableView):

    def __init__(self, parent):
        self.view = QTableView()
        self.parent = parent
        self.cnmodel = models.Components(self.parent.connection)
        self.view.setModel(self.cnmodel.getModel())
        self.view.setItemDelegate(QSqlRelationalDelegate(self.view))
        self._formatTable()
        super().__init__(self.view)
