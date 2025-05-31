
import logging
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGroupBox, QGridLayout
from app.views.buttons.text_buttons import LayoutSwitchButton, TelegramButton, AITextConvertButton
from app.views.buttons.graphic_buttons import RectangleButton, ArrowButton, CleanButton
from app.views.buttons.start_buttons import NotepadButton, CmdButton, CmdAdminButton, ZapretButton
from app.views.buttons.time_buttons import TimerQuick10Button, TimerQuick30Button, TimerQuick60Button, TimerDialogButton, TimersListButton
from app.views.buttons.tool_buttons import PdfConvertButton, MergePdfButton
from app.views.qelements import QVSeparator

class ButtonsGroup(QGroupBox):
    def __init__(self):
        super().__init__(None)
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        items = [
            [LayoutSwitchButton(), TelegramButton(), AITextConvertButton(), QVSeparator(), NotepadButton(), CmdAdminButton(), ZapretButton()],
            [RectangleButton(), ArrowButton(), CleanButton()],
            [TimerQuick10Button(), TimerQuick30Button(), TimerQuick60Button(), TimerDialogButton(), TimersListButton()],
            [PdfConvertButton(), MergePdfButton()],
        ]

        for row_it, row in enumerate(items):
            for col_it, item in enumerate(row):
                layout.addWidget(item, row_it, col_it)
        
        self.setLayout(layout)
