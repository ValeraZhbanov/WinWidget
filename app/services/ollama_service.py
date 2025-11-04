import json
import logging
import requests
from typing import List, Dict, Any, Generator
from PyQt6.QtCore import QObject, pyqtSignal
from app.core.config import configs


class OllamaService(QObject):
    _instance = None
    model_list_updated = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

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
        self.base_url = configs.OLLAMA_BASE_URL
        self._update_model_list()

    def _update_model_list(self):
        """Обновить список доступных моделей"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.models = [model['name'] for model in data.get('models', [])]
                self.model_list_updated.emit(self.models)
        except Exception as e:
            logging.error(f"Ошибка получения списка моделей: {e}")
            self.error_occurred.emit(f"Не удалось получить список моделей: {str(e)}")

    def get_models(self) -> List[str]:
        """Получить список доступных моделей"""
        return self.models

    def chat_stream(self, model: str, messages: List[Dict[str, str]], options: Dict[str, Any] = None) -> Generator[str, None, None]:
        """Отправить сообщения и получить потоковый ответ"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": True
            }
            
            if options:
                payload["options"] = options
                
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                stream=True,
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode('utf-8'))
                    if 'message' in data and 'content' in data['message']:
                        yield data['message']['content']
                    elif 'error' in data:
                        raise Exception(data['error'])
                        
        except Exception as e:
            logging.error(f"Ошибка в чате: {e}")
            raise Exception(f"Ошибка чата: {str(e)}")

    def generate_stream(self, model: str, prompt: str, options: Dict[str, Any] = None) -> Generator[str, None, None]:
        """Сгенерировать текст по промпту"""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": True
            }
            
            if options:
                payload["options"] = options
                
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=True,
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode('utf-8'))
                    if 'response' in data:
                        yield data['response']
                    elif 'error' in data:
                        raise Exception(data['error'])
                        
        except Exception as e:
            logging.error(f"Ошибка генерации: {e}")
            raise Exception(f"Ошибка генерации: {str(e)}")
