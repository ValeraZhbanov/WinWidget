
import logging
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGroupBox, QGridLayout
from app.widget.views.buttons.text_buttons import LayoutSwitchButton, TelegramButton, AITextConvertButton
from app.widget.views.buttons.graphic_buttons import RectangleButton, ArrowButton, CleanButton
from app.widget.views.buttons.start_buttons import NotepadButton, CmdButton, CmdAdminButton, ZapretButton
from app.widget.views.buttons.time_buttons import TimerButton
from app.widget.utils.qelements import QVSeparator

class ButtonsGroup(QGroupBox):
    def __init__(self):
        super().__init__(None)
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        items = [
            [LayoutSwitchButton(), TelegramButton(), AITextConvertButton(), QVSeparator(), NotepadButton(), CmdAdminButton(), ZapretButton()],
            [RectangleButton(), ArrowButton(), CleanButton()],
            [TimerButton()],
        ]

        for row_it, row in enumerate(items):
            for col_it, item in enumerate(row):
                layout.addWidget(item, row_it, col_it)
        
        self.setLayout(layout)
