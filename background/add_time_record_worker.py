from api.api_client import ApiClient
from db.time_record_repository import TimeRecordRepository
from logging import getLogger
import api
import db
import threading
import time

logger = getLogger(__name__)


class AddTimeRecordWorker(object):
    _instance = None

    def __init__(self, wait=10):
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
                repo = TimeRecordRepository(session)
                records = repo.find_by_unsent_status()

                for record in records:
                    try:
                        def tran(_):
                            result = api_client.add_time_record(record)

                            if result.is_ok():
                                record.change_ok_status()
                            elif result.is_req_error():
                                record.change_req_error_status()
                            elif result.is_auth_error():
                                record.change_auth_error_status()

                            repo.update_status(record)

                        session.transaction(tran)
                    except Exception as ex:
                        logger.error(ex)

            time.sleep(self._wait)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()

        return cls._instance
