import logging
from app.widget import WinWidget

logging.basicConfig(level=logging.CRITICAL)

if __name__ == "__main__":
    widget = WinWidget()
    widget.run()