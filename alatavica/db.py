

import sqlite3





class FDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('example.db')
        self.cursor = self.conn.cursor()


    def create_table_not_exist(self,table_name):
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name}("
        create_sql += f"id INTEGER PRIMARY KEY AUTOINCREMENT,"
        create_sql += f"Ticker TEXT NOT NULL,"
        create_sql += f"Open FLOAT NOT NULL,"
        create_sql += f"Close FLOAT NOT NULL,"
        create_sql += f"Low FLOAT NOT NULL,"
        create_sql += f"High FLOAT NOT NULL,"
        create_sql += f"Volume FLOAT NOT NULL"
        create_sql += ")"
        self.cursor.execute(create_sql)
    def format_table(self,ticker_symbol:str,interval:str):
        table_name = ""
        if ticker_symbol.endswith(".HK"):
            table_name = f"HK{ticker_symbol[1:-3]}"
        table_name = f"{table_name}_{interval}"
        return table_name
    def fetch_last(self,ticker_symbol,interval):
        table_name = self.format_table(ticker_symbol,interval)
        self.create_table_not_exist(table_name)
        select_sql = f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1"
        self.cursor.execute(select_sql)
        rows = self.cursor.fetchall()
        if len(rows) > 0:
            for row in rows:
                print(row)

            return rows[0]
        return None


    def save_data(self,rows):
        row_data = [
        ]

        for row in rows:
            row_data.append((1,2,3,4,5))


        self.cursor.executemany('''
            INSERT INTO users (name, age) VALUES (?, ?,?,?,?)
            ''', row_data)

        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()





if __name__ == '__main__':
    database = FDatabase()
