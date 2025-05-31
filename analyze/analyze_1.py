#
import os
from alatavica.db import FDatabase,FTable,FCandleData
from datetime import datetime, timedelta
import sys

def calc_volume(rows,index, num):
    value = 0
    for x in range(max(0,index - num),index):
        value += rows[x].volume
    return value / num

def run(symbol_name):
    db = FDatabase()
    table: FTable = db.get_table(symbol_name, "1d")
    rows: [FCandleData] = table.fetch_rows()

    for index in range(1,len(rows)):
        volume_value = calc_volume(rows,index,20)
        if rows[index].volume > rows[index - 1].volume * 3:
            if index <= len(rows) - 3:
                if rows[index + 1].low_price > rows[index].low_price and rows[index + 1].low_price > rows[
                    index].low_price:
                    print(rows[index])

            else:
                print("may be" ,rows[index])




def main(*args):
    symbol_names = []
    if len(args) == 0:
        for db_name in os.listdir("../db/"):
            if db_name.endswith(".db"):
                symbol_names.append(db_name[:-3])
    else:
        symbol_names.extend(args)

    for symbol_name in symbol_names:
        print(symbol_name)
        run(symbol_name)
if __name__ == "__main__":
    main("6618.HK","9690.HK","0728.HK","2390.HK")