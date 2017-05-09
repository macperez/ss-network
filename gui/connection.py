
import os
import logging
import config
from os.path import expanduser

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


log = logging.getLogger('simpleDevelopment')
HOME = expanduser("~")
PATH_TO_FILE = os.path.join(HOME, config.DATABASE_NAME)


def create_tables():
    log.debug("Creating tables in database")
    query = QSqlQuery()
    query.exec_("create table sector(id int primary key, "
                "name varchar(50) NOT NULL, description varchar(80))")
    query.exec_("insert into sector values(1, 'HealthCare', 'Salud')")
    query.exec_("insert into sector values(2, 'Energy', 'Energía')")
    query.exec_("insert into sector values(3, 'Bank', 'Banca')")

    query.exec_("create table component(id int primary key,"
                "ticket varchar(10) NOT NULL, description varchar(80),"
                "sector int)")
    query.exec_("insert into component values(1, 'GAS.MC',"
                " 'GAS NATURAL', 2)")
    query.exec_("insert into component values(2, 'SAN.MC',"
                " 'Banco Santander',3)")

    query.exec_("create table customnetwork(id int primary key, "
                "name varchar(50) NOT NULL, description varchar(150))")
    query.exec_("insert into customnetwork values "
                "(1, 'IBEX35', 'Primer ejemplo')")
    query.exec_("insert into customnetwork values "
                "(2, 'CAC', 'Segundo ejemplo')")

    query.exec_("create table customnetwork_component("
                "component_id int not null references component(id), "
                "customnetwork_id int not null references customnetwork(id),"
                "primary key (component_id, customnetwork_id))")


def delete_database():
    try:
        os.remove(PATH_TO_FILE)
        log.info("The database has been deleted")

    except OSError as error:
        log.error("The file it does not exist")


def create_database():
    if os.path.isfile(PATH_TO_FILE):
        log.info("The database is already created")
    else:
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(PATH_TO_FILE)
        db.open()
        create_tables()
        db.close()
        log.info("The database has been created")


def createConnection():
    log.debug("Connecting to database")
    db = QSqlDatabase.addDatabase('QSQLITE')
    # db.setDatabaseName(':memory:') # RAM database, bien para tests
    if os.path.isfile(PATH_TO_FILE):
        iscreated = True
        log.info("The database is already created")
    else:
        iscreated = False
        log.info("Creating database")
    db.setDatabaseName(PATH_TO_FILE)
    if not db.open():
        QMessageBox.critical(None, "Cannot open database",
                             "Unable to establish a database connection.\n"
                             "This example needs SQLite support. "
                             "Please read the Qt SQL "
                             "driver documentation for information "
                             "how to build it.\n\n"
                             "Click Cancel to exit.", QMessageBox.Cancel)
        return False, None

    if not iscreated:
        create_tables()
    return True, db
