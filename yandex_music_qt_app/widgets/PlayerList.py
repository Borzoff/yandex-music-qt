from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QListWidget, QListWidgetItem
from qasync import asyncSlot


class PlayerTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRowCount(3)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Название", "Исполнитель", "Альбом"])
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)

    @asyncSlot()
    async def add_item(
        self,
        row: int,
        text: str = None,
        track_id: str = None,
        artist: str = None,
        album: str = None,
    ):
        title_item = QTableWidgetItem(text)
        if not album:
            album_item = QTableWidgetItem("Нету")
        else:
            album_item = QTableWidgetItem(album)
        if not artist:
            artist_item = QTableWidgetItem("Нету")
        else:
            artist_item = QTableWidgetItem(artist)
        title_item.setData(1, track_id)
        artist_item.setData(1, track_id)
        album_item.setData(1, track_id)
        self.setItem(row, 0, title_item)
        self.setItem(row, 1, artist_item)
        self.setItem(row, 2, album_item)

    @asyncSlot()
    async def get_all_data(self):
        all_data = []
        for row in range(self.rowCount()):
            row_data = []
            for column in range(self.columnCount()):
                item = self.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            hidden_data = self.item(row, 0).data(1)
            row_data.append(hidden_data)
            all_data.append(row_data)
        return all_data


class PlayerListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)

    @asyncSlot()
    async def add_item(
        self,
        row: int,
        text: str,
        track_id: str = None,
        artist: str = None,
    ):
        track_title = QListWidgetItem()
        if track_id:
            track_title.setData(1, track_id)
        if not artist:
            track_title.setText(f"{text}")
        else:
            track_title.setText(f"{text} - {artist}")
        self.insertItem(row, track_title)
