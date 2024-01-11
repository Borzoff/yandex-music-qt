from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from qasync import asyncSlot

from yandex_music_qt_app.ui.queuewidget import Ui_QueueWidget


class QueueWidget(QWidget, Ui_QueueWidget):
    def __init__(self):
        super(QueueWidget, self).__init__()
        self.setupUi(self)
        self.close_queue_window.clicked.connect(self.close)
        self.delete_element_from_queue.clicked.connect(self.remove_element)
        self.tableWidget.setEditTriggers(self.tableWidget.EditTrigger.NoEditTriggers)

    @asyncSlot()
    async def add_elements(self, queue: list):
        self.queue = queue
        self.tableWidget.setRowCount(len(self.queue))
        for row, i in enumerate(self.queue):
            await self.add_element(row, i["track_name"], i["track_artist"])

    @asyncSlot()
    async def add_element(self, row: int, title: str, artist: str):
        title_item = QTableWidgetItem(title)
        artist_item = QTableWidgetItem(artist)

        self.tableWidget.setItem(row, 0, title_item)
        self.tableWidget.setItem(row, 1, artist_item)

    def remove_element(self):
        selected_item = self.tableWidget.currentRow()
        try:
            self.queue.pop(selected_item)
            self.tableWidget.removeRow(selected_item)
        except IndexError:
            raise

    async def clear_elements(self):
        self.tableWidget.setRowCount(0)
