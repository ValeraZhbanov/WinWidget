import logging
import json
from typing import Optional, Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal, QUrl, QTimer
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from app.core.config import configs

class TelegramSendMessageNotebookBot(QObject):

    request_finished = pyqtSignal(dict)

    def __init__(self, text, request_finished=None):
        super().__init__()

        if not configs.TELEGRAM_BOT_TOKEN or not configs.TELEGRAM_CHAT_ID:
            raise Exception("Telegram credentials not configured")

        self.url = QUrl(f"https://api.telegram.org/bot{configs.TELEGRAM_BOT_TOKEN}/sendMessage")
        self.data = {
            'chat_id': configs.TELEGRAM_CHAT_ID,
            'text': text
        }

        if request_finished:
            self.request_finished.connect(request_finished)


    def run(self, manager: QNetworkAccessManager):
        self.reply: QNetworkReply = manager.post(self.url, self.data, callback)
        return self.reply

    def _request_finished(self):
        self.response_data = json.loads(self.reply.readAll()).decode('utf-8')
        self.request_finished.emit(self.response_data)


class IntegrationService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        super().__init__()
        self.__initialized = True
        self.manager = QNetworkAccessManager()

    def run_task(self, task):
        return task.run(self.manager)
        