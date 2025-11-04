
import os
import logging
from pydantic_settings import BaseSettings
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QScreen


class Configs(BaseSettings):

    ENV: str = 'dev'
    DEBUG: bool = ENV == 'dev'
    LOGGING_LEVEL: int = logging.DEBUG if DEBUG else logging.CRITICAL

    PROJECT_NAME: str = 'WinWidget'
    PROJECT_TITLE: str = ''
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    RESOURCES_DIR: str = os.path.join(PROJECT_ROOT, 'resources')

    DATETIME_FORMAT: str = 'dd.MM.yyyy HH:mm:ss'
    TIME_FORMAT: str = 'HH:mm:ss'
    DATE_FORMAT: str = 'dd.MM.yyyy'
    DATEFULL_FORMAT: str = 'dddd, dd.MM.yyyy (MMMM)'

    TIME_INTERVAL_UPDATE: int = 1000

    WIDGET_RECT: tuple = (3, 200, 500, 300)
    TARGET_RECT: tuple = (0, WIDGET_RECT[1], WIDGET_RECT[0], WIDGET_RECT[3])
    TOAST_RECT: tuple = (WIDGET_RECT[0], WIDGET_RECT[1] + WIDGET_RECT[3], WIDGET_RECT[2], 100)

    MOUSE_INTERVAL_UPDATE: int = 500
    DRAW_INTERVAL_UPDATE: int = 100

    TELEGRAM_BOT_TOKEN: str | None = os.getenv('WINWIDGET_TELEGRAM_BOT_NOTEBOOK_TOKEN')
    TELEGRAM_CHAT_ID: str | None = os.getenv('TELEGRAM_ID')

    NOTIFICATION_SOUND_PATH: str = os.path.join(RESOURCES_DIR, 'mixkit-sci-fi-click-900.wav')
    STYLES_PATH: str = os.path.join(RESOURCES_DIR, 'styles.css')

    ZAPRET_SERVICE_BAT: str = 'C:\Program Files\zapret\service.bat'
    LAST_USED_FOLDER_OPEN: str = os.path.expanduser("~")
    LAST_USED_FOLDER_SAVE: str = os.path.expanduser("~")

    ACTION_GROUPS: dict = {
        'DRAW': 'Рисование на экране',
        'PDF': 'Обработка pdf-документов',
        'START': 'Запуск программ',
        'TEXT': 'Текст',
        'TIME': 'Таймеры',
        'SQL': 'SQL',
    }
    ACTION_FAST_ACCESS: list = ['TEXT', 'DRAW', 'START', 'TIME', 'SQL', 'PDF']


    OLLAMA_BASE_URL: str = "http://localhost:11434"

    @property
    def OLLAMA_WIDGET_RECT(self) -> tuple:
        app = QApplication.instance()
        screen: QScreen = app.primaryScreen()
        size = screen.size()
        w = size.width() * 0.80
        h = size.height() - 3
        l = size.width() / 2 - w / 2
        t = 3
        return [*map(int, (l, t, w, h))]

    @property
    def OLLAMA_TARGET_RECT(self) -> tuple:
        app = QApplication.instance()
        screen: QScreen = app.primaryScreen()
        size = screen.size()
        w = size.width() * 0.20
        h = 3
        l = size.width() / 2 - w / 2
        t = 0
        return [*map(int, (l, t, w, h))]


    class Config:
        case_sensitive: bool = True


configs = Configs()

