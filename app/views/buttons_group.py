
import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGroupBox, QGridLayout
from app.util.qelements import QIconButton, QEmpty
from app.core.config import configs
from app.actions import actions

class ButtonsGroup(QGroupBox):
    def __init__(self):
        super().__init__(None)
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        items = [[]]

        for row in configs.GROUP_TEMPLATE:
            for item in row:
                if not item:
                    items[-1].append(QEmpty())
                    continue

                current_actions = [action for action in actions if action.group == item and action.is_available()]
                current_actions.sort(key=lambda action: action.order)

                for action_class in current_actions:
                    action = action_class(self)
                    button = QIconButton(os.path.join(configs.RESOURCES_DIR, action.icon_path), action.description)
                    button.clicked.connect(action.perform)
                    items[-1].append(button)
                
            items.append([])

        for row_it, row in enumerate(items):
            for col_it, item in enumerate(row):
                layout.addWidget(item, row_it, col_it)
        
        self.setLayout(layout)
