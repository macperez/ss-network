import logging
from PyQt5.QtCore import Qt
from PyQt5.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
                         QSqlRelationalTableModel, QSqlTableModel)
from PyQt5.QtWidgets import QTableView, QHeaderView, QTreeView

log = logging.getLogger('simpleDevelopment')

GENERIC_SECTOR_CODE_ID = 1000

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

    def create(self, name, description):
        # TODO: capturar excepciones de error que se pueden dar
        query = QSqlQuery()
        last = self.model.rowCount()
        id = last + 1
        self.connection.open()
        query_str = "insert into customnetwork values ({}, '{}', '{}');"\
            .format(id, name, description)
        log.debug("Query: {}".format(query_str))
        query.exec_(query_str)
        self.model.select()
        self.connection.close()
        # FIXME: hacer una query primero y construir un objeto
        return id

    def update(self,id, name, description):
        # TODO: capturar excepciones de error que se pueden dar
        query = QSqlQuery()
        self.connection.open()
        sql = """UPDATE customnetwork SET name = ?, description = ?
                 WHERE id = ?;
              """
        query.prepare(sql)
        query.addBindValue(name)
        query.addBindValue(description)
        query.addBindValue(id)
        ok = query.exec_()
        self.model.select()
        self.connection.close()
        return ok


    def delete_cn(self, customnetwork_id_selected):
        query = QSqlQuery()
        self.connection.open()
        query.prepare('delete from customnetwork where id = ?;')
        query.addBindValue(customnetwork_id_selected)
        ok = query.exec_()
        self.model.select()
        self.connection.close()
        return ok

    @staticmethod
    def getObject(connection, customnetwork_id=-1):
        if customnetwork_id < 0:
            return {}
        cnc_object = {}
        query = QSqlQuery()
        connection.open()
        query.prepare('select id, name, description from customnetwork where id = ?;')
        query.addBindValue(customnetwork_id)
        if query.exec_():
            query.next()
            cnc_object['id'] = int(query.value(0))
            cnc_object['name'] = str(query.value(1))
            cnc_object['description'] = str(query.value(2))

        query_str = """select c.id, c.ticket, n.id, n.name
        from customnetwork n, component c,
        customnetwork_component nc where
        c.id = nc.component_id and
        n.id = nc.customnetwork_id and
        n.id = ?;"""

        log.debug("QUERY: {}".format(query_str))
        query.prepare(query_str)
        query.addBindValue(customnetwork_id)
        cnc_object['components'] = []
        if query.exec_():
            while query.next():
                comp = {}
                comp['id'] = int(query.value(0))
                comp['ticket'] = str(query.value(1))
                cnc_object['components'].append(comp)
        connection.close()

        return cnc_object



class Components(object):

    def __init__(self, connection):
        self.connection = connection
        self.model = QSqlRelationalTableModel()
        self.model.setTable('customnetwork_component')
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.setRelation(0, QSqlRelation('component', 'id', 'ticket'))
        self.model.setRelation(1, QSqlRelation('customnetwork', 'id', 'name'))
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "Ticket")

    def getModel(self):
        return self.model

    def create(self, customnetwork_id, tickets):
        # TODO: capturar excepciones de error que se pueden dar
        log.debug(tickets)
        query = QSqlQuery()
        last = self.model.rowCount()
        id = last + 1
        self.connection.open()
        for ticket in tickets:
            comp_id = self._insert_component_table(query, ticket)
            ok = self.\
                _insert_customernetwork_component_table(query,
                                                        customnetwork_id,
                                                        comp_id)

        self.model.select()
        self.connection.close()

        return id

    def _insert_customernetwork_component_table(self, query, customnetwork_id,
                                                comp_id):
        query.prepare('insert into customnetwork_component values (?,?);')
        query.addBindValue(comp_id)
        query.addBindValue(customnetwork_id)
        return query.exec_()

    def _insert_component_table(self, query, ticket):
        ok = query.exec_("select id from component;")
        id = 0
        if ok:
            query.last()
            last_id = int(query.value(0))
            id = last_id + 1
        query.prepare('insert into component values (?,?,?,?);')
        query.addBindValue(id)
        query.addBindValue(ticket)
        query.addBindValue('_generic_description_')
        query.addBindValue(GENERIC_SECTOR_CODE_ID)
        if query.exec_():
            return id
        else:
            return -1

    def update_components(self, id, tickets):
        # TODO: capturar excepciones de error que se pueden dar
        query = QSqlQuery()
        self.connection.open()
        sql = """UPDATE customnetwork SET name = ?, description = ?
                 WHERE id = ?;
              """
        query.prepare(sql)
        query.addBindValue(name)
        query.addBindValue(description)
        query.addBindValue(id)
        ok = query.exec_()
        self.model.select()
        self.connection.close()
        return ok

    def delete_cnc(self, customnetwork_id_selected):
        query = QSqlQuery()
        self.connection.open()
        query.prepare('delete from customnetwork_component where customnetwork_id = ?;')
        query.addBindValue(customnetwork_id_selected)
        ok = query.exec_()
        self.model.select()
        self.connection.close()
        return ok
