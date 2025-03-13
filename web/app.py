from flask import Flask, render_template
from bokeh.plotting import figure
from bokeh.embed import components

from alatavica.db import FDatabase,FTable
from dataclasses import dataclass
from datetime import datetime
@dataclass
class FCandleData:
    begin_price : float
    end_price : float
    low_price : float
    high_price: float
    volume:float


app = Flask(__name__)

#p.line([1, 2, 3], [4, 5, 6], legend_label="线图", line_width=2)
#    p.circle([1, 2, 3], [4, 5, 6], legend_label="散点图", size=10)


class F6618HKRender:
    def __init__(self,ticker):
        self.ticker = ticker
    def draw(self,p:figure):
        db = FDatabase()
        table: FTable = db.get_table(self.ticker, "1d")

        rows = table.fetch_rows()
        rows.sort(key=lambda row: datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'))
        for i in range(0,len(rows)):
            row = rows[i]
            data:FCandleData = FCandleData(row[1], row[2], row[3], row[4], row[5])
            candle_width = 0.8
            candle_height = abs(data.begin_price - data.end_price)
            candle_center = (data.begin_price + data.end_price) / 2
            color = ""
            if data.begin_price > data.end_price:
                color = "green"
            else:
                color = "red"
            p.line([i, i], [data.low_price, data.high_price],line_color = color)
            p.rect(x=i, y=candle_center, width=0.8, height=candle_height,color = color)
@app.route("/")
def index():
    # 创建 Bokeh 图表
    ticker = "6618.HK"
    p = figure(title=ticker, x_axis_label="X 轴", y_axis_label="Y 轴", tools="pan,wheel_zoom,box_zoom,reset,hover")

    render = F6618HKRender(ticker)
    render.draw(p)

    # 将图表转换为 HTML 组件
    script, div = components(p)

    # 渲染模板并传递组件
    return render_template("index.html", script=script, div=div)



if __name__ == "__main__":
    app.run(debug=True)