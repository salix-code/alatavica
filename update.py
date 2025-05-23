import os
import sys
import time
from datetime import timedelta,datetime

from alatavica.datatype import FCandleData, FDownloadSetting
from alatavica.download.eod_downloader import download as eod_download
from alatavica.download.yfinance_downloader import download as yfinance_download
from alatavica.db import FDatabase,FTable


def main(*args):
    symbol_names = []
    if len(args) == 0:
        for db_name in os.listdir("db/"):
            if db_name.endswith(".db"):
                symbol_names.append(db_name[:-3])
    else:
        symbol_names.extend(args)

    db = FDatabase()
    end_day = datetime.today()
    for symbol_name in symbol_names:
        table = db.get_table(symbol_name,"1d")
        row:[FCandleData] = table.fetch_rows()
        start_day = end_day - timedelta(days=360)
        if len(row) > 0:
            if start_day < row[0].time:
                start_day = row[0].time + timedelta(days=1)
        if start_day > end_day:
            continue
        download_setting = FDownloadSetting(symbol_name, start_day, end_day)
        download_rows:[FCandleData] = yfinance_download(download_setting)

        with_fail_data = (len(download_rows) == 0)
        if len(download_rows) > 0:
            for row in download_rows:
                if row.begin_price == 0:
                    with_fail_data = True
                    break
        if with_fail_data:
            download_rows = eod_download(download_setting)

        table.append_rows(download_rows)

        db.save_table(table)

        time.sleep(5)


if __name__ == "__main__":
    main("6618.HK","9690.HK","0728.HK","2390.HK")