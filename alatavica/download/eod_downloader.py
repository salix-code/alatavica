import os
import requests

from alatavica.datatype import FCandleData,FDownloadSetting
from datetime import datetime


def download(download_setting: FDownloadSetting):
    api_key = "67e614c7d27a66.89808584"
    url = f"https://eodhistoricaldata.com/api/eod/{download_setting.symbol}?api_token={api_key}&fmt=json"
    if download_setting.start is not None and download_setting.end is not None:
        url += f"&from={download_setting.start}&to={download_setting.end}"
    response = requests.get(url).json()
    print(response)
    rows = [FCandleData(datetime.strptime(row['date'], "%Y-%m-%d"),
                        row['open'], row['close'], row['low'], row['high'], row['adjusted_close'], row['volume'])
            for row in response]

    return rows
