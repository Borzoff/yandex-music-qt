from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QStackedWidget,
)
from qasync import asyncSlot
from yandex_music import ClientAsync

from yandex_music_qt_app.models.track_model import TrackModel
from yandex_music_qt_app.services.radio import Radio
from yandex_music_qt_app.ui.main_window import Ui_MainWindow
from yandex_music_qt_app.services.music import MusicManager
from yandex_music_qt_app.utils.action_manager import Actions, action_manager
from yandex_music_qt_app.utils.auth import remove_token
from yandex_music_qt_app.utils.load_data import load_data
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from yandex_music_qt_app.ui.resourcefiles import resources  # noqa
from yandex_music_qt_app.utils.player_tools import (
    format_duration,
    truncate,
    set_track_image,
)
from yandex_music_qt_app.utils.sync_queue import _sync_queue
from yandex_music_qt_app.window.about import AboutWidget
from yandex_music_qt_app.window.queuewindow import QueueWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(
        self,
        yandex_client: ClientAsync,
        manager: MusicManager,
    ):
        super().__init__()
        self.setupUi(self)
        self.client = yandex_client
        self.manager = manager
        self.radio = Radio(self.client)
        self._audio_output = QAudioOutput()
        self._player = QMediaPlayer(self)
        self._player.setAudioOutput(self._audio_output)
        self.queue = []
        self.shuffled_queue = []
        self.radio_queue = []
        self.queue_window = QueueWidget()
        self.current_track_index = 0
        self.timer = QtCore.QTimer(self)
        self.timer.start(1000)
        self.dropdown_menu.hide()
        self.init_player_elements()
        self.init_sidebar_buttons()
        self.init_widgets()
        self.set_icons()

    def init_sidebar_buttons(self):
        self.my_likes.clicked.connect(self.liked_page)
        self.my_wave.clicked.connect(self.run_my_wave)
        self.my_playlist.clicked.connect(self.playlist_page)
        self.my_albums.clicked.connect(self.albums_page)
        self.my_queue.clicked.connect(self.queue_window.show)

    def init_widgets(self):
        self.like_button.hide()
        self.about_action.triggered.connect(self.open_about)
        self.logout_action.triggered.connect(remove_token)
        self.playpause_button.clicked.connect(self.player_state)
        self.tracks_table.doubleClicked.connect(self.play_file)
        self.forward_button.clicked.connect(self.next)
        self.previus_button.clicked.connect(self.back)
        self.shuffle_button.clicked.connect(self.shuffle)
        self.volume_button.toggled.connect(self.visible_volume)
        self.like_button.clicked.connect(self.like_or_dislike_track)

    def init_player_elements(self):
        self.timer.timeout.connect(self.update_slider)
        self.timer.timeout.connect(self.update_time)
        self._player.mediaStatusChanged.connect(self.end_of_media)
        self.timeline.sliderReleased.connect(self.slider_released)
        self.volume_slider.valueChanged.connect(self.change_volume)
        self.volume_slider.setValue(100)

    def set_icons(self):
        self.like_icon = QIcon()
        self.like_icon.addPixmap(
            QPixmap(":/icon/heart.png"),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.like_icon_filled = QIcon()
        self.like_icon_filled.addPixmap(
            QPixmap(":/icon/heart_filled.png"),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.play_icon = QIcon()
        self.play_icon.addPixmap(
            QPixmap(":/icon/play.png"), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.pause_icon = QIcon()
        self.pause_icon.addPixmap(
            QPixmap(":/icon/pause.png"), QIcon.Mode.Normal, QIcon.State.Off
        )

    async def get_queue_from_another_devices(self):
        queue = await _sync_queue(self.client)
        if queue.context.type == "radio":
            return
        tracks_list = []
        for row, i in enumerate(queue["tracks"]):
            tracks_list.append(f"{i['track_id']}:{i['album_id']}")
        response = await self.client.tracks(tracks_list[0:16])
        for b in response:
            res = await self._map_track_to_data(b)
            self.queue.append(res)
        current_index = queue.current_index
        if current_index < 16:
            self.current_track_index = current_index
        await self.queue_window.add_elements(queue=self.queue)
        await self.set_metadata()

    @asyncSlot()
    async def liked_page(self):
        self.stackedWidget.setCurrentIndex(2)
        await self._load_data(
            data_fetcher=self.manager.get_liked_playlist,
            button=self.my_likes,
            table=self.tracks_table,
            stacked_widget=self.stackedWidget,
        )

    @asyncSlot()
    async def playlist_page(self):
        self.stackedWidget.setCurrentIndex(1)
        await self._load_data(
            data_fetcher=self.manager.get_users_playlists,
            button=self.my_playlist,
            action=Actions.open_playlist,
            table=self.playlist_table,
            stacked_widget=self.stackedWidget,
        )

    @asyncSlot()
    async def albums_page(self):
        self.stackedWidget.setCurrentIndex(1)
        await self._load_data(
            data_fetcher=self.manager.get_users_albums,
            button=self.my_albums,
            action=Actions.open_album,
            table=self.playlist_table,
            stacked_widget=self.stackedWidget,
        )

    @asyncSlot()
    async def get_playlists(self):
        playlists = await self.manager.get_users_playlists()
        for i in playlists:
            self.playlists_list.addItem(i[0])

    @asyncSlot()
    async def _load_data(
        self,
        data_fetcher,
        button: QPushButton = None,
        action: Actions = None,
        table=None,
        stacked_widget: QStackedWidget = None,
    ):
        elements_list = [button, stacked_widget]
        await load_data(
            data_fetcher=data_fetcher,
            action=action,
            table=table,
            tracks_table=self.tracks_table,
            ui_elements=elements_list,
            manager=self.manager,
        )

    @asyncSlot()
    async def player_state(self):
        """Получаем статус плеера"""
        if self.queue or self.radio_queue:
            state = self._player.playbackState()
            if state == QMediaPlayer.PlaybackState.StoppedState:
                await self.play()
            elif state == QMediaPlayer.PlaybackState.PlayingState:
                await self.pause()
            elif state == QMediaPlayer.PlaybackState.PausedState:
                self.resume()

    @asyncSlot()
    async def play(self):
        current_queue = await self.get_current_queue()
        if current_queue[self.current_track_index]["track_path"] is None:
            await self.update_path_info(current_queue)
        url = QtCore.QUrl(current_queue[self.current_track_index]["track_path"])
        await self.manager.send_play_start_track(
            current_queue[self.current_track_index]["track_id"]
        )
        self._player.setSource(url)
        self.current_time.setText("0:00")
        self._player.play()
        self.playpause_button.setIcon(self.pause_icon)
        self.timeline.setSliderPosition(0)

    def resume(self):
        self._player.play()
        self.playpause_button.setIcon(self.pause_icon)

    @asyncSlot()
    async def pause(self):
        self._player.pause()
        self.playpause_button.setIcon(self.play_icon)

    @asyncSlot()
    async def stop(self):
        self._player.stop()
        self.queue.clear()
        self.current_track_index = 0

    @asyncSlot()
    async def next(self, from_end: bool = False):
        if self.queue or self.radio_queue:
            if not from_end:
                self._player.stop()
            if self.radio_queue:
                await self._request_next_radio_track()
            self.current_track_index += 1
            await self.set_metadata()
            await self.play()

    @asyncSlot()
    async def back(self):
        if self.queue or self.radio_queue:
            self._player.stop()
            self.current_track_index -= 1
            await self.set_metadata()
            await self.play()

    def update_time(self):
        pos = self._player.position()
        current_time = str(f"{int(pos / 60000)}:{int((pos / 1000) % 60):02}")
        self.current_time.setText(current_time)

    def update_slider(self):
        if self._player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.timeline.setMinimum(0)
            self.timeline.setMaximum(self._player.duration())
            self.timeline.setValue(self.timeline.value() + 1000)

    @asyncSlot()
    async def play_file(self):
        self.shuffle_button.setChecked(False)

        self.queue.clear()
        self.shuffled_queue.clear()
        self.radio_queue.clear()
        track_data = await self._get_track_data_from_click()
        await self.populate_queue(track_data)
        await self.queue_window.add_elements(queue=self.queue)
        await self.set_metadata()
        await self.play()

    @asyncSlot()
    async def set_metadata(self):
        current_queue = await self.get_current_queue()
        self.like_button.show()
        try:
            track = current_queue[self.current_track_index]
        except IndexError:
            self.current_track_index = 0
            track = current_queue[self.current_track_index]

        self.update_slider()
        if track["track_path"] is None or track["track_duration"]:
            await self.update_path_info(current_queue)
        track_title = track["track_name"]
        track_artist = track["track_artist"]
        duration = track["track_duration"]
        if track["track_cover"] is not None:
            set_track_image(track["track_cover"], self.player_cover)
        else:
            self.player_cover.setPixmap(QPixmap(":/icon/music_cover.jpg"))
        formatted_duration = format_duration(duration)
        self.wait_time.setText(formatted_duration)

        truncated_title = truncate(track_title, 20)
        truncated_artist = truncate(track_artist, 20)

        self.track_title.setText(truncated_title)

        self.track_author.setText(truncated_artist)
        self.track_author.setToolTip(track["track_artist"])
        self.track_title.setToolTip(track["track_name"])
        await self.is_liked()

        self.update_time()

    def slider_released(self):
        self._player.setPosition(self.timeline.value())
        self.update_time()

    @asyncSlot()
    async def end_of_media(self):
        if self._player.mediaStatus() == self._player.MediaStatus.EndOfMedia:
            if len(self.queue) > 1 or len(self.radio_queue) >= 1:
                current_queue = await self.get_current_queue()
                await self.manager.send_play_end_track(
                    current_queue[self.current_track_index]["track_id"]
                )
                if self.repeat_button.isChecked():
                    self._player.play()
                    self.timeline.setSliderPosition(0)
                else:
                    await self.next(True)
            else:
                await self.play()

    @asyncSlot()
    async def shuffle(self):
        if self.shuffle_button.isChecked():
            await self.queue_window.clear_elements()
            self.shuffled_queue = self.queue.copy()
            import random

            random.shuffle(self.shuffled_queue)
            await self.queue_window.add_elements(self.shuffled_queue)
        if not self.shuffle_button.isChecked():
            await self.queue_window.clear_elements()
            await self.queue_window.add_elements(self.queue)

    async def update_path_info(self, queue: list):
        track = queue[self.current_track_index]
        if track["track_path"] is None:
            response = await self.manager.play_track_by_id(track["track_id"])
            if track["track_name"] is None:
                track["track_name"] = response.get("track_name")
                track["track_artist"] = response.get("track_artist")
            track["track_path"] = response.get("track_path")
            track["track_cover"] = response.get("track_cover")
            track["track_album"] = response.get("track_album")
            track["track_duration"] = response.get("track_duration")

    @asyncSlot()
    async def is_liked(self):
        if self.queue or self.radio_queue:
            current_queue = await self.get_current_queue()

            res = await self.manager.is_liked(
                current_queue[self.current_track_index]["track_id"]
            )
            if res:
                self.like_button.setIcon(self.like_icon_filled)
            else:
                self.like_button.setIcon(self.like_icon)

    @asyncSlot()
    async def like_or_dislike_track(self):
        if self.queue or self.radio_queue:
            current_queue = await self.get_current_queue()
            track = current_queue[self.current_track_index]["track_id"]
            if not await self.manager.is_liked(
                current_queue[self.current_track_index]["track_id"]
            ):
                res = await self.manager.like_track(track)
                if res:
                    self.like_button.setIcon(self.like_icon_filled)
            else:
                res = await self.manager.dislike_track(track)
                if res:
                    self.like_button.setIcon(self.like_icon)

    @asyncSlot()
    async def run_my_wave(self):
        track = await self.radio.start_radio("user:onyourwave", None)
        self.current_track_index = 0
        self.queue.clear()
        self.shuffled_queue.clear()
        self.radio_queue.clear()
        await self.stop()
        await self.queue_window.clear_elements()
        data = await self._map_track_to_data(track)
        self.radio_queue.append(data)
        await self.queue_window.add_elements(queue=self.radio_queue)
        await self.set_metadata()
        await self.play()

    async def _request_next_radio_track(self):
        track = await self.radio.play_next()
        data = await self._map_track_to_data(track)

        self.radio_queue.append(data)
        await self.queue_window.add_elements(queue=self.radio_queue)

    @staticmethod
    async def _map_track_to_data(track):
        model = TrackModel(
            row=None,
            track_name=track.title,
            track_artist=track.artists[0].name,
            track_id=track.track_id,
            track_cover=track.cover_uri,
            track_album=track.albums[0].id,
            track_duration=track.duration_ms,
        )
        return model.model_dump()

    @asyncSlot()
    async def visible_volume(self):
        if self.volume_button.isChecked():
            self.dropdown_menu.show()
        else:
            self.dropdown_menu.hide()

    def change_volume(self, value: int):
        value /= 100
        self._audio_output.setVolume(value)

    @asyncSlot()
    async def open_about(self):
        self.about_widget = AboutWidget()
        self.about_widget.show()

    @asyncSlot()
    async def get_current_queue(self) -> list:
        if self.shuffle_button.isChecked():
            current_queue = self.shuffled_queue
        elif self.radio_queue:
            current_queue = self.radio_queue
            self.shuffle_button.hide()
            self.shuffle_button.setChecked(False)
            self.repeat_button.hide()
            self.repeat_button.setChecked(False)
        else:
            current_queue = self.queue
            self.shuffle_button.show()
            self.repeat_button.show()

        return current_queue

    @asyncSlot()
    async def _get_track_data_from_click(self):
        response = await action_manager(
            table=self.tracks_table,
            action=Actions.download,
            manager=self.manager,
        )

        model = TrackModel(
            row=None,
            track_name=response["track_name"],
            track_artist=response["track_artist"],
            track_path=response["track_path"],
            track_id=response["track_id"],
            track_cover=response["track_cover"],
            track_album=response["track_album"],
            track_duration=response["track_duration"],
        )
        return model.model_dump()

    async def populate_queue(self, metadata: dict):
        data = await self.tracks_table.get_all_data()

        for row, track in enumerate(data):
            model = TrackModel(
                row=row,
                track_name=track[0],
                track_artist=track[1],
                track_path=None,
                track_id=track[3],
                track_cover=None,
                track_album=None,
                track_duration=None,
            )

            self.queue.append(model.model_dump())

        for b in self.queue:
            if metadata["track_id"] == b["track_id"]:
                b["track_path"] = metadata["track_path"]
                b["track_album"] = metadata["track_album"]
                b["track_cover"] = metadata["track_cover"]
                b["track_duration"] = metadata["track_duration"]
                self.current_track_index = b["row"]

        return
