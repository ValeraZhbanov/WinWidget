﻿from app import WinWidget, configs

configs.ENV = 'prod'

if __name__ == "__main__":
    widget = WinWidget()
    widget.exec()