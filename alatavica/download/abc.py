
import requests
import pandas as pd

# 替换为你的 EOD Historical Data API 密钥
api_key = "67e614c7d27a66.89808584"

# 获取腾讯控股（0700.HK）的历史数据
symbol = "0700.HK"
url = f"https://eodhistoricaldata.com/api/eod/{symbol}?api_token={api_key}&fmt=json"
response = requests.get(url)

# 将数据转换为 Pandas DataFrame
data = pd.DataFrame(response.json())
print(data)