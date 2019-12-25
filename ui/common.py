from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout

NFC_SCREEN_NAME = 'nfc'
SELECT_SCREEN_NAME = 'select'
WEEKS = ["月", "火", "水", "木", "金", "土", "日"]


def create_ok_popup(title, message):
    popup_content = GridLayout(cols=1)

    popup_close = Button(
        text='閉じる',
        font_size=20,
        height=40
    )

    popup_content.add_widget(Label(text=message, font_size=20))
    popup_content.add_widget(popup_close)

    popup = Popup(
        title=title,
        size_hint=(None, None),
        size=(400, 400),
        content=popup_content
    )

    popup_close.bind(on_release=popup.dismiss)

    return popup
