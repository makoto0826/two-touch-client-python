class DbSession(object):
    def __init__(self, conn):
        self._conn = conn

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.close()
        return False

    def fetchall(self, sql, params=None):
        if params is None:
            return self._conn.execute(sql).fetchall()
        else:
            return self._conn.execute(sql, params).fetchall()

    def execute(self, sql, params= None):
        if params is None:
            return self._conn.execute(sql)
        else:
            return self._conn.execute(sql, params)

    def executemany(self, sql, params= None):
        if params is None:
            return self._conn.executemany(sql)
        else:
            return self._conn.executemany(sql, params)

    def executescript(self, sql, params= None):
        if params is None:
            return self._conn.executescript(sql)
        else:
            print(sql,params)
            return self._conn.executescript(sql, params)

    def transaction(self, func):
        try:
            self._conn.execute('begin;')
            func(self)
            self._conn.commit()
        except Exception as ex:
            self._conn.rollback()
            raise ex

    def close(self):
        self._conn.close()
