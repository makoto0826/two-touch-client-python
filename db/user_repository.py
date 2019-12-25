from datetime import datetime
from tzlocal import get_localzone
from model.user import User
import json

ja = get_localzone()


class UserRepository(object):

    def __init__(self, session):
        self._session = session

    def delete_all(self):
        SQL = '''
DELETE FROM users;
DELETE FROM cards;
'''

        self._session.executescript(SQL)

    def add_all(self, users):
        USER_SQL = '''
INSERT INTO users(user_id,user_name,created_at,updated_at)
VALUES (?,?,?,?)
'''

        CARD_INSERT_SQL = '''
INSERT INTO cards(user_id,card_id,created_at,updated_at)
VALUES (?,?,?,?)
'''
        user_insert_list = []

        for user in users:
            user_insert_list.append(
                [user.user_id,
                 user.user_name,
                 datetime.now(ja).isoformat(),
                 datetime.now(ja).isoformat()
                 ])

        self._session.executemany(USER_SQL, user_insert_list)

        card_insert_list = []

        for user in users:
            for card_id in user.cards:
                card_insert_list.append(
                    [user.user_id,
                     card_id,
                     datetime.now(ja).isoformat(),
                     datetime.now(ja).isoformat()
                     ])

        self._session.executemany(CARD_INSERT_SQL, card_insert_list)

    def find_by_card_id(self, card_id):
        SQL = '''
SELECT
    users.user_id,
    users.user_name,
    cards.card_id
FROM
    cards
INNER JOIN
    users
ON
    cards.user_id = users.user_id
WHERE
    cards.card_id = ?
'''

        rows = self._session.fetchall(SQL, [card_id])

        if len(rows) == 0:
            return None

        user = User()
        user.user_id = rows[0][0]
        user.user_name = rows[0][1]

        for row in rows:
            user.cards.append(row[2])

        return user
