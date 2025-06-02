
import os
import logging
from PyQt6.QtCore import QObject


class BaseAction(QObject):
    group: str = 'MAIN'
    order: int = 0

    icon_path: str | None = None
    title: str | None = None
    description: str | None = None

    def perform(self):

        pass

    def is_available():
        return True


