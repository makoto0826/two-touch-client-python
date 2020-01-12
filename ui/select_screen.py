from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty
from ui import NFC_SCREEN_NAME, SELECT_SCREEN_NAME, WEEKS
from model.time_record import TimeRecord
from db.time_record_repository import TimeRecordRepository
from logging import getLogger
from datetime import datetime
import db

logger = getLogger(__name__)

in_sound = SoundLoader.load('./sound/in.mp3')
out_sound = SoundLoader.load('./sound/out.mp3')


class SelectScreen(Screen):
    date = StringProperty()
    time = StringProperty()

    def __init__(self, **kwargs):
        super(SelectScreen, self).__init__(**kwargs)
        self.name = SELECT_SCREEN_NAME
        self.user = None

    def on_pre_enter(self):
        self._timer_callback(None)

    def on_enter(self):
        logger.info('on_enter')
        self._event = Clock.schedule_interval(self._timer_callback, 1)

    def on_leave(self):
        logger.info('on_leave')
        self._event.cancel()
        self._event = None

    def handle_in_click(self):
        self.manager.current = NFC_SCREEN_NAME
        record = TimeRecord.create_with_in(self.user)
        self._add_time_record(record)
        self.user = None

        in_sound.play()

    def handle_out_click(self):
        self.manager.current = NFC_SCREEN_NAME
        record = TimeRecord.create_with_out(self.user)
        self._add_time_record(record)
        self.user = None

        out_sound.play()

    def handle_go_out_in_click(self):
        self.manager.current = NFC_SCREEN_NAME
        record = TimeRecord.create_with_go_out_in(self.user)
        self._add_time_record(record)
        self.user = None

        in_sound.play()

    def handle_go_out_out_click(self):
        self.manager.current = NFC_SCREEN_NAME
        record = TimeRecord.create_with_go_out_out(self.user)
        self._add_time_record(record)
        self.user = None

        out_sound.play()

    def handle_go_out_in_click(self):
        self.manager.current = NFC_SCREEN_NAME
        record = TimeRecord.create_with_go_out_in(self.user)
        self._add_time_record(record)
        self.user = None

        in_sound.play()

    def handle_go_out_out_click(self):
        self.manager.current = NFC_SCREEN_NAME
        record = TimeRecord.create_with_go_out_out(self.user)
        self._add_time_record(record)
        self.user = None

        out_sound.play()

    def handle_cancel_click(self):
        self.manager.current = NFC_SCREEN_NAME
        self.user = None

    def _timer_callback(self, dt):
        now = datetime.now()
        day = WEEKS[now.isoweekday() -1]

        self.date = now.strftime("%Y年%m月%d日(" + day + ")")
        self.time = now.strftime("%H時%M分%S秒")

    def _add_time_record(self, record):
        with db.create_db_session() as session:
            repo = TimeRecordRepository(session)
            session.transaction(lambda _: repo.add(record))
