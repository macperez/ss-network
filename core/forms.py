from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QLineEdit, QTextEdit


class ValidableFieldMixin (object):
    pass


class Communicate(QObject):
    changeValidationStatus = pyqtSignal(bool)


class TextField(QLineEdit, ValidableFieldMixin):
    def __init__(self, content='', parent=None, not_null=True):
        super().__init__(content, parent)
        self.is_valid = True
        self.not_null = not_null
        self.textChanged.connect(self.check_state)
        self.communicate = Communicate()

    def _field_empty(self):
        return self.text() == '' or self.text is None

    def focusOutEvent(self, event):
        if self.not_null and self._field_empty():
            self.setValid(False, 'This field cannot be null')
        else:
            self.setValid(True)

    def setValid(self, valid, errmsg=''):
        if valid:
            self.setStyleSheet("background-color: white;")
            self.communicate.changeValidationStatus.emit(True)

        else:
            self.setStyleSheet("background-color: #f6989d;")  # light red
            self.communicate.changeValidationStatus.emit(False)

        self.setToolTip(errmsg)
        self.is_valid = valid

    def check_state(self, event):
        self.setValid(True)


class TextArea(QTextEdit, ValidableFieldMixin):
    def __init__(self, content='', parent=None, not_null=True):
        super().__init__(content, parent)
        self.is_valid = True
        self.not_null = not_null
        self.textChanged.connect(self.check_state)
        self.communicate = Communicate()

    def _field_empty(self):
        return self.toPlainText() == '' or self.toPlainText() is None

    def focusOutEvent(self, event):
        if self.not_null and self._field_empty():
            self.setValid(False, 'This field cannot be null')
        else:
            self.setValid(True)

    def setValid(self, valid, errmsg=''):
        if valid:
            self.setStyleSheet("background-color: white;")
            self.communicate.changeValidationStatus.emit(True)

        else:
            self.setStyleSheet("background-color: #f6989d;")  # light red
            self.communicate.changeValidationStatus.emit(False)

        self.setToolTip(errmsg)
        self.is_valid = valid

    def check_state(self):
        self.setValid(True)


class FormMixing:
    def __init__(self):
        self.fields = {}

    def get_validable_fields(self):
        for f in dir(self):
            field = getattr(self, f)
            if isinstance(field, ValidableFieldMixin):
                self.fields[f] = field


class FormValidator:
    def validate(self, form, mode):
        form.get_validable_fields()
