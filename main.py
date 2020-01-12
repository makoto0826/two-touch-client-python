import db
import platform
from logging import basicConfig, DEBUG

basicConfig(level=DEBUG)

VERSION = '0.0.1'

if __name__ == '__main__':
    db.init_db()

    from kivy.core.window import Window
    from ui.app import TwoTouchApp

    p = platform.system()

    if p == 'Linux':
        Window.fullscreen = True
        Window.show_cursor = False

    TwoTouchApp().run()

