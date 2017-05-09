import logging
import sys
import datetime as dt

from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox,
                             QFormLayout, QGridLayout, QGroupBox,
                             QHBoxLayout, QLabel, QLineEdit,
                             QSpinBox, QTextEdit,QScrollArea,
                             QVBoxLayout, QWidget, QStyle)

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QValidator
from PyQt5 import QtSql

log = logging.getLogger('simpleDevelopment')


class CustomNetworkNameValidator(QValidator):
    def __init__(self, connection):
        self.connection = connection
        super().__init__()

    def validate(self, text, position):
        log.debug("Trying to validate query")
        self.connection.open()
        query = QtSql.QSqlQuery('select id from customnetwork where '
                                'name = "{}"'.format(text))

        if query.size() > 0 or text == '_INCORRECT_':
            result = QValidator.Invalid, text, position
        else:
            log.debug("Valid name {}".format(text))
            result = QValidator.Acceptable, text, position

        self.connection.close()

        return result


class CreateCustomNetworkDialog(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self, parent):
        super(CreateCustomNetworkDialog, self).__init__(parent)
        self.parent = parent
        self.createFormGroupBox()
        log.debug("Opening dialog")
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                     QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("New CustomNetwork Form")


    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Data:")
        self.name = QLineEdit()
        self.description = QLineEdit()
        self.tickets = QTextEdit()

        # reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
        # input_validator = QRegExpValidator(reg_ex, self.name)
        self.name.setValidator(CustomNetworkNameValidator(
                               self.parent.connection))

        self.name.setPlaceholderText('Enter a name')
        self.name.textChanged.connect(self.check_state)

        layout = QFormLayout()
        layout.addRow(QLabel("Name:"), self.name)
        layout.addRow(QLabel("Description:"), self.description)
        layout.addRow(QLabel("Tickets:"), self.tickets)
        self.formGroupBox.setLayout(layout)

    def check_state(self, event):
        sender = self.sender()
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        # FIXME: esto no está funcionando
        if state == QValidator.Acceptable:
            log.debug(state)
            color = 'white' # green
        elif state == QValidator.Intermediate:
            color = '#fff79a' # yellow
        else:
            log.debug(state)
            color = '#f6989d' # red

        sender.setStyleSheet("background-color: {};".format(color))
    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getData(parent=None):

        dialog = CreateCustomNetworkDialog(parent)
        result = dialog.exec_()
        return (dialog.name.text(),
                dialog.description.text(),
                dialog.tickets.toPlainText(),
                result == QDialog.Accepted)



class Example(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.initUI()

    def initUI(self):

        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
