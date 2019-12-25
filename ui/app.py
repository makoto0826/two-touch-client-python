import japanize_kivy
from kivy.app import App
from kivy.lang import Builder
from ui.nfc_screen import NfcScreen
from ui.select_screen import SelectScreen
from background.information_worker import InformationWorker
from background.add_time_record_worker import AddTimeRecordWorker
from device.nfc_receiver import NfcReceiver

class TwoTouchApp(App):
    def build(self):
        kv = Builder.load_file('./ui/screen.kv')
        return kv

    def on_start(self):
        InformationWorker.get_instance().run()
        AddTimeRecordWorker.get_instance().run()
        NfcReceiver.get_instance().run()

    def on_stop(self):
        InformationWorker.get_instance().stop()
        AddTimeRecordWorker.get_instance().stop()
        NfcReceiver.get_instance().close()