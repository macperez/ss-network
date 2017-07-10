import logging
import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
                         QSqlRelationalTableModel, QSqlTableModel)
from PyQt5.QtWidgets import QTableView, QHeaderView, QTreeView
from core import utils


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
        query_str = """INSERT INTO customnetwork VALUES ({}, '{}', '{}');"""\
            .format(id, name, description)
        log.debug("Query: {}".format(query_str))
        query.exec_(query_str)
        self.model.select()
        self.connection.close()
        # FIXME: hacer una query primero y construir un objeto
        return id

    def update(self, id, name, description):
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

    def delete_cn(self, customnetwork_id):
        query = QSqlQuery()
        self.connection.open()
        query.prepare('delete from customnetwork where id = ?;')
        query.addBindValue(customnetwork_id)
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
        query.prepare('SELECT id, name, description from customnetwork '
                      'WHERE id = ?;')
        query.addBindValue(customnetwork_id)
        if query.exec_():
            query.next()
            cnc_object['id'] = int(query.value(0))
            cnc_object['name'] = str(query.value(1))
            cnc_object['description'] = str(query.value(2))

        query_str = """SELECT c.id, c.ticket, n.id, n.name
        FROM customnetwork n, component c,
        customnetwork_component nc WHERE
        c.id = nc.component_id AND
        n.id = nc.customnetwork_id AND
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
        sql = """DELETE FROM customnetwork_component
                 WHERE customnetwork_id = ?;
              """
        query.prepare(sql)
        query.addBindValue(id)
        ok = query.exec_()
        if ok:
            for ticket in tickets:
                sql = "SELECT id, ticket FROM component WHERE ticket = '{}';"\
                    .format(ticket)
                if query.exec_() and query.next():
                    component_id = int(query.value(0))
                    query.clear()
                    sql = """INSERT into customnetwork_component
                    VALUES (?, ?);
                    """
                    query.prepare(sql)
                    query.addBindValue(component_id)
                    query.exec_()
                else:
                    comp_id = self._insert_component_table(query, ticket)
                    ok = self.\
                        _insert_customernetwork_component_table(query,
                                                                id,
                                                                comp_id)

        self.model.select()
        self.connection.close()
        return ok

    def delete_cnc(self, customnetwork_id):
        query = QSqlQuery()
        self.connection.open()
        query_str = 'delete from customnetwork_component where '
        ' customnetwork_id = ?;'
        query.prepare(query)
        query.addBindValue(customnetwork_id)
        ok = query.exec_()
        self.model.select()
        self.connection.close()
        return ok


class NetWorkParameters(object):
    def __init__(self, connection):
        self.connection = connection

    def __init__(self, connection, step, history,
                 start_date, end_date, customnetwork_id):
        self.connection = connection
        self.object = {'step': step,
                       'history': history,
                       'start_date': start_date,
                       'end_date': end_date,
                       'customnetwork_id': customnetwork_id}

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def save(self):
        log.debug("Saving params")
        self.connection.open()
        query = QSqlQuery()
        ok = query.exec_("SELECT id FROM networkpreferences;")
        id = 0
        if ok and query.next():
            query.last()
            last_id = int(query.value(0))
            id = last_id + 1
        start_date_txt = self.object['start_date']
        end_date_txt = self.object['end_date']

        step = int(self.object['step'])
        history = int(self.object['history'])
        customnetwork_id = int(self.object['customnetwork_id'])

        query.prepare('insert into networkpreferences values (?,?,?,?,?);')
        query.addBindValue(id)
        query.addBindValue(step)
        query.addBindValue(history)
        query.addBindValue(utils.change_date_format(start_date_txt))
        query.addBindValue(utils.change_date_format(end_date_txt))
        query.addBindValue(customnetwork_id)

        ok = query.exec_()
        log.error(query.lastError().text())    

        self.connection.close()
        return ok

    @staticmethod
    def getObject(connection, customnetwork_id=-1):
        if customnetwork_id < 0:
            return {}
        cnc_object = {}
        query = QSqlQuery()
        connection.open()
        query_str = """SELECT id, step, historical, start_date, end_date
        FROM networkpreferences
        WHERE
        customnetwork_id = ?;
        """
        log.debug("QUERY: {}".format(query_str))
        query.prepare(query_str)
        query.addBindValue(customnetwork_id)
        if query.exec_() and query.next():
            cnc_object['id'] = int(query.value(0))
            cnc_object['step'] = str(query.value(1))
            cnc_object['historical'] = str(query.value(2))
            cnc_object['start_date'] = str(query.value(3))
            cnc_object['end_date'] = str(query.value(4))
        connection.close()

        return cnc_object
