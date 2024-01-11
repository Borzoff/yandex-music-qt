from pydantic import BaseModel


class TrackModel(BaseModel):
    row: int | None = None
    track_name: str | None = None
    track_artist: str | None = None
    track_path: str | None = None
    track_id: str | None = None
    track_cover: str | None = None
    track_album: int | None = None
    track_duration: int | None = None
