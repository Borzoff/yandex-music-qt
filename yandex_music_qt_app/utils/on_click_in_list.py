from PyQt6.QtWidgets import QTableWidget, QListWidget

from yandex_music_qt_app.services.music import MusicManager


async def model_download_clicked(
    table: QTableWidget, manager: MusicManager
) -> QTableWidget | tuple:
    res = await manager.play_track_by_id(table.currentIndex().data(1))

    return res


async def model_open_playlist_clicked(
    table: QListWidget, manager: MusicManager
) -> QListWidget | tuple:
    if table.currentIndex().data(1) is not None:
        res = await manager.open_playlist_by_id(table.currentIndex().data(1))
    else:
        res = None
    return res


async def model_open_album_clicked(
    table: QListWidget, manager: MusicManager
) -> QListWidget | tuple:
    res = await manager.open_album_by_id(table.currentIndex().data(1))

    return res
