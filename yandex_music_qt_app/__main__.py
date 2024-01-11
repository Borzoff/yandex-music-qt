import asyncio
import sys

import yandex_music.exceptions
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop
from yandex_music import ClientAsync

from yandex_music_qt_app.services.music import MusicManager
from yandex_music_qt_app.utils.auth import (
    get_token,
    make_auth,
)
from yandex_music_qt_app.window.window import MainWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


async def main():
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    client = ClientAsync(get_token())
    manager = MusicManager(client)
    try:
        await client.init()
        log = await manager.is_logged_in()
        if not log:
            make_auth()
    except yandex_music.exceptions.UnauthorizedError:
        make_auth()
    finally:
        client = ClientAsync(get_token())
        manager = MusicManager(client)
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)
    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    main_window = MainWindow(yandex_client=client, manager=manager)
    main_window.show()
    event_loop.create_task(main_window.get_queue_from_another_devices())
    event_loop.run_until_complete(app_close_event.wait())
    event_loop.close()


if __name__ == "__main__":
    asyncio.run(main())
