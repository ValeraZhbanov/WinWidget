import os
import logging
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt6.QtGui import QTextCursor, QAction, QTextOption
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QGraphicsDropShadowEffect,
    QComboBox, QTabWidget, QLabel, QFrame, QSplitter, QSizePolicy,
    QToolBar, QToolButton, QMenu, QApplication
)
from app.services.ollama_service import OllamaService
from app.services.toast_service import ToastService
from app.util.qelements import QHSeparator, QHoveredWidget
from app.core.config import configs


class MessageWidget(QFrame):
    """Виджет отображения одного сообщения"""
    
    def __init__(self, role: str, content: str, parent=None):
        super().__init__(parent)
        self.role = role
        self.content = content
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Заголовок сообщения
        header_layout = QHBoxLayout()
        role_label = QLabel(f"{self.role}:")
        role_label.setObjectName("MessageRole")
        header_layout.addWidget(role_label)
        header_layout.addStretch()
        
        # Кнопки управления
        copy_btn = QPushButton("Копировать")
        copy_btn.setObjectName("CopyButton")
        copy_btn.clicked.connect(self.copy_content)
        copy_btn.setFixedHeight(25)
        header_layout.addWidget(copy_btn)
        
        layout.addLayout(header_layout)
        
        # Текст сообщения
        self.content_text = QTextEdit()
        self.content_text.setReadOnly(True)
        self.content_text.setText(self.content)
        self.content_text.setWordWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
        self.content_text.setMaximumHeight(150)
        layout.addWidget(self.content_text)
        
        self.setLayout(layout)
        self.setObjectName("MessageWidget")
        
    def copy_content(self):
        """Скопировать содержимое сообщения"""
        clipboard = self.content_text.toPlainText()
        QApplication.clipboard().setText(clipboard)
        ToastService().add("Сообщение скопировано")


class ChatTab(QWidget):
    """Вкладка чата с моделью"""
    
    def __init__(self, model_name: str, parent=None):
        super().__init__(parent)
        self.model_name = model_name
        self.ollama_service = OllamaService()
        self.messages = []
        self.is_generating = False
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Область сообщений
        self.messages_container = QFrame()
        self.messages_layout = QVBoxLayout()
        self.messages_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.messages_layout.setSpacing(5)
        self.messages_layout.setContentsMargins(5, 5, 5, 5)
        self.messages_container.setLayout(self.messages_layout)
        
        # Прокручиваемая область
        self.scroll_area = QSplitter(Qt.Orientation.Vertical)
        self.scroll_area.addWidget(self.messages_container)
        self.scroll_area.setStretchFactor(0, 1)
        
        layout.addWidget(self.scroll_area)
        
        # Разделитель
        layout.addStretch()
        
        # Область ввода
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(5, 5, 5, 5)
        
        # Панель инструментов
        self.toolbar = self.create_toolbar()
        input_layout.addWidget(self.toolbar)
        
        # Поле ввода
        self.input_text = QTextEdit()
        self.input_text.setMaximumHeight(80)
        self.input_text.setPlaceholderText("Введите ваше сообщение...")
        input_layout.addWidget(self.input_text)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        self.send_btn = QPushButton("Отправить")
        self.send_btn.clicked.connect(self.send_message)
        buttons_layout.addWidget(self.send_btn)
        
        self.stop_btn = QPushButton("Остановить")
        self.stop_btn.clicked.connect(self.stop_generation)
        self.stop_btn.setEnabled(False)
        buttons_layout.addWidget(self.stop_btn)
        
        buttons_layout.addStretch()
        
        input_layout.addLayout(buttons_layout)
        input_layout_widget = QWidget()
        input_layout_widget.setLayout(input_layout)
        
        layout.addWidget(input_layout_widget)
        
        self.setLayout(layout)
        
    def create_toolbar(self):
        """Создать панель инструментов"""
        toolbar = QToolBar()
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        toolbar.setIconSize(toolbar.iconSize() * 0.8)  # Уменьшить иконки
        
        # Кнопка поиска в интернете
        search_action = QAction("🌐", self)
        search_action.setToolTip("Поиск в интернете")
        search_action.triggered.connect(self.search_internet)
        toolbar.addAction(search_action)
        
        # Кнопка размышлений
        think_action = QAction("🤔", self)
        think_action.setToolTip("Размышлять")
        think_action.triggered.connect(self.think_mode)
        toolbar.addAction(think_action)
        
        # Меню кастомных опций
        custom_menu = QMenu("Кастомные опции", self)
        custom_action1 = QAction("Кратко", self)
        custom_action1.triggered.connect(lambda: self.add_prefix("Кратко: "))
        custom_action2 = QAction("Подробно", self)
        custom_action2.triggered.connect(lambda: self.add_prefix("Подробно: "))
        custom_menu.addAction(custom_action1)
        custom_menu.addAction(custom_action2)
        
        custom_btn = QToolButton()
        custom_btn.setText("⚙️")
        custom_btn.setMenu(custom_menu)
        custom_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        custom_btn.setToolTip("Кастомные опции")
        toolbar.addWidget(custom_btn)
        
        return toolbar
        
    def add_prefix(self, prefix: str):
        """Добавить префикс к тексту"""
        current_text = self.input_text.toPlainText()
        self.input_text.setPlainText(prefix + current_text)
        self.input_text.moveCursor(QTextCursor.MoveOperation.End)
        
    def search_internet(self):
        """Поиск в интернете"""
        current_text = self.input_text.toPlainText()
        if current_text:
            self.add_prefix("[Поиск в интернете] ")
        
    def think_mode(self):
        """Режим размышлений"""
        current_text = self.input_text.toPlainText()
        if current_text:
            self.add_prefix("[Размышлять] ")
        
    def add_message(self, role: str, content: str):
        """Добавить сообщение в чат"""
        message_widget = MessageWidget(role, content)
        self.messages_layout.addWidget(message_widget)
        self.messages.append({"role": role, "content": content})
        
        # Прокрутить вниз
        QTimer.singleShot(100, self.scroll_to_bottom)
        
    def scroll_to_bottom(self):
        """Прокрутить вниз"""
        # self.scroll_area.widget(0).vis.ensureVisible(0, self.messages_layout.count() * 1000)
        
    def send_message(self):
        """Отправить сообщение"""
        message = self.input_text.toPlainText().strip()
        if not message or self.is_generating:
            return
            
        self.add_message("Пользователь", message)
        self.input_text.clear()
        self.send_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.is_generating = True
        
        # Отправить запрос в Ollama
        try:
            self.add_message("Модель", "")
            self.start_generation(self.model_name, message)
        except Exception as e:
            self.is_generating = False
            self.send_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            ToastService().add(f"Ошибка: {str(e)}")
        
    def start_generation(self, model: str, user_message: str):
        """Начать генерацию ответа"""
        try:
            # Подготовить сообщения
            messages = self.messages[:-1]  # Все сообщения кроме последнего (пустого от модели)
            messages.append({"role": "user", "content": user_message})
            
            # Запустить потоковую генерацию
            def stream_response():
                try:
                    response_content = ""
                    last_widget = self.messages_layout.itemAt(self.messages_layout.count() - 1).widget()
                    if isinstance(last_widget, MessageWidget) and last_widget.role == "Модель":
                        for chunk in self.ollama_service.chat_stream(model, messages):
                            response_content += chunk
                            # Обновить последнее сообщение
                            last_widget.content_text.setPlainText(response_content)
                            # Прокрутить вниз
                            QTimer.singleShot(10, self.scroll_to_bottom)
                            
                    self.is_generating = False
                    self.send_btn.setEnabled(True)
                    self.stop_btn.setEnabled(False)
                    
                except Exception as e:
                    self.is_generating = False
                    self.send_btn.setEnabled(True)
                    self.stop_btn.setEnabled(False)
                    ToastService().add(f"Ошибка генерации: {str(e)}")
            
            # Запустить в отдельном потоке
            from PyQt6.QtCore import QThread
            self.thread = QThread()
            self.thread.run = stream_response
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()
            
        except Exception as e:
            self.is_generating = False
            self.send_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            ToastService().add(f"Ошибка отправки: {str(e)}")
        
    def stop_generation(self):
        """Остановить генерацию"""
        self.is_generating = False
        self.send_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        ToastService().add("Генерация остановлена")


