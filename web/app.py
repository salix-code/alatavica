from flask import Flask, render_template
import bokeh.plotting as plotting
import bokeh.embed as embed

from alatavica.db import FDatabase,FTable
from dataclasses import dataclass
from datetime import datetime

#Open,Close,Low,High,Volume
@dataclass
class FCandleData:
    begin_price : float
    end_price : float
    low_price : float
    high_price: float
    volume:float


app = Flask(__name__)

class F6618HKRender:
    def __init__(self,ticker):
        self.ticker = ticker
    def draw(self,p:plotting.figure):
        db = FDatabase()
        table: FTable = db.get_table(self.ticker, "1d")

        rows:[FCandleData] = table.fetch_rows()
        rows.sort(key=lambda x: x.time)
        for i in range(0,len(rows)):
            data = rows[i]
            candle_width = 0.8
            candle_height = abs(data.begin_price - data.end_price)
            candle_center = (data.begin_price + data.end_price) / 2
            color = "red" if data.begin_price <= data.end_price else "green"
            p.line([i, i], [data.low_price, data.high_price],line_color = color)
            p.rect(x=i, y=candle_center, width= candle_width, height=candle_height,color = color)
@app.route("/")
def index():
    # 创建 Bokeh 图表
    ticker = "6618.HK"
    p = plotting.figure(title=ticker, x_axis_label="X 轴", y_axis_label="Y 轴", tools="pan,wheel_zoom,box_zoom,reset,hover")

    render = F6618HKRender(ticker)
    render.draw(p)

    # 将图表转换为 HTML 组件
    script, div = embed.components(p)

    # 渲染模板并传递组件
    return render_template("index.html", script=script, div=div)


if __name__ == "__main__":
    app.run(debug=True)