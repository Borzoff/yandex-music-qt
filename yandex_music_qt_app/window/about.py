from PyQt6.QtWidgets import QWidget
from yandex_music_qt_app.ui.about import Ui_Form


class AboutWidget(QWidget, Ui_Form):
    def __init__(self):
        super(AboutWidget, self).__init__()
        self.setupUi(self)
