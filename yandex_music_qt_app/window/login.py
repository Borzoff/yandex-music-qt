from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QDialogButtonBox,
)


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        self.setWindowTitle("Авторизация")
        self.token_line_edit = QLineEdit()
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Введите код из браузерной строки:"))
        layout.addWidget(self.token_line_edit)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def token(self):
        return self.token_line_edit.text()
