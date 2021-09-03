import sqlite3
from typing import List, Any

from common import constants
from model import asset as s


class AssetRepo:

    def __init__(self):
        self.conn = sqlite3.connect(constants.DB_NAME)
        self.cursor = self.conn.cursor()
        initialize_table_statement = """
        CREATE TABLE IF NOT EXISTS assets 
        (
           id INTEGER PRIMARY KEY AUTOINCREMENT,  
           name varchar(50),
           value varchar(50)
        )
        """
        self.cursor.execute(initialize_table_statement)
        self.conn.commit()

    def upd(self, id: int, new_asset: s.Asset) -> None:
        upd_statement = "UPDATE assets SET name = ?, value = ? WHERE id = ?"
        self.cursor.execute(upd_statement, (new_asset.name, new_asset.value, id))
        self.conn.commit()

    def fetch_all(self) -> List[Any]:
        self.cursor.execute("SELECT * FROM assets")
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()


asset_repo_instance = AssetRepo()
