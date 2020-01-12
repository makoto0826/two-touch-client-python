import japanize_kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from ui.screen_container import ScreenContainer
from ui.nfc_screen import NfcScreen
from ui.select_screen import SelectScreen
from background.information_worker import InformationWorker
from background.add_time_record_worker import AddTimeRecordWorker
from device.nfc_receiver import NfcReceiver

Builder.load_file('./ui/screen.kv')

class TwoTouchApp(App):
    def build(self):
        return ScreenContainer()

    def on_start(self):
        InformationWorker.get_instance().run()
        AddTimeRecordWorker.get_instance().run()
        NfcReceiver.get_instance().run()

    def on_stop(self):
        InformationWorker.get_instance().stop()
        AddTimeRecordWorker.get_instance().stop()
        NfcReceiver.get_instance().close()