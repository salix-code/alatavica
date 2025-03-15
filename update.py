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
    def get_end_day(self,end_day):
        day = end_day.isoweekday()
        if day >= 6:
            end_day -= pd.Timedelta(days=(day - 5))
        return end_day
    def download(self):
        table:FTable = self.db.get_table(self.ticker_symbol,self.interval)
        end_day = self.get_end_day(pd.to_datetime(today()))
        end_day += pd.Timedelta(hours=8)

        rows = table.fetch_rows()

        ago_day = end_day - pd.Timedelta(weeks=156)
        if len(rows) > 0:
            if ago_day <= pd.to_datetime(rows[0].time):
                ago_day = pd.to_datetime(rows[0].time) + pd.Timedelta(days=1)
            else:
                return
        download_setting = FDownloadSetting(self.interval)
        #[]
        download_setting.end_day = end_day
        while download_setting.end_day > ago_day:
            download_setting.start_day = self.get_start_day(download_setting.end_day - pd.Timedelta(weeks=4))
            if download_setting.start_day < ago_day:
                download_setting.start_day = ago_day

            if download_setting.start_day > download_setting.end_day:
                download_setting.end_day = download_setting.start_day
                continue

            print(f"开始下载{download_setting.start_day} 到{download_setting.end_day}的数据")

            download = FDownload()
            data = download.download(self.ticker_symbol,download_setting)
            rows:[FCandleData] = []
            num = 0
            for t, row in data.iterrows():
                rows.append(FCandleData(t, row['Open'].iloc[0], row['Close'].iloc[0],
                             row['Low'].iloc[0], row['High'].iloc[0], row['Volume'].iloc[0]))
                num += 1
            rows.sort(key=lambda x: x.time, reverse=True)
            table.append_rows(rows)
            self.db.save_table(table)

            download_setting.end_day = download_setting.start_day - pd.Timedelta(weeks=4)





def main():
    #p = FDownloadRecentlyPolicy("NIO","1d")
    #p = FDownloadRecentlyPolicy("3311.HK","1d")
    # 华新水泥
    #p = FDownloadRecentlyPolicy("6655.HK","1d")
    #
    #p = FDownloadRecentlyPolicy("0586.HK", "1d")
    p = FDownloadRecentlyPolicy("3933.HK", "1d")
    p.download()



if __name__ == '__main__':
    main()