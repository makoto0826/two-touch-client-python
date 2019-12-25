from api.api_client import ApiClient
from db.user_repository import UserRepository
from db.information_repository import InformationRepository
from logging import getLogger
import api
import db
import threading
import time

logger = getLogger(__name__)


class InformationWorker(object):

    _instance = None

    def __init__(self, wait=300):
        self._thread = None
        self._wait = wait
        self._running = False

    def run(self):
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def stop(self, timeout=10):
        if not self._running:
            return

        self._running = False
        self._thread.join(timeout)
        self._thread = None

    def _run(self):
        while self._running:
            logger.info('run')

            api_options = api.get_options()
            api_client = ApiClient(api_options)

            with db.create_db_session() as session:
                info_repo = InformationRepository(session)
                user_repo = UserRepository(session)

                try:
                    api_result = api_client.get_information()

                    if not api_result.is_ok():
                        continue

                    remote_info = api_result.value
                    local_info = info_repo.get()

                    if local_info is None or local_info.version.users_version < remote_info.version.users_version:
                        api_result = api_client.get_users()

                        if not api_result.is_.ok():
                            continue

                        def tran(_):
                            info_repo.upsert(remote_info)
                            user_repo.delete_all()
                            user_repo.add_all(api_result.value)

                        session.transaction(tran)

                except Exception as ex:
                    logger.error(ex)

            time.sleep(self._wait)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()

        return cls._instance
