import os
import requests

from alatavica.datatype import FCandleData
from datetime import datetime

class FDownloadSetting:
    def __init__(self, symbol, start, end):
        self.symbol = symbol
        self.start = start
        self.end = end

class FDownloader:
    def __init__(self):
        self.api_key = "67e614c7d27a66.89808584"
    def download(self,download_setting:FDownloadSetting):
        url = f"https://eodhistoricaldata.com/api/eod/{download_setting.symbol}?api_token={self.api_key}&fmt=json"
        if download_setting.start is not None and download_setting.end is not None:
            url += f"&from={download_setting.start}&to={download_setting.end}"
        response = requests.get(url).json()

        rows = [FCandleData(datetime.strptime(row['date'],"%Y-%m-%d"),
                            row['open'],row['close'],row['low'],row['high'],row['adjusted_close'],row['volume'])
                for row in response]

        return rows

if __name__ == '__main__':
    downloader = FDownloader()
    rows = downloader.download("1816.HK")
    print(rows)