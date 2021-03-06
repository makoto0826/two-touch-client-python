from datetime import datetime
from tzlocal import get_localzone
import uuid
import json

IN_TYPE = '1'
OUT_TYPE = '2'
START_BREAK_TYPE = '3'
END_BREAK_TYPE = '4'
GO_OUT_TYPE = '7'
GO_OUT_BACK_TYPE = '8'

NONE_STATUS = '1'
OK_STATUS = '2'
REQ_ERROR_STATUS = '3'
AUTH_ERROR_STATUS = '4'

ja = get_localzone()


class TimeRecord(object):

    def __init__(self):
        self.time_record_id = str(uuid.uuid4())
        self.card_id = None
        self.user_id = None
        self.user_name = None
        self.type = None
        self.status = NONE_STATUS
        self.registered_at = None

    def to_json(self):
        return json.dumps({
            'localTimeRecordId': self.time_record_id,
            'cardId': self.card_id,
            'userId': self.user_id,
            'userName': self.user_name,
            'type': self.type,
            'registeredAt': self.registered_at.isoformat()
        }).encode('utf-8')

    def change_ok_status(self):
        self.status = OK_STATUS

    def change_req_error_status(self):
        self.status = REQ_ERROR_STATUS

    def change_auth_error_status(self):
        self.status = AUTH_ERROR_STATUS

    @staticmethod
    def create_with_in(user):
        record = TimeRecord._create(user)
        record.type = IN_TYPE

        return record

    @staticmethod
    def create_with_out(user):
        record = TimeRecord._create(user)
        record.type = OUT_TYPE

        return record

    @staticmethod
    def create_with_start_break(user):
        record = TimeRecord._create(user)
        record.type = START_BREAK_TYPE

        return record

    @staticmethod
    def create_with_end_break(user):
        record = TimeRecord._create(user)
        record.type = END_BREAK_TYPE

        return record

    @staticmethod
    def create_with_go_out(user):
        record = TimeRecord._create(user)
        record.type = GO_OUT_TYPE

        return record

    @staticmethod
    def create_with_go_out_back(user):
        record = TimeRecord._create(user)
        record.type = GO_OUT_BACK_TYPE

        return record

    @staticmethod
    def _create(user):
        record = TimeRecord()
        record.card_id = user.current_card_id
        record.user_id = user.user_id
        record.user_name = user.user_name
        record.registered_at = datetime.now(ja)

        return record
