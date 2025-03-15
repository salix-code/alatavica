from alatavica.db import FDatabase,FTable,FCandleData
from datetime import datetime, timedelta

def volume_less(row_a:FCandleData,row_b:FCandleData):
    return row_a.volume < row_b.volume * 0.95
def price_less(row_a:FCandleData,row_b:FCandleData):
    return row_a.end_price < row_b.end_price
    #return (row_a[1] + row_a[2]) < (row_b[1] + row_b[2])
    #return row_a[1] < (row_b[1] * 1)
    #return max(row_a[1], row_a[2]) < max(row_b[1], row_b[2]) and min(row_a[1], row_a[2]) < min(row_b[1], row_b[2])

def main():
    ticker = "3933.HK"
    db = FDatabase()
    table: FTable = db.get_table(ticker, "1d")

    rows:[FCandleData] = table.fetch_rows()
    rows.sort(key=lambda x: x.time, reverse=True)
    general_volume = []
    for i in range(2, len(rows)):
        if rows[i - 1].end_price > rows[i].end_price and rows[i - 2].end_price > rows[i].end_price:
            if volume_less(rows[i - 1], rows[i]) and volume_less(rows[i - 2], rows[i - 1]):
                if price_less(rows[i], rows[i - 1]) and price_less(rows[i - 1], rows[i - 2]):
                    general_volume.append(i)

    for i in general_volume:
        print(rows[i])

    print(rows[0])





if __name__ == '__main__':
    main()


