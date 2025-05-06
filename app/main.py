
import logging
from app.widget import WinWidget
from app.core.config import configs

logging.basicConfig(level=configs.LOGGING_LEVEL)

if __name__ == "__main__":
    widget = WinWidget()
    widget.run()