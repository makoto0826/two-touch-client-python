from datetime import datetime
from tzlocal import get_localzone
import uuid
import json

IN_TYPE = '1'
OUT_TYPE = '2'
GO_OUT_IN = '7'
GO_OUT_OUT = '8'

NONE_STATUS = '1'
SENT_STATUS = '2'
NOT_FOUND_STATUS = '5'

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

    def change_sent_status(self):
        self.status = SENT_STATUS

    def change_not_found_status(self):
        self.status = NOT_FOUND_STATUS

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
    def create_with_go_out_in(user):
        record = TimeRecord._create(user)
        record.type = GO_OUT_IN

        return record

    @staticmethod
    def create_with_go_out_out(user):
        record = TimeRecord._create(user)
        record.type = GO_OUT_OUT

        return record

    @staticmethod
    def _create(user):
        record = TimeRecord()
        record.card_id = user.current_card_id
        record.user_id = user.user_id
        record.user_name = user.user_name
        record.registered_at = datetime.now(ja)

        return record
