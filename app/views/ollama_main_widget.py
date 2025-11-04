import os
import logging
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect, pyqtSlot
from PyQt6.QtGui import QTextCursor, QAction, QTextOption, QFont, QIcon
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QGraphicsDropShadowEffect,
    QComboBox, QTabWidget, QLabel, QFrame, QSplitter, QSizePolicy,
    QToolBar, QToolButton, QMenu, QApplication, QListWidget, QListWidgetItem,
    QFileDialog, QCheckBox, QGroupBox, QProgressBar
)
from app.services.ollama_service import OllamaService, ChatService, Message
from app.services.toast_service import ToastService
from app.util.qelements import QHSeparator, QHoveredWidget
from app.core.config import configs

class LoadingMessageWidget(QFrame):
    """Виджет для отображения сообщения с лоадером"""
    def __init__(self):
        super().__init__()
        self.setObjectName("loadingMessageWidget")
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Заголовок
        role_label = QLabel("Assistant")
        role_label.setStyleSheet("font-weight: bold; color: #4a90e2;")
        
        # Лоадер
        self.loading_label = QLabel("-thinking-")
        self.loading_label.setStyleSheet("color: #888; font-style: italic;")
        
        # Анимация точек
        self.dots = 0
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_loading_text)
        self.animation_timer.start(500)
        
        layout.addWidget(role_label)
        layout.addWidget(self.loading_label)
        layout.addStretch()
        
        self.setStyleSheet("""
            LoadingMessageWidget {
                background-color: #3a3a3a;
                border: 1px solid #555;
                border-radius: 8px;
            }
        """)
        
        self.setLayout(layout)

    def update_loading_text(self):
        self.dots = (self.dots + 1) % 4
        self.loading_label.setText("-" + "." * self.dots + "-")

    def stop_animation(self):
        self.animation_timer.stop()

class MessageWidget(QFrame):
    def __init__(self, role: str, content: str, model: str = None):
        super().__init__()
        self.role = role
        self.content = content
        self.model = model
        
        self.setObjectName("messageWidget")
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Заголовок сообщения
        header_layout = QHBoxLayout()
        role_label = QLabel(f"{self.role.title()}")
        role_label.setStyleSheet("font-weight: bold; color: #4a90e2;")
        
        if self.model:
            model_label = QLabel(f"({self.model})")
            model_label.setStyleSheet("color: #888; font-size: 9pt;")
            header_layout.addWidget(role_label)
            header_layout.addWidget(model_label)
        else:
            header_layout.addWidget(role_label)
        
        header_layout.addStretch()
        
        # Содержимое сообщения
        content_text = QTextEdit()
        content_text.setReadOnly(True)
        content_text.setPlainText(self.content)
        content_text.setWordWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
        content_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Стилизация в зависимости от роли
        if self.role == "user":
            self.setStyleSheet("""
                MessageWidget {
                    background-color: #2d2d2d;
                    border: 1px solid #444;
                    border-radius: 8px;
                }
            """)
        else:
            self.setStyleSheet("""
                MessageWidget {
                    background-color: #3a3a3a;
                    border: 1px solid #555;
                    border-radius: 8px;
                }
            """)
        
        layout.addLayout(header_layout)
        layout.addWidget(content_text)
        self.setLayout(layout)

