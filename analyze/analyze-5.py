# 录找5日均线超过24日均线的情况
import os

from alatavica.datatype import FCandleData
from alatavica.db import FDatabase, FTable


def run(ticker):
    db = FDatabase()
    table: FTable = db.get_table(ticker,"1d")
    rows: [FCandleData] = table.fetch_rows()

    def calc_price(index_day, interval_day):
        price_list = [x.low_price for x in
                      rows[max(0, index_day - interval_day + 1):min(index_day + 1, len(rows))]]
        return sum(price_list) / interval_day

    policy_list = [
        (3,10,1.05,0.9,10),
        (3, 10, 1.05,0.9,10),
        (5, 24, 1.05,0.9,10),
        (5, 24, 1.05,0.9,10),
    ]
    for policy in policy_list:
        data = []
        for i in range(0,len(rows)):
            day_5 = calc_price(i, policy[0])
            day_24 = calc_price(i, policy[1])
            data.append((day_5, day_24))

        index = 1
        select_day = []
        while index < len(rows):
            if data[index][0] > data[index][1] and data[index - 1][0] < data[index - 1][1]:
                if data[index][0] > data[index - 1][0]:
                    if data[index][1] > data[index - 1][1] * policy[3]:
                        select_day.append(index)

            index += 1

        fail_count = 0
        for day in select_day:
            price = data[day - 1][1]
            index = day + 1
            while index < len(rows) and index < day + policy[4]:
                if rows[index].high_price > price * policy[2]:
                    print(rows[day],price)
                    break
                index += 1
            else:
                print(rows[day],"failed")
                fail_count += 1

        print(policy,len(select_day),fail_count)




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

