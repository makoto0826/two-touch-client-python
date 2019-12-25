from datetime import datetime
from tzlocal import get_localzone
from model.time_record import TimeRecord

ja = get_localzone()


class TimeRecordRepository(object):

    def __init__(self, session):
        self._session = session

    def add(self, time_record):
        SQL = '''
INSERT INTO time_records(time_record_id,user_id,user_name,card_id,type,status,registered_at,created_at,updated_at)
VALUES (?,?,?,?,?,?,?,?,?)
'''
        self._session.execute(SQL, [
            time_record.time_record_id,
            time_record.user_id,
            time_record.user_name,
            time_record.card_id,
            time_record.type,
            time_record.status,
            time_record.registered_at.isoformat(),
            datetime.now(ja).isoformat(),
            datetime.now(ja).isoformat()
        ])

    def update_status(self, time_record):
        SQL = '''
UPDATE
    time_records
SET
    status = ?,
    updated_at = ?
WHERE
    time_record_id = ?
'''

        self._session.execute(
            SQL, [time_record.status,datetime.now(ja).isoformat(), time_record.time_record_id])

    def find_by_unsent_status(self):
        SQL = '''
SELECT
    time_record_id,
    user_id,
    user_name,
    card_id,
    type,
    status,
    registered_at
FROM
    time_records
WHERE
    status = '1'
'''
        rows = self._session.fetchall(SQL)

        time_records = []

        if len(rows) == 0:
            return time_records

        for row in rows:
            time_record = TimeRecord()
            time_record.time_record_id = row[0]
            time_record.user_id = row[1]
            time_record.user_name = row[2]
            time_record.card_id = row[3]
            time_record.type = row[4]
            time_record.status = row[5]
            time_record.registered_at = datetime.fromisoformat(row[6])

            time_records.append(time_record)

        return time_records
