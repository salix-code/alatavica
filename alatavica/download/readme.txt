pip install polygon-api-client


from polygon import RESTClient

# 替换为你的 API 密钥
client = RESTClient("YOUR_API_KEY")

# 获取股票历史数据
data = client.get_aggs("AAPL", 1, "day", "2023-01-01", "2023-10-01")

# 查看数据
for agg in data:
    print(agg)



    Key=mlvUwxPV57JITuJE3NRaBtT03VHKxgqp
    https://polygon.io/docs/rest/stocks/overview




3. Investing.com
Investing.com 提供全球股票数据，包括香港股票。

使用方法：
使用 investpy 库获取数据：
python
复制
import investpy

# 获取腾讯控股（0700.HK）的历史数据
data = investpy.get_stock_historical_data(stock="0700", country="hong kong", from_date="2023-01-01", to_date="2023-10-01")
print(data)
特点：
免费且易于使用。
依赖网页数据，可能会受到网页结构变化的影响。
香港股票的代码格式为 股票代码，例如 0700。



2. EOD Historical Data
EOD Historical Data 提供全球股票数据，包括香港股票。

使用方法：
注册并获取 API 密钥：EOD Historical Data 注册页面。
使用 Python 获取数据：
python
复制
import requests
import pandas as pd

# 替换为你的 EOD Historical Data API 密钥
api_key = "YOUR_API_KEY"

# 获取腾讯控股（0700.HK）的历史数据
symbol = "0700.HK"
url = f"https://eodhistoricaldata.com/api/eod/{symbol}?api_token={api_key}&fmt=json"
response = requests.get(url)

# 将数据转换为 Pandas DataFrame
data = pd.DataFrame(response.json())
print(data)
特点：
支持全球股票、ETF、指数等。
免费版本有 API 调用限制（1 次/秒，1000 次/月）。
香港股票的代码格式为 股票代码.HK，例如 0700.HK。