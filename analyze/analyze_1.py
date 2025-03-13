from alatavica.db import FDatabase,FTable
from datetime import datetime, timedelta


def main():
    db = FDatabase()
    table:FTable = db.get_table("6618","1d")
    rows = table.fetch_rows()
    rows.sort(key = lambda row: datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S'))

    n = 2
    pinbar = []
    for i in range(0,len(rows)):
        row = rows[i]
        open_price = row[1]
        close_price = row[2]
        high_price = row[3]
        low_price = row[4]
        if open_price < close_price:
            if n * (open_price - low_price) > (close_price - open_price) and (high_price - close_price) / (close_price - open_price) < 0.01:
                pinbar.append(i)
        elif open_price > close_price:
            if n * (close_price - low_price) > (open_price - close_price) and (high_price - close_price) / (open_price - close_price) < 0.01:
                pinbar.append(i)
        else:
            if high_price - open_price < (open_price - low_price) * 0.5:
                pinbar.append(i)

    for i in pinbar:
        for j in range(0,5):
            print(i,rows[i][0],rows[i+j][1:])

if __name__ == '__main__':
    main()