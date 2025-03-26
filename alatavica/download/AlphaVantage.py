from alpha_vantage.timeseries import TimeSeries
import pandas as pd

api_key = 'FB3QC6DIE6PSSPEB' # 免费申请：https://www.alphavantage.co/
ts = TimeSeries ( key = api_key , output_format = 'pandas' ) # 获取苹果股票日线数据
data , meta_data = ts.get_daily ( symbol = '1816.HK' )
print (data.head())
# 清洗数据（Alpha Vantage 的列名与yfinance不同）
#data = data.rename ( columns = { '1. open' : 'Open' , '2. high' : 'High' , '3. low' : 'Low' , '4. close' : 'Close' , '5. volume' : 'Volume' } )

print(data)


14282a531f9344c2b35ebe6875483c1c


from twelvedata import TDClient import matplotlib . pyplot as plt # 初始化客户端 td = TDClient ( apikey = "YOUR_API_KEY" ) # 获取苹果(AAPL)日线数据 ts = td . time_series ( symbol = "AAPL" , interval = "1day" , outputsize = 10 , # 获取最近10条 ) . as_pandas ( ) # 简单可视化 t

# 获取腾讯港股数据 hk_data = td . time_series ( "HKEX:0700" , interval = "1day" ) . as_pandas ( )# s [ 'close' ] . plot ( title = "AAPL Close Price" ) plt . show ( )