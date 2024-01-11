import json
import sys
import webbrowser

import requests
from PyQt6.QtWidgets import QMessageBox

from yandex_music_qt_app.config import MAIN_DIR
from yandex_music_qt_app.config import CLIENT_ID, CLIENT_SECRET
from yandex_music_qt_app.window.login import LoginDialog


def get_token():
    try:
        with open(f"{MAIN_DIR}/token.json", "r") as token_file:
            data = json.load(token_file)
            token = data["token"]
    except (FileNotFoundError, KeyError, json.decoder.JSONDecodeError):
        return
    return token


def rewrite_token(token):
    with open(f"{MAIN_DIR}/token.json", "w") as token_file:
        config = {"token": token}
        json.dump(config, token_file)

        return token


def remove_token():
    with open(f"{MAIN_DIR}/token.json", "w") as token_file:
        config = {"token": ""}
        json.dump(config, token_file)

    sys.exit()


def generate_token(token):
    link_post = "https://oauth.yandex.com/token"
    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 "
        "Safari/537.36"
    )
    header = {"user-agent": user_agent}
    try:
        request_post = f"grant_type=authorization_code&code={token}&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"

        request_auth = requests.post(link_post, data=request_post, headers=header)
        dump = request_auth.json()

        if request_auth.status_code == 200:
            token = dump.get("access_token")
            return token

    except requests.exceptions.ConnectionError:
        print("Не удалось отправить запрос на получение токена")
        return ""


def make_auth():
    QMessageBox.about(
        None,
        "Авторизация",
        "Сейчас откроется браузер. Скопируйте код из адресной строки",
    )
    auth_link = (
        f"https://oauth.yandex.ru/authorize?response_type=code&client_id={CLIENT_ID}"
    )
    webbrowser.open(auth_link)
    window = LoginDialog()
    response = window.exec()
    if response:
        result = window.token()
        if result:
            token = generate_token(result)
            rewrite_token(token)
    else:
        sys.exit()
