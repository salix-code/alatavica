import datetime

import yfinance as yf
import pandas as pd

from datetime import date,timedelta

class FDownloadSetting:
    def __init__(self):
        pass
    def get_interval(self):
        pass
    def get_start_day(self)->datetime.datetime:
        pass
    def get_end_day(self)->datetime.datetime:
        pass

class FDownload:
    def __init__(self):
        pass
    def download(self,ticker_symbol,setting:FDownloadSetting):
        start_data = setting.get_start_day().strftime("%Y-%m-%d")
        end_data = setting.get_end_day().strftime("%Y-%m-%d")
        # 下载数据
        data = yf.download(ticker_symbol, start=start_data, end=end_data, interval=setting.get_interval())
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

            # 显示数据
            print(data)

            # 保存数据到CSV文件
            #data.to_csv(f"{ticker_symbol}_minute_data_{start_data}_{end_data}.csv")
        return data

class FMinuteDownloadSetting(FDownloadSetting):
    def __init__(self,interval:str):
        super().__init__()
        self.interval:str = interval
        self.max_delta_day = 60
        if self.interval == "1m":
            self.max_delta_day = 3
        self.end_day = date.today()
        self.start_day = date.today()
    def get_interval(self)->str:
        return self.interval
    def since(self,end_day):
        self.end_day = end_day
        self.start_day = end_day - timedelta(days=self.max_delta_day)
    def get_start_day(self):
        return self.start_day
    def get_end_day(self):
        return self.end_day