class OllamaWidget(QWidget):
    """Основной виджет Ollama"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ollama_service = OllamaService()
        self.setup_ui()
        self.load_models()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Выбор модели
        model_layout = QHBoxLayout()
        model_layout.setContentsMargins(0, 0, 0, 0)
        
        self.model_combo = QComboBox()
        self.model_combo.currentTextChanged.connect(self.add_new_tab)
        self.model_combo.setMaximumWidth(150)
        
        model_layout.addWidget(QLabel("Модель:"))
        model_layout.addWidget(self.model_combo)
        model_layout.addStretch()
        
        layout.addLayout(model_layout)
        
        # Вкладки чатов
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        layout.addWidget(self.tab_widget)
        
        self.setLayout(layout)
        
    def load_models(self):
        """Загрузить список моделей"""
        models = self.ollama_service.get_models()
        self.model_combo.clear()
        self.model_combo.addItems(models)
        self.model_combo.addItem("+ Новая вкладка")
        
    def add_new_tab(self, model_name: str):
        """Добавить новую вкладку"""
        if model_name == "+ Новая вкладка" or model_name == "":
            return
            
        # Создать новую вкладку
        chat_tab = ChatTab(model_name)
        tab_index = self.tab_widget.addTab(chat_tab, model_name)
        self.tab_widget.setCurrentIndex(tab_index)
        
        # Сбросить комбо-бокс
        self.model_combo.setCurrentIndex(0)
        
    def close_tab(self, index: int):
        """Закрыть вкладку"""
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
        else:
            ToastService().add("Нельзя закрыть последнюю вкладку")


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

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.separator = QHSeparator()
        self.main_layout.addWidget(self.separator)
        
        # Основной виджет Ollama
        self.ollama_view = OllamaWidget()
        self.main_layout.addWidget(self.ollama_view)

        self.setLayout(self.main_layout)

    def show(self):
        self.animation_show.start()
        self.raise_()
        self.activateWindow()
        return super().show()

    def hide(self):
        self.animation_hide.start()

    def _on_hide_finished(self):
        return super().hide()
