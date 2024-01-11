import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel


def format_duration(duration):
    milliseconds = duration
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return str(f"{minutes}:{seconds}")


def set_track_image(cover, label: QLabel):
    try:
        set_image(cover, label)
    except:
        raise


def truncate(string, length):
    if len(string) >= length:
        return f"{string[:length]}..."
    return string


def set_image(url: str, label: QLabel):
    request = requests.get(url)
    pixmap = QPixmap()
    pixmap.loadFromData(request.content)
    label.setPixmap(pixmap)
