import datetime

import yfinance as yf
from yfinance.exceptions import YFRateLimitError

from alatavica.datatype import FDownloadSetting


def download(setting:FDownloadSetting):

    try:
        start = setting.start.strftime("%Y-%m-%d")
        end = setting.end.strftime("%Y-%m-%d")
        data = yf.download(setting.symbol, start= start, end= end,
                           interval="1d",repair=True,progress=False)
    except YFRateLimitError as e :
        print(e)
    else:
        if data.empty:
            return []
        # 检查索引是否已经有时区信息
        if data.index.tz is None:
            # 如果没有时区信息，设置为UTC时区
            data.index = data.index.tz_localize('UTC')
        if setting.symbol.endswith('.HK'):
            data.index = data.index.tz_convert('Asia/Shanghai')

        return data







