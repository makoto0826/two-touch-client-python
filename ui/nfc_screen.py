from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty
from device.nfc_receiver import NfcReceiver
from ui import NFC_SCREEN_NAME, SELECT_SCREEN_NAME, WEEKS
from db.user_repository import UserRepository
from datetime import datetime
from logging import getLogger
import db

logger = getLogger(__name__)

not_found_sound = SoundLoader.load('./sound/not_found.mp3')
touch_sound = SoundLoader.load('./sound/touch.mp3')


class NfcScreen(Screen):
    date = StringProperty()
    time = StringProperty()

    _callback_running = False

    def __init__(self, **kwargs):
        super(NfcScreen, self).__init__(**kwargs)
        self.name = NFC_SCREEN_NAME

    def on_pre_enter(self):
        self._timer_callback(None)

    def on_enter(self):
        logger.info('on_enter')
        NfcReceiver.get_instance().add_handler(self._get_id_callback)
        self._event = Clock.schedule_interval(self._timer_callback, 1)

    def on_leave(self):
        logger.info('on_leave')
        NfcReceiver.get_instance().remove_handler(self._get_id_callback)
        self._event.cancel()
        self._event = None

    def _timer_callback(self, dt):
        now = datetime.now()
        day = WEEKS[now.isoweekday() - 1]

        self.date = now.strftime("%m月%d日(" + day + ")")
        self.time = now.strftime("%H:%M:%S")

    def _get_id_callback(self, card_id):
        logger.info('card_id:' + card_id)

        with db.create_db_session() as session:
            user_repo = UserRepository(session)
            user = user_repo.find_by_card_id(card_id)

            if user is None:
                not_found_sound.play()
                return

            select_screen = self.manager.get_screen(SELECT_SCREEN_NAME)

            if select_screen.user is not None:
                return

            touch_sound.play()
            user.current_card_id = card_id
            select_screen.user = user
            self.manager.current = SELECT_SCREEN_NAME
