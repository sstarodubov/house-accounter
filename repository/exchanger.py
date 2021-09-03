from sqlite3 import Connection

from repository.db_conn import conn


class ExchangerRepo:
    def __init__(self, db_conn: Connection):
        self.conn = db_conn
        self.cursor = self.conn.cursor()
        init_exchange_rate_table = """
        CREATE TABLE IF NOT EXISTS exchange_rates
        (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         "from" varchar(50),
         "to" varchar(50),
         rate varchar(250),
         time timestamp
        )
        """

        self.cursor.execute(init_exchange_rate_table)
        self.conn.commit()

    def __del__(self):
        self.conn.close()


exchanger_repo_instance = ExchangerRepo(conn)
