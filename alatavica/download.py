import yfinance as yf
import pandas as pd



class FDownload:
    def __init__(self):
        self.ticker_symbol = "9888.HK"
        self.start_date = "2025-03-03"
        self.end_date = "2025-03-05"
        self.interval = '1m'
    def get_start_date(self):
        return self.start_date
    def get_end_date(self):
        return self.end_date
    def get_interval(self):
        return self.interval

    def download(self):

        start_data = self.get_start_date()
        end_data = self.get_end_date()
        # 下载数据
        data = yf.download(self.ticker_symbol, start=start_data, end=end_data, interval=self.get_interval())
        # 检查数据是否为空
        if data.empty:
            print("没有下载到数据，请检查股票代码和日期范围。")
        else:
            # 检查索引是否已经有时区信息
            if data.index.tz is None:
                # 如果没有时区信息，设置为UTC时区
                data.index = data.index.tz_localize('UTC')

            # 转换为纽约时区
            data.index = data.index.tz_convert('America/New_York')

            # 显示数据
            print(data)

            # 保存数据到CSV文件
            data.to_csv(f"{self.ticker_symbol}_minute_data_{self.get_start_date()}_{self.get_end_date()}.csv")
        return data


class F1MinuteDownload(FDownload):
    def __init__(self):
        super().__init__()
        self.current = ""
    def get_interval(self):
        return "1m"

