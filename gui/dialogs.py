import logging
import sys
import datetime as dt

from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox,
                             QFormLayout, QGridLayout, QGroupBox,
                             QHBoxLayout, QLabel, QLineEdit,
                             QSpinBox, QTextEdit, QVBoxLayout,
                             QWidget, QStyle)

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QValidator
from PyQt5 import QtSql

from gui.models import CustomNetwork


log = logging.getLogger('simpleDevelopment')


class CustomNetworkNameValidator():
    def __init__(self, connection):
        self.connection = connection

    def validate(self, text):
        if text is None or text == '':
            return QValidator.Invalid, 'The field cannot be empty'

        self.connection.open()
        query = QtSql.QSqlQuery()
        text_query = 'select id from customnetwork where name = "{}";' \
            .format(text)
        query.exec_(text_query)
        if query.next():
            result = QValidator.Invalid, 'This name alreay exists'
        else:
            log.debug("Valid name {}".format(text))
            result = QValidator.Acceptable, 'ok'

        self.connection.close()

        return result


class CustomNetworkFormDialog(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self, parent, customnetwork_id):
        super().__init__(parent)
        self.parent = parent
        self.object = CustomNetwork.getObject(parent.connection, customnetwork_id)

        self.createFormGroupBox()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                          QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accepting)
        self.buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("New CustomNetwork Form")

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Data:")
        self.name = QLineEdit(self.object.get('name', ''))
        self.description = QLineEdit(self.object.get('description', ''))
        if 'components' in self.object and len(self.object['components']) > 0:
            tickets_text = \
            ' '.join([comp['ticket'] for comp in self.object['components']])
        else:
            tickets_text = ''

        self.tickets = QTextEdit(tickets_text)

        self.name.setPlaceholderText('Enter a name')
        self.name.textChanged.connect(self.check_state)
        layout = QFormLayout()
        layout.addRow(QLabel("Name:"), self.name)
        layout.addRow(QLabel("Description:"), self.description)
        layout.addRow(QLabel("Tickets:"), self.tickets)
        self.formGroupBox.setLayout(layout)

    def accepting(self):
        # TODO: La validación del resto de campos falta.
        ok_button = self.buttonBox.buttons()[0]
        validator = CustomNetworkNameValidator(self.parent.connection)
        state = validator.validate(self.name.text())[0]
        # state = validator.validate(self.name.text(), 0)[0]
        if state == QValidator.Acceptable:
            color = 'white'
            ok_button.setEnabled(True)
        else:
            color = '#f6989d'  # red
            ok_button.setEnabled(False)
        self.name.setStyleSheet("background-color: {};".format(color))
        if state == QValidator.Acceptable:
            self.done(QDialog.Accepted)


    def check_state(self, event):
        ok_button = self.buttonBox.buttons()[0]
        self.name.setStyleSheet("background-color: white;")
        ok_button.setEnabled(True)
    #  static method to create the dialog and return (date, time, accepted)

    @staticmethod
    def getData(parent=None, customnetwork_id=-1):

        dialog = CustomNetworkFormDialog(parent, customnetwork_id)
        result = dialog.exec_()
        tickets = dialog.tickets.toPlainText().split()
        # TODO: aquí necesita validación extra, no sólo un simple split()
        return (dialog.name.text(),
                dialog.description.text(),
                tickets,
                result == QDialog.Accepted)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
