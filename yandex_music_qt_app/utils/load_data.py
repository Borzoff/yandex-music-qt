import asyncio

from PyQt6.QtWidgets import QListWidget, QStackedWidget, QTableWidget

from yandex_music_qt_app.services.music import MusicManager
from yandex_music_qt_app.widgets.PlayerList import PlayerTableWidget, PlayerListWidget
from yandex_music_qt_app.utils.action_manager import Actions, action_manager


async def add_to_table(table: PlayerTableWidget | PlayerListWidget, data: list):
    try:
        table.setRowCount(0)
        table.setRowCount(len(data))
    except AttributeError:
        table.clear()
    for row, item in enumerate(data):
        await table.add_item(row, *item)

    return True


async def load_data(
    data_fetcher,
    table: PlayerListWidget | PlayerTableWidget,
    tracks_table: PlayerTableWidget,
    manager: MusicManager,
    action: Actions = None,
    ui_elements: list = None,
):
    button, stacked_widget = ui_elements
    if button:
        button.setEnabled(False)
    tracks_table.setRowCount(0)

    data = await data_fetcher()
    await add_to_table(table, data)
    try:
        await connect_signal(table, manager, tracks_table, action, stacked_widget)
    except Exception:
        raise
    if button:
        button.setEnabled(True)
    return data


async def connect_signal(
    table: PlayerTableWidget,
    manager: MusicManager,
    tracks_table,
    action: Actions,
    stacked_widget,
):
    if not action:
        return
    table.doubleClicked.connect(
        lambda: asyncio.create_task(
            create_task(
                table=table,
                tracks_table=tracks_table,
                action=action,
                stacked_widget=stacked_widget,
                manager=manager,
            )
        )
    )


async def create_task(
    table: QListWidget | QTableWidget,
    tracks_table,
    manager: MusicManager,
    action,
    stacked_widget,
):
    current_action = await action_manager(table=table, action=action, manager=manager)
    if action == Actions.open_album or action == Actions.open_playlist:
        if current_action is not None:
            try:
                await change_page(stacked_widget, 2)
                await add_to_table(tracks_table, current_action)
                table.doubleClicked.disconnect()
            except Exception as e:
                print(e)


async def change_page(widget: QStackedWidget, page: int):
    widget.setCurrentIndex(page)
