from PyQt5.QtWidgets import QLineEdit


class ValidableFieldMixin (object):
    pass


class TextField(QLineEdit, ValidableFieldMixin):
    def __init__(self, content='', parent=None):
        super().__init__(content, parent)
        self.is_valid = True
        self.textChanged.connect(self.check_state)

    def setValid(self, valid):
        if valid:
            self.setStyleSheet("background-color: white;")
        else:
            self.setStyleSheet("background-color: #f6989d;")  # light red
            self.setToolTip('ERROR FIELD')
        self.is_valid = valid

    def check_state(self, event):
        self.setValid(True)

    def setErrorMessage(self, message):
        self.error_message = message


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
