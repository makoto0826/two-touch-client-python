from datetime import datetime
from tzlocal import get_localzone
from model.information import Information

ja = get_localzone()

class InformationRepository(object):

    def __init__(self, session):
        self._session = session

    def get(self):
        SQL = 'SELECT text FROM information WHERE id=1'
        rows = self._session.fetchall(SQL)

        for row in rows:
            return Information.from_json(row[0])

        return None

    def upsert(self, info):
        SQL = '''
INSERT INTO information(id,text,created_at,updated_at)
VALUES (1,?,?,?)
ON CONFLICT(id)
DO UPDATE SET
text       = excluded.text,
updated_at = excluded.updated_at
'''
        json_data = info.to_json()
        self._session.execute(SQL, [json_data, datetime.now(ja).isoformat(), datetime.now(ja).isoformat()])
