import datetime

import yfinance as yf
import pandas as pd

from datetime import date,timedelta

from dateutil.utils import today
from yfinance.exceptions import YFRateLimitError

from alatavica.datatype import FDownloadSetting


def download(setting:FDownloadSetting):

    # 下载数据
    try:
        data = yf.download(setting.symbol, start= setting.start, end= setting.end,
                           interval="1d",repair=True,progress=False)
    except YFRateLimitError as e :
        pass
    # 检查数据是否为空
    if data.empty:
        print("没有下载到数据，请检查股票代码和日期范围。")
    else:
        # 检查索引是否已经有时区信息
        if data.index.tz is None:
            # 如果没有时区信息，设置为UTC时区
            data.index = data.index.tz_localize('UTC')

        # 转换为纽约时区
        data.index = data.index.tz_convert('Asia/Shanghai')


        # 保存数据到CSV文件
        #data.to_csv(f"{ticker_symbol}_minute_data_{start_data}_{end_data}.csv")
    return data








