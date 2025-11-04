import logging
import json
from typing import Optional, Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal, QUrl, QTimer
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from app.core.config import configs


class TelegramSendMessageNotebookBot(QObject):

    request_finished = pyqtSignal(dict)
    request_error = pyqtSignal(str)

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
        request = QNetworkRequest(self.url)
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
        
        json_data = json.dumps(self.data).encode('utf-8')
        self.reply = manager.post(request, json_data)
        self.reply.finished.connect(self._request_finished)
        self.reply.errorOccurred.connect(self._handle_error)
        return self.reply

    def _request_finished(self):
        try:
            if self.reply.error() == QNetworkReply.NetworkError.NoError:
                response_data = json.loads(self.reply.readAll().data().decode('utf-8'))
                self.request_finished.emit(response_data)
            else:
                error_msg = f"Network error: {self.reply.errorString()}"
                self.request_error.emit(error_msg)
        except Exception as e:
            error_msg = f"Error processing response: {str(e)}"
            self.request_error.emit(error_msg)
        finally:
            self.reply.deleteLater()

    def _handle_error(self, error):
        error_msg = f"Request failed with error {error}: {self.reply.errorString()}"
        logging.error(error_msg)
        self.request_error.emit(error_msg)


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

