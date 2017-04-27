
import os
import logging
import config

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


log = logging.getLogger(__name__)


def create_tables ():

    log.debug("Creating tables in database")
    query = QSqlQuery()
    query.exec_("create table sector(id int primary key, "
                "name varchar(50) NOT NULL, description varchar(80))")
    query.exec_("insert into sector values(1, 'HealthCare', 'Salud')")
    query.exec_("insert into sector values(2, 'Energy', 'Energía')")
    query.exec_("insert into sector values(3, 'Bank', 'Banca')")


    query.exec_("create table ticket(id int primary key, code varchar(10) NOT NULL, description varchar(80), sector int)")
    query.exec_("insert into employee values(1, 'GAS.MC', 'GAS NATURAL', 2)")
    query.exec_("insert into employee values(2, 'SAN.MC', 'Banco Santander',3)")




    query.exec_("create table custom_network(id int primary key, "
                "name varchar(50) NOT NULL, description varchar(20))")

    query.exec_("insert into custom_network values(1, 'IBEX35', 'Primer ejemplo')")
    query.exec_("insert into custom_network values(2, 'CAC', 'Segundo ejemplo')")

    query.exec_("create table component (id int primary key,"
                                             "imagefile int,"
                                             "location varchar(20),"
                                             "country varchar(20),"
                                             "description varchar(100))");



def createConnection():
    log.debug("Connecting to database")
    db = QSqlDatabase.addDatabase('QSQLITE')
    # db.setDatabaseName(':memory:') # RAM database, bien para tests
    if os.path.isfile(config.DATABASE_NAME):
        iscreated = True
    else:
        iscreated = False
        db.setDatabaseName('nt.db')
    if not db.open():
        QMessageBox.critical(None, "Cannot open database",
                "Unable to establish a database connection.\n"
                "This example needs SQLite support. Please read the Qt SQL "
                "driver documentation for information how to build it.\n\n"
                "Click Cancel to exit.",
                QMessageBox.Cancel)
        return False

    if not iscreated:
        create_tables()
    return True
