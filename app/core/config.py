

import os
import logging
from pydantic_settings import BaseSettings

class Configs(BaseSettings):

    ENV: str = os.getenv("ENV", "dev")
    DEBUG: bool = ENV == "dev"
    LOGGING_LEVEL: int = logging.DEBUG if DEBUG else logging.INFO

    PROJECT_NAME: str = "win-widget"
    PROJECT_TITLE: str = ""
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    RESOURCES_DIR: str = os.path.join(PROJECT_ROOT, 'resources')

    DATETIME_FORMAT: str = "dd.MM.yyyy HH:mm:ss"
    DATETIMEFULL_FORMAT: str = "d MMMM yyyy года HH:mm:ss"
    TIME_INTERVAL_UPDATE: int = 1000

    WIDGET_RECT: tuple = (3, 200, 500, 300)
    TARGET_RECT: tuple = (-10, WIDGET_RECT[1], 13, WIDGET_RECT[3])
    MOUSE_INTERVAL_UPDATE: int = 500

    DRAW_INTERVAL_UPDATE: int = 100


    QTWIDGET_STYLES: str = """
QFrame {
    background: #2b2b2b;
    border: 1px solid #444;
    border-radius: 0;
    padding: 0;
}

QToolTip {
    background-color: #3a3a3a;
    color: #f0f0f0;
    border: 1px solid #4a4a4a;
    border-radius: 4px;
    padding: 8px;
    font-family: "Segoe UI", Arial;
    font-size: 11pt;
    box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
    opacity: 240;
}

QLabel {
    border: none;
    color: #ffffff;
    font-size: 30pt;
    font-weight: 500;
    font-family: "Segoe UI", Arial;
    margin: 0;
    padding: 0;
}

QGroupBox {
    border: none;
    margin: 0;
    padding: 0;
}

QPushButton {
    background: #3a3a3a;
    border: 1px solid #555;
    border-radius: 4px;
    min-width: 25px;
    max-width: 25px;
    min-height: 25px;
    max-height: 25px;
    padding: 0;
    margin: 0;
}

QPushButton:hover {
    background: #4a4a4a;
}

QPushButton:pressed {
    background: #2a2a2a;
}
"""
    QTOVERLAY_STYLES: str = """
background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #000000, stop:1 #2a5c2a);
border: none;
border-radius: 0 5px 5px 0;
padding: 0;
margin: 0;
"""

    class Config:
        case_sensitive: bool = True


configs = Configs()

