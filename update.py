import sys
from datetime import timedelta,datetime

from alatavica.datatype import FCandleData
from alatavica.download.eod_downloader import FDownloader, FDownloadSetting
from alatavica.db import FDatabase,FTable

def main(symbol_name):
    downloader = FDownloader()
    db = FDatabase()
    table = db.get_table(symbol_name,"1d")
    row:[FCandleData] = table.fetch_rows()

    download_num = 1

    end_day = datetime.today() - timedelta(days=1)

    while download_num > 0:
        download_num = download_num - 1
        start_day = end_day - timedelta(days=360)
        if len(row) > 0:
            if start_day < row[0].time:
                start_day = row[0].time + timedelta(days=1)

        if start_day <= end_day:
            download_setting = FDownloadSetting(symbol_name,start_day.strftime("%Y-%m-%d"),end_day.strftime("%Y-%m-%d"))
            download_rows = downloader.download(download_setting)
            end_day = start_day - timedelta(days=1)
            table.append_rows(download_rows)

    db.save_table(table)

if __name__ == "__main__":
    main("9690.HK")