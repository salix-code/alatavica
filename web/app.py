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

#p.line([1, 2, 3], [4, 5, 6], legend_label="线图", line_width=2)
#    p.circle([1, 2, 3], [4, 5, 6], legend_label="散点图", size=10)


class F6618HKRender:
    def __init__(self,ticker):
        self.ticker = ticker
    def draw(self,p:plotting.figure):
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

@app.route("/analyze")
def analyze_1():
    ticker = "6618.HK"
    db = FDatabase()
    table: FTable = db.get_table(ticker, "1d")
    db.close()

    rows = table.fetch_rows()
    selects = []
    for i in range(1,len(rows) - 1):
        data:FCandleData = FCandleData(rows[i][1], rows[i][2], rows[i][3], rows[i][4], rows[i][5])
        prev:FCandleData = FCandleData(rows[i - 1][1], rows[i - 1][2], rows[i -1 ][3], rows[i -1][4], rows[i - 1][5])
        if data.begin_price > data.end_price:
            if data.volume > prev.volume * 2:
                selects.append(i)
    selects_2 = []
    for i in selects:
        curr: FCandleData = FCandleData(rows[i][1], rows[i][2], rows[i][3], rows[i][4], rows[i][5])
        post:FCandleData = FCandleData(rows[i + 1][1], rows[i + 1][2], rows[i + 1 ][3], rows[i +1][4], rows[i + 1][5])
        if post.volume > curr.volume and curr.end_price < post.end_price:
            selects_2.append(i)


    for k in selects_2:
        print(rows[k])





if __name__ == "__main__":
    app.run(debug=True)