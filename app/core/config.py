

import os
import logging
from pydantic_settings import BaseSettings

class Configs(BaseSettings):

    ENV: str = os.getenv("ENV", "dev")
    DEBUG: bool = ENV == "dev"
    LOGGING_LEVEL: int = logging.DEBUG if DEBUG else logging.INFO

    PROJECT_NAME: str = "WinWidget"
    PROJECT_TITLE: str = ""
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    RESOURCES_DIR: str = os.path.join(PROJECT_ROOT, 'resources')

    DATETIME_FORMAT: str = "dd.MM.yyyy HH:mm:ss"
    TIME_FORMAT: str = "HH:mm:ss"
    DATE_FORMAT: str = "dd.MM.yyyy"
    DATEFULL_FORMAT: str = "dddd, dd.MM.yyyy (MMMM)"

    TIME_INTERVAL_UPDATE: int = 1000

    WIDGET_RECT: tuple = (3, 200, 500, 300)
    TARGET_RECT: tuple = (-10, WIDGET_RECT[1], 13, WIDGET_RECT[3])
    MOUSE_INTERVAL_UPDATE: int = 500

    DRAW_INTERVAL_UPDATE: int = 100

    TELEGRAM_BOT_TOKEN: str | None = os.getenv("WINWIDGET_TELEGRAM_BOT_NOTEBOOK_TOKEN")
    TELEGRAM_CHAT_ID: str | None = os.getenv("TELEGRAM_ID")

    NOTIFICATION_SOUND_PATH: str = os.path.join(RESOURCES_DIR, 'mixkit-sci-fi-click-900.wav')
    STYLES_PATH: str = os.path.join(RESOURCES_DIR, 'styles.qss')

    class Config:
        case_sensitive: bool = True


configs = Configs()

