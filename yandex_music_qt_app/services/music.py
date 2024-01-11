from random import random
from typing import List

from yandex_music import ClientAsync, Track, Playlist, TrackShort, TracksList


class MusicManager:
    """Yandex Music manager"""

    def __init__(self, client: ClientAsync):
        self.client = client
        # self.radio = Radio(self.client)

    async def get_user_info(self):
        """Получаем информацию пользователя"""
        if not self.client.me.account:
            return
        res = self.client.me.account
        return res

    async def is_logged_in(self):
        """Проверяем в аккаунте мы или нет"""
        if self.client.me.account.display_name is None:
            return False
        else:
            return True

    async def get_users_playlists(self):
        """Получаем плейлисты"""
        liked_playlists = await self.client.users_likes_playlists(timeout=228)
        my_playlists = await self.client.users_playlists_list(timeout=228)
        tracks = [("Ваши плейлисты:", None, None, None)]
        for playlist in my_playlists:
            tracks.append(
                (
                    playlist.title,
                    playlist.playlist_id,
                    playlist.owner.name,
                    playlist.owner.uid,
                )
            )
        tracks.append(("Чужие плейлисты, которые вам понравились:", None, None, None))
        for playlist in liked_playlists:
            tracks.append(
                (
                    playlist.playlist.title,
                    playlist.playlist.playlist_id,
                    playlist.playlist.owner.name,
                    playlist.playlist.owner.uid,
                )
            )

        return tracks

    async def get_users_albums(self):
        """Получаем альбомы"""
        albums = await self.client.users_likes_albums(timeout=228)
        tracks = []
        for album in albums:
            tracks.append(
                (
                    album.album.title,
                    album.album.id,
                    album.album.artists[0].name,
                    None,
                )
            )

        return tracks

    async def get_liked_playlist(self) -> list:
        """Любимые треки"""
        playlist = await self.client.users_likes_tracks(timeout=228)
        res = await self._fetch_tracks(playlist)
        return res

    async def play_track_by_id(self, track_id: str):
        """Получаем ссылку трек"""
        get_track = await self.client.tracks(track_id, timeout=900)
        track = get_track[0]
        track_cover = f"https://{track.cover_uri[:-2]}200x200"
        track_duration = track.duration_ms
        try:
            track_artist = track.artists[0].name
            track_album = track.albums[0].id
        except IndexError:
            track_artist = "Нету"
            track_album = None
        download_link = None
        directory = await track.get_download_info_async(True)
        for info in directory:
            if info.codec == "mp3" and info.bitrate_in_kbps == 320:
                download_link = info.direct_link
                break
            else:
                download_link = info.direct_link

        res = {
            "track_name": track.title,
            "track_artist": track_artist,
            "track_path": download_link,
            "track_id": track_id,
            "track_album": track_album,
            "track_cover": track_cover,
            "track_duration": track_duration,
        }

        return res

    async def open_playlist_by_id(self, playlist_id: str):
        """Открываем плейлист"""
        get_playlist = await self.client.playlists_list(playlist_id, timeout=228)
        tracks = await get_playlist[0].fetch_tracks_async()
        tracks_list = await self._tracks_to_list(tracks)

        return tracks_list

    async def open_album_by_id(self, album_id: int):
        """Открываем альбом"""
        album = await self.client.albums(album_id, timeout=228)
        tracks = await album[0].with_tracks_async()
        res = await self._tracks_to_list(tracks.volumes[0])

        return res

    async def is_liked(self, track_id: str):
        """Проверяем статус нравится на треки"""
        playlist = await self.client.users_likes_tracks()
        search = playlist.tracks_ids
        if track_id in search:
            return True
        else:
            return False

    async def like_track(self, track_id):
        """Добавляем отметку нравится"""
        return await self.client.users_likes_tracks_add(track_id)

    async def dislike_track(self, track_id):
        """Снимаем отметку нравится"""
        return await self.client.users_likes_tracks_remove(track_id)

    async def _fetch_tracks(self, playlist: Playlist | TracksList):
        """Получаем треки"""
        tracks = await playlist.fetch_tracks_async()
        res = await self._tracks_to_list(tracks)
        return res

    @staticmethod
    async def _tracks_to_list(tracks_object: List[Track] | List[TrackShort]) -> List:
        """Треки в список"""
        res = []
        for result in tracks_object:
            track = result.track if hasattr(result, "track") else result
            track_title = track.title
            track_id = track.track_id
            try:
                artist = track.artists[0].name
                album = track.albums[0].title
            except (AttributeError, IndexError):
                album = "Нету"
                artist = "Нету"

            res.append((track_title, track_id, artist, album))

        return res

    async def send_play_start_track(self, track_id: str):
        """Отправляем в Яндекс данные о начале прослушивания трека (Нужно для рекомендаций)"""
        response = await self.client.tracks(track_id)
        track = response[0]
        total_seconds = track.duration_ms
        try:
            await self.client.play_audio(
                from_="desktop_win-home-playlist_of_the_day-playlist-default",
                track_id=track.id,
                album_id=track.albums[0].id,
                play_id=await self._generate_play_id(),
                track_length_seconds=0,
                total_played_seconds=0,
                end_position_seconds=total_seconds,
            )
        except IndexError:
            pass

    async def send_play_end_track(self, track_id):
        """Отправляем в Яндекс данные о конце прослушивания трека (Нужно для рекомендаций)"""
        response = await self.client.tracks(track_id)
        track = response[0]
        played_seconds = track.duration_ms
        total_seconds = track.duration_ms
        await self.client.play_audio(
            from_="desktop_win-home-playlist_of_the_day-playlist-default",
            track_id=track.id,
            album_id=track.albums[0].id,
            play_id=await self._generate_play_id(),
            track_length_seconds=int(total_seconds),
            total_played_seconds=played_seconds,
            end_position_seconds=total_seconds,
        )

    @staticmethod
    async def _generate_play_id():
        return "%s-%s-%s" % (
            int(random() * 1000),
            int(random() * 1000),
            int(random() * 1000),
        )
