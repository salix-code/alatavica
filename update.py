
from alatavica.db import FDatabase,FTable
from alatavica.download import FMinuteDownloadSetting,FDownload
from datetime import datetime, timedelta
from datetime import date



class FDownloadRecentlyPolicy:
    def __init__(self,ticker_symbol,interval):
        self.ticker_symbol = ticker_symbol
        self.interval = interval
        self.db = FDatabase()

    def download(self):
        table:FTable = self.db.get_table(self.ticker_symbol,self.interval)
        yesterday = date.today() - timedelta(days=1)
        download_setting = FMinuteDownloadSetting(self.interval)
        down_days = timedelta(days = 0)
        end_day = yesterday
        while down_days.days < 720:
            download_setting.since(end_day)
            start_day = download_setting.get_start_day()
            down_days = yesterday - start_day
            end_day = start_day - timedelta(days=1)

            download = FDownload()
            data = download.download(self.ticker_symbol,download_setting)
            rows = []
            for t, row in data.iterrows():
                rows.append((t.strftime('%Y-%m-%d %H:%M:%S'), row['Open'].iloc[0], row['Close'].iloc[0],
                             row['Low'].iloc[0], row['High'].iloc[0], row['Volume'].iloc[0]))
            rows.sort(key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S"), reverse=True)
            table.append_rows(rows)

            self.db.save_table(table)

    def close(self):
        self.db.close()


def main():
    #p = FDownloadRecentlyPolicy("NIO","1d")
    p = FDownloadRecentlyPolicy("6618.HK","1d")
    p.download()
    p.close()


if __name__ == '__main__':
    main()