import logging
import sys
import datetime as dt

from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox,
                             QFormLayout, QGridLayout, QGroupBox,
                             QHBoxLayout, QLabel, QLineEdit,
                             QSpinBox, QTextEdit, QVBoxLayout,
                             QWidget, QStyle, QLCDNumber,
                             QSlider, QProgressBar, QPushButton,
                             QDesktopWidget)

from PyQt5.QtCore import QRegExp, Qt, QBasicTimer

from PyQt5.QtGui import QRegExpValidator, QValidator, QColor
from PyQt5 import QtSql

from core import forms, utils
from gui.models import CustomNetwork, NetWorkParameters


log = logging.getLogger('simpleDevelopment')


CREATION, EDITION, READ = 0, 1, 2


class CustomNetworkValidator(forms.FormValidator):
    def __init__(self, connection):
        self.connection = connection

    def _name_already__exists(self, name):
        isOK = name.is_valid

        self.connection.open()
        query = QtSql.QSqlQuery()
        text_query = 'select id from customnetwork where name = "{}";' \
            .format(name.text())
        query.exec_(text_query)
        if query.next():
            isOk &= False
            name.setValid(False, 'This name already exists')
        else:
            log.debug("Valid name {}".format(name.text()))
            name.setValid(True)
            isOk &= True

        return isOk

    def validate(self, form, mode=CREATION):
        super().validate(form, mode)
        isOk = True

        name = form.fields['name']

        if mode == CREATION:
            isOk &= _name_already__exists(name)

        tickets = form.fields['tickets']
        components = tickets.toPlainText().split()
        checking_set = set()
        repetead = set()
        for ticket in components:
            if ticket not in checking_set:
                checking_set.add(ticket)
            else:
                repetead.add(ticket)
        if len(repetead) > 0:
            isOk = False
            tickets.setValid(False,
                             'The are some tickets repetead: {}'.
                             format(' '.join(repetead)))

        # QValidator.Invalid
        self.connection.close()

        if isOk:
            val = QValidator.Acceptable
        else:
            val = QValidator.Invalid

        return val


class NetworkPreferenceValidator(forms.FormValidator):
    def __init__(self, connection):
        self.connection = connection

    def _name_already__exists(self, name):
        isOK = name.is_valid

        self.connection.open()
        query = QtSql.QSqlQuery()
        text_query = 'select id from customnetwork where name = "{}";' \
            .format(name.text())
        query.exec_(text_query)
        if query.next():
            isOk &= False
            name.setValid(False, 'This name already exists')
        else:
            log.debug("Valid name {}".format(name.text()))
            name.setValid(True)
            isOk &= True

        return isOk

    def validate(self, form, mode=CREATION):
        super().validate(form, mode)
        isOk = True
        start_date_fd = form.fields['start_date']
        end_date_fd = form.fields['end_date']

        try:
            start_date = utils.to_dt(start_date_fd.text())
        except ValueError as e:
            isOk &= False
            start_date_fd.setValid(False, str(e))

        try:
            end_date = utils.to_dt(end_date_fd.text())

        except ValueError as e:
            isOk &= False
            end_date_fd.setValid(False, str(e))

        if isOk and utils.cmp_dt(start_date, end_date) >= 0:
            isOk &= False
            start_date.setValid(False,
                                'The start_date cannot be greater'
                                ' than the end date')
            end_date.setValid(False, 'The start_date cannot be greater'
                                     ' than the end date')

        if isOk:
            val = QValidator.Acceptable
        else:
            val = QValidator.Invalid

        return val


class CustomNetworkFormDialog(QDialog, forms.FormMixing):
    # NumGridRows = 3
    # NumButtons = 4

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

        self.name.communicate.changeValidationStatus.connect(self.check_state)

        if 'components' in self.object and len(self.object['components']) > 0:
            tickets_text = \
                ' '.join([comp['ticket']
                         for comp in self.object['components']])
        else:
            tickets_text = ''

        self.tickets = forms.TextArea(tickets_text, not_null=False)
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
            state = validator.validate(self, EDITION)
        else:
            state = validator.validate(self, CREATION)

        if state == QValidator.Acceptable:
            ok_button.setEnabled(True)
        else:
            ok_button.setEnabled(False)

        if state == QValidator.Acceptable:
            self.done(QDialog.Accepted)

    #  static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getData(parent=None, customnetwork_id=-1):

        dialog = CustomNetworkFormDialog(parent, customnetwork_id)
        result = dialog.exec_()
        tickets = dialog.tickets.toPlainText().split()
        return (dialog.name.text(),
                dialog.description.text(),
                tickets,
                result == QDialog.Accepted)


