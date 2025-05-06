
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGroupBox, QGridLayout
from app.widget.views.buttons.text_buttons import LayoutSwitchButton
from app.widget.views.buttons.graphic_buttons import RectangleButton, ArrowButton, CleanButton
from app.widget.views.buttons.start_buttons import NotepadButton, CmdButton, CmdAdminButton

class ButtonsGroup(QGroupBox):
    def __init__(self):
        super().__init__(None)
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(LayoutSwitchButton(), 0, 0)

        layout.addWidget(RectangleButton(), 1, 0)
        layout.addWidget(ArrowButton(), 1, 1)
        layout.addWidget(CleanButton(), 1, 2)

        layout.addWidget(NotepadButton(), 2, 0)
        layout.addWidget(CmdButton(), 2, 1)
        layout.addWidget(CmdAdminButton(), 2, 2)

        layout.setColumnStretch(3, 1)
        layout.setRowStretch(3, 1)

        self.setLayout(layout)
