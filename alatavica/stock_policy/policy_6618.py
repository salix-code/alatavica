import dataclasses
from typing import List


from alatavica.datatype import FCandleData
from alatavica.db import FDatabase, FTable

def get_low_price(row:FCandleData) -> float:
    return row.low_price
def get_high_price(row:FCandleData) -> float:
    return row.high_price

class FPolicy_6618:
    def __init__(self):
        self.ticker = "6618.hk"
    def run(self):
        db = FDatabase()
        table: FTable = db.get_table(self.ticker, "1d")
        rows: List[FCandleData] = table.fetch_rows()
        print(rows[0].time, rows[1].time)

        def calc_price(index_day,interval_day):
            price_list = [x.low_price for x in
                          rows[max(0, index_day - interval_day + 1):min(index_day + 1, len(rows))]]
            return sum(price_list) / interval_day
        def calc_volume(index_day,interval_day):
            volume_list = [x.volume for x in
                          rows[max(0, index_day - interval_day + 1):min(index_day + 1, len(rows))]]
            return sum(volume_list) / interval_day

        index = 0
        data = []

        while index < len(rows):
            if index == 0:
                data.append((rows[0].low_price,rows[0].low_price,rows[0].volume))
            else:
                data.append((calc_price(index,5),calc_price(index,20),calc_volume(index,30)))
            index += 1
        index = 0
        total = 0
        success = 0
        while index < len(rows):
            if data[index][0] < min(rows[index].end_price,rows[index].begin_price):
                profit_price =  rows[index].high_price
                begin_index = index
                while index < len(rows) and data[index][0] < max(rows[index].end_price,rows[index].begin_price):
                    if profit_price < rows[index].high_price:
                        profit_price = rows[index].high_price
                    index += 1
                if begin_index == index:
                    index += 1
                else:
                    total += 1
                    if profit_price - data[begin_index][0] > 1:
                        success += 1
                        print(rows[begin_index],profit_price,data[begin_index])
                    else:
                        print(profit_price,rows[begin_index])
            else:
                index += 1

        print(success, total)

        for i in range(0,5):
            print(data[len(rows) - i - 1],rows[len(rows) - i - 1])

    def run_1(self):
        db = FDatabase()
        table: FTable = db.get_table(self.ticker, "1d")
        rows: List[FCandleData] = table.fetch_rows()
        print(rows[0].time, rows[1].time)

        def calc_price(index_day, interval_day):
            price_list = [x.low_price for x in
                          rows[max(0, index_day - interval_day + 1):min(index_day + 1, len(rows))]]
            return sum(price_list) / interval_day

        def calc_volume(index_day, interval_day):
            volume_list = [x.volume for x in
                           rows[max(0, index_day - interval_day + 1):min(index_day + 1, len(rows))]]
            return sum(volume_list) / interval_day

        index = 0
        data = []

        while index < len(rows):
            if index == 0:
                data.append((rows[0].low_price, rows[0].low_price, rows[0].volume))
            else:
                data.append((calc_price(index, 5), calc_price(index, 20), calc_volume(index, 30)))
            index += 1

        index = 2
        total = 0
        success = 0
        while index < len(rows):
            if data[index - 1][0] > data[index - 1][0]:
                total += 1

            index += 1
if __name__ == "__main__":
    FPolicy_6618().run_1()