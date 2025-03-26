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