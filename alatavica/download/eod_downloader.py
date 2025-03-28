import os
import requests

from alatavica.datatype import FCandleData


class FDownloader:
    def __init__(self):
        self.api_key = "67e614c7d27a66.89808584"
    def download(self,symbol):
        url = f"https://eodhistoricaldata.com/api/eod/{symbol}?api_token={self.api_key}&fmt=json"
        response = requests.get(url).json()
        rows = [FCandleData(row['date'],
                            row['open'],row['close'],row['low'],row['high'],row['adjusted_close'],row['volume'])
                for row in response]

        return rows

if __name__ == '__main__':
    downloader = FDownloader()
    rows = downloader.download("1816.HK")
    print(rows)