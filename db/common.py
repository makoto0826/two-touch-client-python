from db.db_session import DbSession
import sqlite3
import os
import logging

DB_PATH = './data/two-touch.db'

DDL = '''
CREATE TABLE information(
    id   INTEGER    NOT NULL,
    text JSON       NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE users(
    user_id    NVARCHAR(256) NOT NULL,
    user_name  NVARCHAR(256) NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY(user_id)
);

CREATE TABLE cards(
    card_id    NVARCHAR(256) NOT NULL,
    user_id    NVARCHAR(256) NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY(card_id,user_id)
);

CREATE TABLE time_records(
    time_record_id  NVARCHAR(36)  NOT NULL,
    user_id       NVARCHAR(256) NOT NULL,
    user_name     NVARCHAR(256) NOT NULL,
    card_id       NVARCHAR(256) NOT NULL,
    type          CHAR(1) NOT NULL,
    status        CHAR(1) NOT NULL,
    registered_at TEXT NOT NULL,
    created_at    TEXT NOT NULL,
    updated_at    TEXT NOT NULL,
    PRIMARY KEY(time_record_id)
);
'''


def init_db():
    if not os.path.exists(DB_PATH):
        with create_db_session() as session:
            session.transaction(lambda _: _.executescript(DDL))


def create_db_session():
    conn = sqlite3.connect(DB_PATH, isolation_level='EXCLUSIVE')
    return DbSession(conn)
