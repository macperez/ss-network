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

from core import forms
from gui.models import CustomNetwork


log = logging.getLogger('simpleDevelopment')

CREATION, EDITION, READ = 0, 1, 2


class CustomNetworkValidator(forms.FormValidator):
    def __init__(self, connection):
        self.connection = connection

    def validate(self, form, mode=CREATION):
        super().validate(form, mode)
        isOk = True

        name = form.fields['name']
        if name.is_valid:
            isOk &= True

        self.connection.open()
        query = QtSql.QSqlQuery()
        text_query = 'select id from customnetwork where name = "{}";' \
            .format(name.text())
        query.exec_(text_query)
        if query.next():
            isOk &= False
            # name.setErrorMessage('This name already exists')
            name.setValid(False, 'This name already exists')
        else:
            log.debug("Valid name {}".format(name.text()))
            name.setValid(True)
            isOk &= True
            # isOk = QValidator.Acceptable

        # QValidator.Invalid
        self.connection.close()

        if isOk:
            val = QValidator.Acceptable
        else:
            val = QValidator.Invalid

        return val


class CustomNetworkFormDialog(QDialog, forms.FormMixing):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self, parent, customnetwork_id):
        super().__init__(parent)
        self.parent = parent
        self.object = CustomNetwork.getObject(parent.connection,
                                              customnetwork_id)
        self._createFormGroupBox()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                          QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accepting)
        self.buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)

        self.setLayout(mainLayout)
        self.setWindowTitle("New CustomNetwork Form")

    def _createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Data:")
        self.name = forms.TextField(self.object.get('name', ''))
        self.description = forms.TextField(self.object.get('description', ''),
                                           not_null=False)

        # self.name.focusOutEvent.connect(self.buttonClicked)
        # self.description.clicked.connect(self.buttonClicked)
        self.name.communicate.changeValidationStatus.connect(self.check_state)
        self.description.communicate.changeValidationStatus.\
            connect(self.check_state)

        if 'components' in self.object and len(self.object['components']) > 0:
            tickets_text = \
                ' '.join([comp['ticket']
                         for comp in self.object['components']])
        else:
            tickets_text = ''

        self.tickets = QTextEdit(tickets_text)
        self.name.setPlaceholderText('Enter a name')

        layout = QFormLayout()
        layout.addRow(QLabel("Name:"), self.name)
        layout.addRow(QLabel("Description:"), self.description)
        layout.addRow(QLabel("Tickets:"), self.tickets)
        self.formGroupBox.setLayout(layout)

    def accepting(self):
        ok_button = self.buttonBox.buttons()[0]
        validator = CustomNetworkValidator(self.parent.connection)
        if len(self.object) > 0:
            state = validator.validate(self, EDITION)[0]
        else:
            state = validator.validate(self, CREATION)

        if state == QValidator.Acceptable:
            ok_button.setEnabled(True)
        else:
            ok_button.setEnabled(False)
        # self.name.setStyleSheet("background-color: {};".format(color))
        if state == QValidator.Acceptable:
            self.done(QDialog.Accepted)

    def check_state(self, val):
        # ok_button = self.buttonBox.buttons()[0]
        print(">> Check state {}".format(val))

        # ok_button.setEnabled(True)

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
