
import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QWidget,QSizePolicy
from app.util.qelements import QIconButton, QFlowLayout
from app.core.config import configs
from app.actions import actions


class ActionGroup(QFrame):

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        self.setLayout(layout)


class ActionFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        main_layout = QFlowLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        
        self.setLayout(main_layout)

        self._create_button_groups()
        
    def _create_button_groups(self):
        action_groups = configs.ACTION_FAST_ACCESS
        
        for group_name in action_groups:
            group_actions = [
                action for action in actions 
                if action.group == group_name and action.is_available()
            ]
            
            if not group_actions:
                continue
                
            group_actions.sort(key=lambda a: a.order)
            
            group_container = ActionGroup()

            for action_class in group_actions:
                action = action_class(self)
                button = QIconButton(os.path.join(configs.RESOURCES_DIR, action.icon_path), action.description)
                button.clicked.connect(action.perform)
                group_container.layout().addWidget(button)
            
            group_container.layout().addStretch()
            
            self.layout().addWidget(group_container)