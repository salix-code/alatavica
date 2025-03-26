import sys

from dateutil.utils import today

from alatavica.db import FDatabase, FTable, FCandleData
from alatavica.download import FDownload, FDownloadSetting
import pandas as pd



class FDownloadRecentlyPolicy:
    def __init__(self,ticker_symbol,interval):
        self.ticker_symbol = ticker_symbol
        self.interval = interval
        self.db = FDatabase()
    def get_start_day(self,start_day):
        day = start_day.isoweekday()
        if day >= 6:
            start_day += pd.Timedelta(days=7 - day + 1)
        return start_day

    def download(self):
        table:FTable = self.db.get_table(self.ticker_symbol,self.interval)
        end_day = pd.to_datetime(today())
        #end_day += pd.Timedelta(hours=8)
        rows = table.fetch_rows()
        ago_day = end_day - pd.Timedelta(weeks=156)
        if len(rows) > 0:
            if ago_day <= pd.to_datetime(rows[0].time):
                ago_day = pd.to_datetime(rows[0].time) + pd.Timedelta(days=1)
            else:
                return
        if self.interval == "1m":
            max_ago_day = end_day - pd.Timedelta(days=8)
            if ago_day < max_ago_day:
                ago_day = max_ago_day
        download_setting = FDownloadSetting(self.interval)
        #[]
        download_setting.end_day = end_day
        while download_setting.end_day > ago_day:
            download_setting.start_day = download_setting.end_day - pd.Timedelta(weeks=4)
            if download_setting.start_day < ago_day:
                download_setting.start_day = ago_day
                if download_setting.start_day > download_setting.end_day:
                    download_setting.end_day = download_setting.start_day
                    continue

            print(f"开始下载{download_setting.start_day} 到{download_setting.end_day}的数据")

            download = FDownload()
            data = download.download(self.ticker_symbol,download_setting)
            #print(data.columns.tolist())
            #('Close', '1816.HK'), ('High', '1816.HK'), ('Low', '1816.HK'), ('Open', '1816.HK'), ('Volume', '1816.HK')]
            column_name = []
            for c in data.columns.tolist():
                column_name.append(c[0])
            print("查找列名顺序:",column_name)
            column_index = [column_name.index(c) for c in ["Open","Close","Low","High","Volume"]]
            rows:[FCandleData] = [
                FCandleData(row[0],row[column_index[0]],row[column_index[1]],row[column_index[2]],row[column_index[3]])
                for row in data.itertuples ( index = True )]

            for row in  rows:
                if row.volume ==0 :
                    print("break")
            rows.sort(key=lambda x: x.time, reverse=True)
            table.append_rows(rows)
            download_setting.end_day = download_setting.start_day - pd.Timedelta(days=1)
        self.db.save_table(table)

def main(ticker_symbol,interval):
    p = FDownloadRecentlyPolicy(ticker_symbol,interval)
    p.download()

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        ticker = sys.argv[1]
        interval = sys.argv[2]
        if ticker.endswith(".HK") and interval.endswith("d"):
            main(ticker,interval)
    else:
        main("1816.HK", "1d")