class ChatArea(QWidget):
    def __init__(self, ollama_service: OllamaService):
        super().__init__()
        self.ollama_service = ollama_service
        self.loading_widget = None  # Для отслеживания лоадера
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Область сообщений
        self.messages_area = QTextEdit()
        self.messages_area.setReadOnly(True)
        self.messages_area.setObjectName("messagesArea")
        
        # Создаем scroll area для сообщений
        from PyQt6.QtWidgets import QScrollArea, QWidget
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("messagesScrollArea")
        
        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.messages_layout.setSpacing(10)
        
        self.scroll_area.setWidget(self.messages_container)
        
        # Панель инструментов чата
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(16, 16))
        
        # Выбор модели
        self.model_combo = QComboBox()
        self.model_combo.addItems(self.ollama_service.get_models())
        self.toolbar.addWidget(QLabel("Модель:"))
        self.toolbar.addWidget(self.model_combo)
        
        # Опции
        self.keep_alive_checkbox = QCheckBox("Сохранять в памяти")
        self.thinking_checkbox = QCheckBox("Размышления")
        self.toolbar.addWidget(self.keep_alive_checkbox)
        self.toolbar.addWidget(self.thinking_checkbox)
        
        # Кнопка прикрепления файлов
        attach_btn = QPushButton("📎")
        attach_btn.setToolTip("Прикрепить файл")
        attach_btn.clicked.connect(self.attach_file)
        self.toolbar.addWidget(attach_btn)
        
        # Поле ввода
        self.input_area = QTextEdit()
        self.input_area.setMaximumHeight(100)
        self.input_area.setPlaceholderText("Введите сообщение...")
        self.input_area.keyPressEvent = self.input_key_press_event
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        self.send_btn = QPushButton("Отправить")
        self.send_btn.clicked.connect(self.send_message)
        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.clicked.connect(self.clear_chat)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addWidget(self.send_btn)
        
        layout.addWidget(self.toolbar)
        layout.addWidget(self.scroll_area, 1)
        layout.addWidget(self.input_area)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)

    def connect_signals(self):
        self.ollama_service.chat_response_received.connect(self.append_response_chunk)
        self.ollama_service.chat_completed.connect(self.on_chat_completed)
        self.ollama_service.error_occurred.connect(self.on_error)
        self.ollama_service.model_list_updated.connect(self.update_model_list)
        self.ollama_service.sending_started.connect(self.on_sending_started)

    def input_key_press_event(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                # Shift+Enter - новая строка
                self.input_area.insertPlainText("\n")
            else:
                # Enter - отправка сообщения
                self.send_message()
                return
        QTextEdit.keyPressEvent(self.input_area, event)

    def send_message(self):
        content = self.input_area.toPlainText().strip()
        if not content:
            return
            
        model = self.model_combo.currentText()
        
        # Очистить поле ввода
        self.input_area.clear()
        
        # Добавить сообщение пользователя в UI
        self.add_message_to_ui("user", content, model)
        
        # Отправить сообщение сервису
        self.ollama_service.send_message(content, model)

    def on_sending_started(self):
        """Показать лоадер при начале отправки"""
        if self.loading_widget is None:
            self.loading_widget = LoadingMessageWidget()
            self.messages_layout.addWidget(self.loading_widget)
            self.scroll_to_bottom()

    def append_response_chunk(self, chunk: str):
        """Добавить часть ответа"""
        # Удалить лоадер, если он есть
        if self.loading_widget:
            self.loading_widget.stop_animation()
            self.messages_layout.removeWidget(self.loading_widget)
            self.loading_widget.deleteLater()
            self.loading_widget = None
        
        # Найти последнее сообщение ассистента или создать новое
        if self.messages_layout.count() > 0:
            last_item = self.messages_layout.itemAt(self.messages_layout.count() - 1)
            if last_item.widget() and hasattr(last_item.widget(), 'role') and last_item.widget().role == "assistant":
                # Обновить последнее сообщение
                content_text = last_item.widget().findChild(QTextEdit)
                if content_text:
                    content_text.setPlainText(content_text.toPlainText() + chunk)
                    self.scroll_to_bottom()
                    return
        
        # Создать новое сообщение ассистента
        self.add_message_to_ui("assistant", chunk, self.model_combo.currentText())

    def on_chat_completed(self):
        """Обработка завершения чата"""
        self.loading_widget = None
        self.scroll_to_bottom()

    def on_error(self, error_msg: str):
        """Обработка ошибок"""
        # Удалить лоадер при ошибке
        if self.loading_widget:
            self.loading_widget.stop_animation()
            self.messages_layout.removeWidget(self.loading_widget)
            self.loading_widget.deleteLater()
            self.loading_widget = None
            
        ToastService.show_error(error_msg)

    def update_model_list(self, models: list):
        current_model = self.model_combo.currentText()
        self.model_combo.clear()
        self.model_combo.addItems(models)
        if current_model in models:
            self.model_combo.setCurrentText(current_model)

    def add_message_to_ui(self, role: str, content: str, model: str = None):
        message_widget = MessageWidget(role, content, model)
        self.messages_layout.addWidget(message_widget)
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        """Прокрутить вниз"""
        QTimer.singleShot(50, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

    def clear_chat(self):
        # Очистить UI
        while self.messages_layout.count():
            item = self.messages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Очистить текущий чат в сервисе
        chat_service = self.ollama_service.chat_service
        if chat_service.current_chat:
            chat_service.current_chat.messages.clear()
        
        self.loading_widget = None

    def attach_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Прикрепить файл", 
            "", 
            "Текстовые файлы (*.txt *.md *.py);;Изображения (*.png *.jpg *.jpeg *.gif);;Все файлы (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Добавить содержимое файла в поле ввода
                current_text = self.input_area.toPlainText()
                if current_text:
                    current_text += "\n\n"
                self.input_area.setPlainText(current_text + f"[Прикрепленный файл: {os.path.basename(file_path)}]\n{content}")
            except Exception as e:
                ToastService.show_error(f"Ошибка чтения файла: {str(e)}")

from PyQt6.QtCore import QSize

class Sidebar(QWidget):
    def __init__(self, ollama_service: OllamaService):
        super().__init__()
        self.ollama_service = ollama_service
        self.setup_ui()
        self.load_chats()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # Кнопки верхнего меню
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(5)
        
        self.new_chat_btn = QPushButton("➕ Новый чат")
        self.new_chat_btn.clicked.connect(self.create_new_chat)
        
        self.settings_btn = QPushButton("⚙️ Настройки")
        self.settings_btn.clicked.connect(self.open_settings)
        
        buttons_layout.addWidget(self.new_chat_btn)
        buttons_layout.addWidget(self.settings_btn)
        
        # Список чатов
        self.chats_label = QLabel("История чатов")
        self.chats_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        
        self.chats_list = QListWidget()
        self.chats_list.itemClicked.connect(self.on_chat_selected)
        
        layout.addLayout(buttons_layout)
        layout.addWidget(self.chats_label)
        layout.addWidget(self.chats_list)
        layout.addStretch()
        
        self.setLayout(layout)

    def load_chats(self):
        self.chats_list.clear()
        chat_service = self.ollama_service.chat_service
        for chat in chat_service.get_chats():
            item = QListWidgetItem(chat.title)
            item.setData(Qt.ItemDataRole.UserRole, chat.id)
            self.chats_list.addItem(item)

    def create_new_chat(self):
        # Создать новый чат через сервис
        chat_service = self.ollama_service.chat_service
        models = self.ollama_service.get_models()
        model = models[0] if models else "llama3"
        chat = chat_service.create_chat("Новый чат", model)
        
        # Обновить список чатов
        self.load_chats()
        
        # Выбрать новый чат
        for i in range(self.chats_list.count()):
            item = self.chats_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == chat.id:
                self.chats_list.setCurrentItem(item)
                break

    def on_chat_selected(self, item):
        chat_id = item.data(Qt.ItemDataRole.UserRole)
        # Здесь будет логика переключения чата
        print(f"Выбран чат: {chat_id}")

    def open_settings(self):
        # Пока показываем пустое диалоговое окно
        from app.util.qelements import QDialogParentHide
        dialog = QDialogParentHide(self.window())
        dialog.setWindowTitle("Настройки")
        dialog.setGeometry(200, 200, 400, 300)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Настройки Ollama"))
        layout.addWidget(QLabel("(Пока пусто)"))
        
        dialog.setLayout(layout)
        dialog.exec()

class QOllamaMainWidget(QHoveredWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setMouseTracking(True)
        self.setGeometry(QRect(*configs.OLLAMA_WIDGET_RECT))
        self.setFixedSize(*configs.OLLAMA_WIDGET_RECT[2:])
        
        self.ollama_service = OllamaService()
        
        self.animation_show = QPropertyAnimation(self, b"windowOpacity")
        self.animation_show.setDuration(300)
        self.animation_show.setStartValue(0)
        self.animation_show.setEndValue(1)

        self.animation_hide = QPropertyAnimation(self, b"windowOpacity")
        self.animation_hide.setDuration(300)
        self.animation_hide.setStartValue(1)
        self.animation_hide.setEndValue(0)
        self.animation_hide.finished.connect(self._on_hide_finished)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(3, 3)
        shadow.setColor(Qt.GlobalColor.gray)
        self.setGraphicsEffect(shadow)

        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Боковая панель
        self.sidebar = Sidebar(self.ollama_service)
        self.sidebar.setFixedWidth(200)
        self.sidebar.setObjectName("sidebar")
        
        # Основная область чата
        self.chat_area = ChatArea(self.ollama_service)
        
        # Разделитель
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.chat_area)
        splitter.setSizes([200, 600])
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def show(self):
        self.animation_show.start()
        self.raise_()
        self.activateWindow()
        return super().show()

    def hide(self):
        self.animation_hide.start()

    def _on_hide_finished(self):
        return super().hide()

    def closeEvent(self, event):
        """Очистка ресурсов при закрытии"""
        self.ollama_service.cleanup()
        super().closeEvent(event)
