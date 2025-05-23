#
import os
from alatavica.db import FDatabase,FTable,FCandleData
from datetime import datetime, timedelta
import sys

def index_previous_max_price_from(end_index,rows,num):
    result = -1
    for index in range(max(0,end_index - num + 1),end_index + 1):
        if result == -1:
            result = index
        elif rows[index].high_price > rows[result].high_price:
            result = index
    return result



def run(symbol_name):
    db = FDatabase()
    table: FTable = db.get_table(symbol_name, "1d")
    rows: [FCandleData] = table.fetch_rows()

    data = []
    for index in range(0,len(rows)):
        data.append(index_previous_max_price_from(index,rows,24))

    for index in range(0,len(rows)):
        if index - data[index] > 20:
            print(rows[data[index]])
            print(rows[index])


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
    main("6618.HK")