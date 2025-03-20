from alatavica.db import FDatabase,FTable,FCandleData
from datetime import datetime, timedelta
import sys
import pandas as pd


def main(ticker,interval):
    db = FDatabase()
    table: FTable = db.get_table(ticker, interval)
    rows: [FCandleData] = table.fetch_rows()
    rows.sort(key=lambda x: x.time, reverse=True)

    statics = []
    for row in rows:
        t = pd.to_datetime(row.time)
        t = t.tz_localize("Asia/Shanghai")
        t = t.tz_convert("America/New_York")
        statics_row = [t,row.begin_price < row.end_price,0,0,0]
        statics_row[2] = abs(row.end_price - row.begin_price) / min(row.end_price,row.begin_price)
        statics_row[3] = (row.high_price - max(row.begin_price,row.end_price)) /max(row.begin_price,row.end_price)
        statics_row[4] = abs(row.low_price - max(row.begin_price, row.end_price)) / max(row.begin_price, row.end_price)

        statics.append(statics_row)

    for row in statics:
        print(row)

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        ticker = sys.argv[1]
        interval = sys.argv[2]
        if ticker.endswith(".HK") and interval.endswith("d"):
            main(ticker, interval)
    else:
        main("QID", "1m")
