import sqlite3
from typing import List, Any

from common import constants
from model import saving as s


class SavingsRepo:

    def __init__(self):
        self.conn = sqlite3.connect(constants.DB_NAME)
        self.cursor = self.conn.cursor()
        initialize_table_statement = """
        CREATE TABLE IF NOT EXISTS savings 
        (
           id INTEGER PRIMARY KEY AUTOINCREMENT,  
           name varchar(50),
           value varchar(50)
        )
        """
        self.cursor.execute(initialize_table_statement)
        self.conn.commit()

    def upd(self, id: int, new_saving: s.Saving) -> None:
        upd_statement = "UPDATE savings SET name = ?, value = ? WHERE id = ?"
        self.cursor.execute(upd_statement, (new_saving.name, new_saving.value, id))
        self.conn.commit()

    def fetch_all(self) -> List[Any]:
        self.cursor.execute("SELECT * FROM savings")
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()


saving_repo_instance = SavingsRepo()