class NetWorkParametersFormDialog(QDialog, forms.FormMixing):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.object = NetWorkParameters.\
            getObject(parent.connection, parent.customnetwork_id_selected)
        self.customnetwork = CustomNetwork.getObject(parent.connection)
        splinnersGroupBox = self._createSplinnersGroupBox()
        dateGroupBox = self._createDateGroupBox()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                          QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accepting)
        self.buttonBox.rejected.connect(self.reject)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(splinnersGroupBox)
        mainLayout.addWidget(dateGroupBox)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("New CustomNetwork Form")

    def _createDateGroupBox(self):
        dateGroupBox = QGroupBox("Date:")
        self.start_date = forms.TextField()
        validator = QRegExpValidator(QRegExp(utils.DATE_EXP))
        self.start_date.setValidator(validator)

        self.end_date = forms.TextField(self.object.get('end_date', ''))
        self.end_date.setValidator(validator)
        layout = QFormLayout()
        layout.addRow(QLabel("Start date:"), self.start_date)
        layout.addRow(QLabel("End date:"), self.end_date)
        dateGroupBox.setLayout(layout)

        self.start_date.communicate.\
            changeValidationStatus.connect(self.check_state)
        self.end_date.communicate.\
            changeValidationStatus.connect(self.check_state)

        return dateGroupBox

    def _createSplinnersGroupBox(self):
        splinnersGroupBox = QGroupBox("Params:")

        step_lbl = QLabel("Step")
        self.lcd_step = QLCDNumber(self)
        self.lcd_step.setSegmentStyle(QLCDNumber.Flat)

        sld_step = QSlider(Qt.Horizontal, self)
        sld_step.setFocusPolicy(Qt.NoFocus)
        sld_step.setRange(1, 10)

        history_lbl = QLabel("History")
        self.lcd_history = QLCDNumber(self)
        self.lcd_history.setSegmentStyle(QLCDNumber.Flat)
        sld_history = QSlider(Qt.Horizontal, self)
        sld_history.setFocusPolicy(Qt.NoFocus)
        sld_history.setRange(10, 100)
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(step_lbl, 1, 0)
        grid.addWidget(sld_step, 1, 1)
        grid.addWidget(self.lcd_step, 1, 2)
        grid.addWidget(history_lbl, 2, 0)
        grid.addWidget(sld_history, 2, 1)
        grid.addWidget(self.lcd_history, 2, 2)

        splinnersGroupBox.setLayout(grid)
        sld_step.valueChanged.connect(self.lcd_step.display)
        sld_history.valueChanged.connect(self.lcd_history.display)

        return splinnersGroupBox

    def accepting(self):
        ok_button = self.buttonBox.buttons()[0]
        validator = NetworkPreferenceValidator(self.parent)
        if len(self.object) > 0:
            state = validator.validate(self, EDITION)
        else:
            state = validator.validate(self, CREATION)

        if state == QValidator.Acceptable:
            ok_button.setEnabled(True)
        else:
            ok_button.setEnabled(False)

        if state == QValidator.Acceptable:
            self.done(QDialog.Accepted)

    #  static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getData(parent=None, customnetwork_id=-1):

        dialog = NetWorkParametersFormDialog(parent)
        result = dialog.exec_()
        return (dialog.lcd_step.value(),
                dialog.lcd_history.value(),
                dialog.start_date,
                dialog.end_date,
                result == QDialog.Accepted)


class BackGroundTaskDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.timer = QBasicTimer()
        self.step = 0
        self.resize(280, 100)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('QProgressBar')
        self.show()
        # self.setFocusPolicy(Qt.StrongFocus)
        self.doAction()

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.close()
            # return
        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):

        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)


    @staticmethod
    def open(parent=None):

        dialog = BackGroundTaskDialog(parent)
        result = dialog.exec_()
        return True


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
