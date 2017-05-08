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
        for col in range(maxcols):
            self.view.horizontalHeader().\
                setSectionResizeMode(col, QHeaderView.Stretch)


class CustomNetworkView(ApplicationTableView):

    def __init__(self, parent):
        self.view = QTableView()
        self.parent = parent
        self.cnmodel = models.CustomNetwork(self.parent.connection)
        self.view.setModel(self.cnmodel.getModel())
        self.view.setItemDelegate(QSqlRelationalDelegate(self.view))
        self._formatTable()
        self.view.selectionModel().selectionChanged.connect(self.selChanged)
        self.dependantView = parent.cncview
        super().__init__(self.view)

    def _formatTable(self):
        super()._formatTable()
        self.view.hideColumn(0)

    def selChanged(self, event, selected):
        if event.count() == 1:
            index = event.indexes()[0]
            rowidx = index.row()
            cn_id = self.cnmodel.getModel().index(rowidx, 0).data()
            cn_name = self.cnmodel.getModel().index(rowidx, 1).data()
            self.parent.connection.open()
            dependant_model = self.dependantView.cnmodel.getModel()
            dependant_model.setFilter("customnetwork_id={}".format(cn_id))
            self.parent.connection.close()



class CustomNetworkComponentView(ApplicationTableView):

    def __init__(self, parent):
        self.view = QTableView()
        self.parent = parent
        self.cnmodel = models.Components(self.parent.connection)
        self.view.setModel(self.cnmodel.getModel())
        self.view.setItemDelegate(QSqlRelationalDelegate(self.view))
        self._formatTable()
        super().__init__(self.view)
