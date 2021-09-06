from sqlite3 import Connection
from typing import Dict
from model import asset_types as at
from repository.db_conn import conn


class ExchangerRepo:
    def __init__(self, db_conn: Connection):
        self.conn = db_conn
        self.cursor = self.conn.cursor()
        init_exchange_rate_table = """
        CREATE TABLE IF NOT EXISTS exchange_rates
        (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         from_cur varchar(50),
         ro_cur varchar(50),
         rate varchar(250),
         time timestamp
        )
        """

        self.cursor.execute(init_exchange_rate_table)
        self.conn.commit()

    def update_rate(self, currency: str, rate: float) -> None:
        upd_statement = "UPDATE exchange_rates SET rate = ? WHERE from_cur = ?"
        self.cursor.execute(upd_statement, (str(rate), currency))
        self.conn.commit()

    def fetch_rates(self) -> (Dict[str, float], str):
        statement = "SELECT * FROM exchange_rates"
        self.cursor.execute(statement)
        rows = self.cursor.fetchall()
        rates = {}
        time = ""
        for row in rows:
            rates[f"{row[2]}_IN_{row[1]}"] = float(row[3])
            if row[1] == at.AssetTypes.USD.__str__():
                time = row[4]

        return rates, time

    def __del__(self):
        self.conn.close()


exchanger_repo_instance = ExchangerRepo(conn)
