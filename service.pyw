import logging
from app import WinWidget, configs

configs.ENV = 'prod'
configs.DEBUG = False
configs.LOGGING_LEVEL = logging.CRITICAL

if __name__ == "__main__":
    widget = WinWidget()
    widget.exec()