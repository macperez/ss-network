from PyQt5.QtCore import Qt
from PyQt5.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
                         QSqlRelationalTableModel, QSqlTableModel)
from PyQt5.QtWidgets import QTableView


class CustomNetwork(object):

    def __init__(self, connection):
        self.connection = connection

        self.model = QSqlTableModel()
        self.model.setTable('customnetwork')
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "id")
        self.model.setHeaderData(1, Qt.Horizontal, "name")
        self.model.setHeaderData(2, Qt.Horizontal, "description")

    def getView(self):
        view = QTableView()
        view.setModel(self.model)
        view.setItemDelegate(QSqlRelationalDelegate(view))
        view.setWindowTitle(title)
        return view

    def getView(self):
        view = QTableView()
        view.setModel(self.model)
        view.setWindowTitle("Custom networks")
        return view
