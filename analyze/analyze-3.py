from alatavica.db import FDatabase,FTable,FCandleData
from datetime import datetime, timedelta
import sys


# 策略1:寻找连续三天突破40均线的
# 成交量的计算，Volume * （B + E） /2
def get_volume_price(x):
    return x.volume * (x.begin_price + x.end_price) / 2
def calc_volume_average(rows,average_num,volume_average):
    if len(rows) > average_num:
        first_volume = sum([get_volume_price(x) for x in rows[0:average_num]])
        volume_average.append(first_volume)
        for k in range(1,len(rows) - average_num + 1):
            volume_average.append(volume_average[len(volume_average) - 1] + get_volume_price(rows[k + average_num - 1]) - get_volume_price(rows[k - 1]))
        for k in range(0,len(volume_average)):
            volume_average[k] /= average_num

def search_jump_up_average_40(rows):
    volume_average = []
    calc_volume_average(rows, 40, volume_average)

    for k in range(0,len(volume_average) - 2):
        bSelected = True
        for j in range(0,3):
            if get_volume_price(rows[k + j]) < volume_average[k + j] * 0.95:
                bSelected = False
                break
        if bSelected:
            print(rows[k])

def main(ticker,interval):
    db = FDatabase()
    table: FTable = db.get_table(ticker, interval)
    rows: [FCandleData] = table.fetch_rows()
    rows.sort(key=lambda x: x.time, reverse=True)

    search_jump_up_average_40(rows)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        ticker = sys.argv[1]
        interval = sys.argv[2]
        if ticker.endswith(".HK") and interval.endswith("d"):
            main(ticker, interval)
    else:
        main("0570.HK", "1d")

