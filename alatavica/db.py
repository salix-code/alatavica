

import sqlite3

class FTable:
    def __init__(self,table_name):
        self.rows = []
        self.table_name = table_name
        self.new_index = 0
    def fetch_rows(self):
        return self.rows
    def fetch_first(self):
        return self.rows[0]
    def num(self):
        return len(self.rows)
    def fetch_last(self):
        return self.rows[-1]
    def append_rows(self,rows):
        self.rows.extend(rows)

    def merge_table(self,table_name,interval):
        result_table = FTable(table_name)
        for i in range(0,len(self.rows),interval):
            open_price = self.rows[i][1]
            close_price = self.rows[i + interval if i + interval < len(self.rows) else len(self.rows) - 1][2]
            low_price = self.rows[i][3]
            high_price = self.rows[i][4]

            for j in range(1,min(interval,len(self.rows) - i)):
                row = self.rows[i+j]
                if row[3] < low_price:
                    low_price = row[3]
                if row[4] > high_price:
                    high_price = row[4]
            result_table.rows.append((self.rows[i][0],open_price,close_price,low_price,high_price))

        return result_table



class FDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('20250312.db')
        self.tables = dict()

    def get_table(self,ticker_symbol:str,interval:str) -> FTable:
        table_name = self.format_table(ticker_symbol,interval)
        if table_name not in self.tables:
            self.tables[table_name] = FTable(table_name)
            self.create_if_not_exist(table_name)
            self.load_table(table_name)
        return self.tables[table_name]

    def create_if_not_exist(self,table_name):
        cursor = self.conn.cursor()
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name}("
        create_sql += f"id INTEGER PRIMARY KEY AUTOINCREMENT,"
        create_sql += f"Ticker TEXT NOT NULL,"
        create_sql += f"Open FLOAT NOT NULL,"
        create_sql += f"Close FLOAT NOT NULL,"
        create_sql += f"Low FLOAT NOT NULL,"
        create_sql += f"High FLOAT NOT NULL,"
        create_sql += f"Volume FLOAT NOT NULL"
        create_sql += ")"
        cursor.execute(create_sql)

        cursor.close()
    def load_table(self,table_name):
        table = self.tables[table_name]
        cursor = self.conn.cursor()
        select_sql = f"SELECT Ticker,Open,Close,Low,High FROM {table_name} ORDER BY id"
        cursor.execute(select_sql)
        table.rows.extend(cursor.fetchall())
        table.new_index = len(table.rows)

    def save_table(self,table:FTable):
        insert_rows = table.rows[table.new_index:]
        cursor = self.conn.cursor()
        table_name = table.table_name
        cursor.executemany(
            f"INSERT INTO {table_name} (Ticker,Open,Close,Low,High,Volume) VALUES (?,?,?,?,?,?)", insert_rows)
        table.new_index = len(table.rows)

        self.conn.commit()
        cursor.close()

    def format_table(self,ticker_symbol:str,interval:str):
        table_name = ""
        if ticker_symbol.endswith(".HK"):
            table_name = f"HK{ticker_symbol[1:-3]}"
        table_name = f"{table_name}_{interval}"
        return table_name


    def close(self):
        self.conn.close()

if __name__ == '__main__':
    database = FDatabase()
