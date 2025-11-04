import ollama
import logging
from typing import List, Dict, Any, Generator
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from app.core.config import configs

# Модели данных
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Message:
    id: str
    role: str  # "user" или "assistant"
    content: str
    timestamp: datetime
    model: str = None

@dataclass
class Chat:
    id: str
    title: str
    messages: List[Message]
    model: str
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())

class ChatService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.chats: List[Chat] = []
            self.current_chat: Chat = None

    def create_chat(self, title: str, model: str) -> Chat:
        chat = Chat(
            id=str(uuid.uuid4()),
            title=title,
            messages=[],
            model=model,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.chats.append(chat)
        self.current_chat = chat
        return chat

    def get_chats(self) -> List[Chat]:
        return self.chats

    def set_current_chat(self, chat_id: str):
        for chat in self.chats:
            if chat.id == chat_id:
                self.current_chat = chat
                return chat
        return None

    def add_message(self, message: Message):
        if self.current_chat:
            self.current_chat.messages.append(message)
            self.current_chat.updated_at = datetime.now()

class OllamaWorker(QObject):
    """Рабочий класс для выполнения операций с Ollama в отдельном потоке"""
    response_chunk_received = pyqtSignal(str)
    response_completed = pyqtSignal()
    error_occurred = pyqtSignal(str)
    model_list_updated = pyqtSignal(list)

    def __init__(self, base_url: str):
        super().__init__()
        self.client = ollama.Client(host=base_url)
        self.is_running = False

    def get_models(self):
        """Получить список доступных моделей"""
        try:
            response = self.client.list()
            models = [model.model for model in response.models]
            self.model_list_updated.emit(models)
            return models
        except Exception as e:
            logging.error(f"Ошибка получения списка моделей: {e}")
            self.error_occurred.emit(f"Не удалось получить список моделей: {str(e)}")

    def send_message(self, model: str, messages: List[Dict[str, str]], options: Dict[str, Any] = None):
        """Отправить сообщения и получить потоковый ответ"""
        try:
            self.is_running = True
            stream = self.client.chat(
                model=model,
                messages=messages,
                stream=True,
                options=options or {}
            )

            for chunk in stream:
                if not self.is_running:
                    break
                content = chunk.get('message', {}).get('content', '')
                if content:
                    self.response_chunk_received.emit(content)
            
            self.response_completed.emit()
        except Exception as e:
            logging.error(f"Ошибка в чате: {e}")
            self.error_occurred.emit(f"Ошибка чата: {str(e)}")
        finally:
            self.is_running = False

    def stop(self):
        """Остановить текущую операцию"""
        self.is_running = False

class OllamaService(QObject):
    _instance = None
    
    # Сигналы для взаимодействия с UI
    model_list_updated = pyqtSignal(list)
    chat_response_received = pyqtSignal(str)
    chat_completed = pyqtSignal()
    error_occurred = pyqtSignal(str)
    sending_started = pyqtSignal()  # Начало отправки сообщения

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
        
        # Создаем рабочий поток
        self.thread = QThread()
        self.worker = OllamaWorker(configs.OLLAMA_BASE_URL)
        
        # Перемещаем рабочий объект в поток
        self.worker.moveToThread(self.thread)
        
        # Подключаем сигналы
        self.worker.response_chunk_received.connect(self.chat_response_received)
        self.worker.response_completed.connect(self.chat_completed)
        self.worker.error_occurred.connect(self.error_occurred)
        self.worker.model_list_updated.connect(self.model_list_updated)
        
        # Запускаем поток
        self.thread.start()
        
        self.models: List[str] = []
        self.chat_service = ChatService()
        
        # Получаем список моделей
        self.get_models()

    def get_models(self):
        """Получить список доступных моделей"""
        return self.worker.get_models()

    def send_message(self, content: str, model: str = None):
        """Отправить сообщение и получить ответ"""
        if not model:
            model = self.models[0] if self.models else "llama3"
        
        # Создать новый чат, если его нет
        if not self.chat_service.current_chat:
            self.chat_service.create_chat("Новый чат", model)
        
        # Добавить сообщение пользователя
        user_message = Message(
            id=str(uuid.uuid4()),
            role="user",
            content=content,
            timestamp=datetime.now(),
            model=model
        )
        self.chat_service.add_message(user_message)
        
        # Подготовить сообщения для отправки
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in self.chat_service.current_chat.messages
        ]
        
        # Сигнал о начале отправки
        self.sending_started.emit()
        
        # Отправляем в рабочий поток
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(0, lambda: self.worker.send_message(model, messages))

    def stop_current_operation(self):
        """Остановить текущую операцию"""
        self.worker.stop()

    def cleanup(self):
        """Очистка ресурсов"""
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
