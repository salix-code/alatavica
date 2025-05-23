import sys

import os
import sqlite3

from datetime import datetime
from typing import List

from alatavica.datatype import FCandleData


class FTable:
    def __init__(self,ticker,interval):
        self.rows : [FCandleData] = []
        self.ticker = ticker
        self.interval = interval
        self.new_index = 0
    def fetch_rows(self) -> List[FCandleData]:
        return self.rows
    def fetch_first(self):
        return self.rows[0]
    def num(self):
        return len(self.rows)
    def fetch_last(self):
        return self.rows[-1]
    def append_rows(self,rows):
        self.rows.extend(rows)

class FDatabaseTableNameHelper:
    def __init__(self,ticker:str,interval):
        self.ticker = ticker.lower()
        if self.ticker.endswith('.hk') and len(self.ticker) >= 8:
            self.ticker = self.ticker[1:]
        self.interval = interval
    def get_database_name(self):
        return self.ticker.lower() + ".db"
    def get_table_name(self):
        return f"_{self.interval}"
    def get_alice_name(self):
        return self.ticker.lower() + "." + self.interval.lower()

class FDatabase:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"db")

        self.tables = dict()

    def get_table(self,ticker:str,interval:str) -> FTable:
        name_helper = FDatabaseTableNameHelper(ticker,interval)
        alice_name = name_helper.get_alice_name()
        if alice_name not in self.tables:
            self.tables[alice_name] = FTable(ticker,interval)
            self.create_if_not_exist(ticker,interval)
            self.load_table(ticker,interval)
        return self.tables[alice_name]

    def create_if_not_exist(self,ticker,interval):
        name_helper = FDatabaseTableNameHelper(ticker, interval)
        conn = sqlite3.connect(os.path.join(self.db_path,name_helper.get_database_name()))

        cursor = conn.cursor()
        create_sql = f"CREATE TABLE IF NOT EXISTS {name_helper.get_table_name()}("
        create_sql += f"id INTEGER PRIMARY KEY AUTOINCREMENT,"
        create_sql += f"DateTime TEXT NOT NULL,"
        create_sql += f"Open FLOAT NOT NULL,"
        create_sql += f"Close FLOAT NOT NULL,"
        create_sql += f"Low FLOAT NOT NULL,"
        create_sql += f"High FLOAT NOT NULL,"
        create_sql += f"AdjustedClose FLOAT NOT NULL,"
        create_sql += f"Volume BIGINT NOT NULL"
        create_sql += ")"
        cursor.execute(create_sql)
        cursor.close()
        conn.close()

    def load_table(self,ticker,interval):
        name_helper = FDatabaseTableNameHelper(ticker, interval)
        conn = sqlite3.connect(os.path.join(self.db_path,name_helper.get_database_name()))
        table = self.tables[name_helper.get_alice_name()]
        cursor = conn.cursor()
        select_sql = f'SELECT "DateTime","Open","Close","Low","High","AdjustedClose","Volume" FROM {name_helper.get_table_name()} ORDER BY "id"'
        try:
            cursor.execute(select_sql)
        except Exception as e:
            print(select_sql)
            print(e)
        for row in cursor.fetchall():
            table.rows.append(FCandleData(datetime.strptime(row[0],"%Y-%m-%d"),row[1],row[2],row[3],row[4],row[5],row[6]))
        table.new_index = len(table.rows)
        cursor.close()
        conn.close()

    def save_table(self,table:FTable):
        if table.new_index == table.num():
            return
        name_helper = FDatabaseTableNameHelper(table.ticker, table.interval)
        insert_rows = []
        for x in range(table.new_index,len(table.rows)):
            insert_rows.append((table.rows[x].time.strftime("%Y-%m-%d"),
                                table.rows[x].begin_price,
                                table.rows[x].end_price,
                                table.rows[x].low_price,
                                table.rows[x].high_price,
                                table.rows[x].adjusted_close,
                                table.rows[x].volume
                                ))
        conn = sqlite3.connect(os.path.join(self.db_path,name_helper.get_database_name()))
        cursor = conn.cursor()
        table_name = name_helper.get_table_name()
        cursor.executemany(
            f"INSERT INTO {table_name} (DateTime,Open,Close,Low,High,AdjustedClose,Volume) VALUES (?,?,?,?,?,?,?)", insert_rows)
        table.new_index = len(table.rows)

        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    database = FDatabase()
    table = database.get_table("9690.HK",'1d')
    table.fetch_rows()
