from PyQt6.QtWidgets import QTableWidget, QListWidget
import enum

from yandex_music_qt_app.utils.on_click_in_list import (
    model_download_clicked,
    model_open_playlist_clicked,
    model_open_album_clicked,
)


class Actions(enum.Enum):
    download = 1
    open_playlist = 2
    open_album = 3


async def action_manager(table: QTableWidget | QListWidget, action: Actions, manager):
    match action:
        case Actions.download:
            model = await model_download_clicked(table, manager)
        case Actions.open_playlist:
            model = await model_open_playlist_clicked(table, manager)
        case Actions.open_album:
            model = await model_open_album_clicked(table, manager)
        case _:
            model = None
    return model
