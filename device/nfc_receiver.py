from logging import getLogger
import nfc
import threading
import time

logger = getLogger(__name__)


TARGETS = ['106A', '212F']


class NfcReceiver(object):

    _instance = None

    def __init__(self):
        self._handlers = []
        self._running = False
        self._wait = 1

    def add_handler(self, func):
        self._handlers.append(func)

    def remove_handler(self, func):
        self._handlers = list(filter(lambda f: f != func, self._handlers))

    def run(self):
        if(self._running):
            return

        try:
            self._clf = nfc.ContactlessFrontend('usb')
        except Exception as ex:
            logger.error(ex)
            return

        self._running = True
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def _run(self):
        rdwr = {
            'targets': TARGETS,
            'on-connect': lambda tag: False
        }

        while self._running:
            tag = self._clf.connect(rdwr=rdwr)
            try:
                id = tag.identifier.hex().upper()

                for handler in self._handlers:
                    handler(id)

            except Exception as ex:
                logger.error(ex)

            time.sleep(self._wait)

    def close(self, timeout=10):
        if not self._running:
            return

        self._running = False

        if self._clf:
            self._clf.close()
            self._clf = None

        self._thread.join(timeout=timeout)
        self._thread = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()

        return cls._instance
