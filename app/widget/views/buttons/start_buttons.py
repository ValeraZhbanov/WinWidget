
import os
import ctypes
import logging
import subprocess
from app.widget.views.buttons.icon_button import QIconButton
from app.service.toast_manager import ToastManager
from app.core.config import configs


class NotepadButton(QIconButton):
    def __init__(self):
        super().__init__("icons8-notepad-50.png", "Блокнот")
        
    def on_click(self):
        try:
            subprocess.Popen(['notepad.exe'])
        except Exception as e:
            logging.error(f"Ошибка запуска блокнота: {e}")


class CmdButton(QIconButton):
    def __init__(self):
        super().__init__("icons8-cmd-50.png", "Консоль")
        
    def on_click(self):
        try:
            user_profile = os.path.expanduser('~')
            ctypes.windll.shell32.ShellExecuteW(None, None, 'cmd.exe', f'/K "cd /d {user_profile}"', user_profile, 1)
        except Exception as e:
            logging.error(f"Ошибка запуска командной строки: {e}")


class CmdAdminButton(QIconButton):
    def __init__(self):
        super().__init__("icons8-cmd-80.png", "Консоль администратора")
        
    def on_click(self):
        try:
            user_profile = os.path.expanduser('~')
            ctypes.windll.shell32.ShellExecuteW(None, 'runas', 'cmd.exe', f'/K "cd /d {user_profile}"', user_profile, 1)
        except Exception as e:
            logging.error(f"Ошибка запуска командной строки от имени администратора: {e}")


class ZapretButton(QIconButton):
    def __init__(self):
        super().__init__("icons8-hack-64.png", "Zapret")
        
    def on_click(self):
        try:
            ctypes.windll.shell32.ShellExecuteW(None, 'runas', configs.ZAPRET_SERVICE_BAT, None, None, 1)
        except Exception as e:
            logging.error(f"Ошибка запуска zapret-service.bat от имени администратора: {e}")