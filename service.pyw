from app.widget import WinWidget
from app.core.config import configs

configs.ENV = 'prod'

if __name__ == "__main__":
    widget = WinWidget()
    widget.run()