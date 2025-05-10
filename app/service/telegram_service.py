import requests
import logging
from app.core.config import configs

class TelegramService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def send_message(self, text: str):
        if not configs.TELEGRAM_BOT_TOKEN or not configs.TELEGRAM_CHAT_ID:
            logging.warning("Telegram credentials not configured")
            return False

        try:
            url = f"https://api.telegram.org/bot{configs.TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': configs.TELEGRAM_CHAT_ID,
                'text': text
            }
            response = requests.post(url, data=payload)
            return response.status_code == 200
        except Exception as e:
            logging.error(f"Error sending Telegram message: {e}")
            return False