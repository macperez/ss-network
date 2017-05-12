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
from PyQt5.QtWidgets import QTableView, QHeaderView, QAbstractItemView, \
                            QMessageBox
from PyQt5.QtSql import QSqlRelationalDelegate

from gui import models

log = logging.getLogger('simpleDevelopment')


class ApplicationTableView(object):
    def __init__(self, view):
        self.view = view
        self.view.setEditTriggers(QAbstractItemView.NoEditTriggers)

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
        self.view.selectionModel().selectionChanged.connect(self.selChanged)
        self.view.doubleClicked.connect(self.manageDoubleClick)
        self._formatTable()
        self.dependantView = parent.cncview
        self.customnetwork_id_selected = -1
        super().__init__(self.view)

    def _formatTable(self):
        super()._formatTable()
        self.view.hideColumn(0)

    def manageDoubleClick(self):
        log.debug("doubleClick detected")

    def selChanged(self, event, selected):
        indexes = event.indexes()
        self.parent.deletebutton.setEnabled(True)
        self.parent.editbutton.setEnabled(True)
        if indexes:
            index = indexes[0]
            rowidx = index.row()
            self.view.selectRow(rowidx)
            cn_id = self.cnmodel.getModel().index(rowidx, 0).data()
            cn_name = self.cnmodel.getModel().index(rowidx, 1).data()
            self.parent.connection.open()
            dependant_model = self.dependantView.cnmodel.getModel()
            dependant_model.setFilter("customnetwork_id={}".format(cn_id))

            self.parent.connection.close()
            self.customnetwork_id_selected = cn_id

    def remove(self):
        reply = QMessageBox.question(self.parent, 'Delete custom network',
            "Are you sure to remove?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            log.debug("The {} customnetwork is going to be deleted" \
                .format(self.customnetwork_id_selected))

            ok = self.parent.cncview.cnmodel.delete_cnc(self.customnetwork_id_selected)
            if ok:
                self.cnmodel.delete_cn(self.customnetwork_id_selected)

    def get_selected_custom_network(self):
        return self.customnetwork_id_selected

class CustomNetworkComponentView(ApplicationTableView):

    def __init__(self, parent):
        self.view = QTableView()
        self.parent = parent
        self.cnmodel = models.Components(self.parent.connection)
        self.view.setModel(self.cnmodel.getModel())
        self.view.setItemDelegate(QSqlRelationalDelegate(self.view))
        self._formatTable()
        super().__init__(self.view)
