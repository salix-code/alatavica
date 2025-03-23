from tigeropen.common.consts import (Language,        # 语言
                                Market,           # 市场
                                BarPeriod,        # k线周期
                                QuoteRight)       # 复权类型
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.common.util.signature_utils import read_private_key
from tigeropen.quote.quote_client import QuoteClient

def get_client_config():
    """
    https://quant.itigerup.com/#developer 开发者信息获取
    """
    # 港股牌照需用 props_path 参数指定token路径，如 '/Users/xxx/xxx/', 如不指定则取当前路径
    # 必须使用关键字参数指定 props_path
    client_config = TigerOpenClientConfig(props_path='/Users/ruiqingkong/Works/')
    return client_config

# 调用上方定义的函数生成用户配置ClientConfig对象
client_config = get_client_config()

# 调用上方定义的函数生成用户配置ClientConfig对象
#client_config = get_client_config()

# 随后传入配置参数对象来初始化QuoteClient
quote_client = QuoteClient(client_config)

# 完成初始化后，就可以调用quote_client方法来使用调用QuoteClient对象的get_stock_brief方法来查询股票行情了
# 此处以美国股票为例，关于其他支持的市场及标的类型，请参考文档的基本操作部分。
# 对于使用多台设备调用API的用户，需先调用grab_quote_permission进行行情权限的抢占，详情请见基本操作-行情类-通用-grab_quote_permission方法说明
permissions = quote_client.grab_quote_permission()

#输出list类型的行情权限权限列表
print(permissions)

# 调用API查询股票行情
stock_price = quote_client.get_timeline_history(['00700'],"2025-03-19")

# 查询行情函数会返回一个包含当前行情快照的pandas.DataFrame对象，见返回示例。具体字段含义参见get_stock_briefs方法说明
print(stock_price)