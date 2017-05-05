import logging
from PyQt5.QtCore import Qt
from PyQt5.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
                         QSqlRelationalTableModel, QSqlTableModel)
from PyQt5.QtWidgets import QTableView, QHeaderView, QTreeView

log = logging.getLogger('simpleDevelopment')


class CustomNetwork(object):

    def __init__(self, connection):
        self.connection = connection

        self.model = QSqlTableModel()
        self.model.setTable('customnetwork')
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select()
        # self.model.setHeaderData(0, Qt.Horizontal, "id")
        self.model.setHeaderData(1, Qt.Horizontal, "Name")
        self.model.setHeaderData(2, Qt.Horizontal, "Description")

    def getModel(self):
        return self.model


class Components(object):

    def __init__(self, connection):
        self.connection = connection
        self.model = QSqlRelationalTableModel()
        self.model.setTable('customnetwork_component')
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.setRelation(0, QSqlRelation('component', 'id', 'ticket'))
        self.model.setRelation(1, QSqlRelation('customnetwork', 'id', 'name'))
        self.model.select()
        # self.model.setHeaderData(0, Qt.Horizontal, "id")
        self.model.setHeaderData(0, Qt.Horizontal, "Ticket")

    def getModel(self):
        return self.model
