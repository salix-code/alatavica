from alatavica.db import FDatabase,FTable,FCandleData
from datetime import datetime, timedelta

def main():
    ticker = "3933.HK"
    db = FDatabase()
    table: FTable = db.get_table(ticker, "1d")

    rows:[FCandleData] = table.fetch_rows()
    rows.sort(key=lambda x: x.time, reverse=True)
    general_volume = []
    for i in range(2, len(rows)):
        if rows[i].volume > rows[i-1].volume and rows[i].volume > rows[i-2].volume:
            if rows[i - 1].end_price > min(rows[i].begin_price, rows[i].end_price) and rows[i - 2].end_price > min(rows[i].begin_price, rows[i].end_price):
                general_volume.append(i)


    for i in general_volume:
        t = rows[i]
        if i < 7 :
            print("?",t)
            for j in range(0,i):
                c = rows[j]
                if c.low_price < (t.low_price - t.low_price * 0.05):
                    print("-",rows[j])
            continue
        errors = []
        for j in range(i - 7,i):
            c = rows[j]
            if c.low_price < (t.low_price - t.low_price * 0.05):
                errors.append(j)


        if len(errors) > 0:
            print("-",t)
            for e in errors:
                print("\t",rows[e])

        else:
            print("+", t)
    print(rows[0])





if __name__ == '__main__':
    main()


