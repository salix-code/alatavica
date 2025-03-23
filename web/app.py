from flask import Flask, render_template
import bokeh.plotting as plotting
import bokeh.embed as embed

from alatavica.db import FDatabase,FTable
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from bokeh . models import Range1d

#Open,Close,Low,High,Volume
@dataclass
class FCandleData:
    begin_price : float
    end_price : float
    low_price : float
    high_price: float
    volume:float


app = Flask(__name__)

class FRender:
    def __init__(self,ticker):
        self.ticker = ticker
    def draw(self,p:plotting.figure):
        db = FDatabase()
        table: FTable = db.get_table(self.ticker, "1d")

        rows:[FCandleData] = table.fetch_rows()
        rows.sort(key=lambda x: x.time)
        rows = rows[len(rows)-360:]
        x = np.array([x for x in range(0,len(rows))])
        y = np.array([(y.begin_price + y.end_price) / 2 for y in rows ])
        height = np.array([abs(y.begin_price - y.end_price)  for y in rows ])
        color = ["red" if data.begin_price <= data.end_price else "green" for data in rows]
        p.rect(x = x, y = y,width = 0.8,height = height,color= color)
        liney0 = [x.low_price for x in rows]
        liney1 = [y.high_price for y in rows]
        p.segment(x0=x,y0=liney0, x1 = x , y1 =liney1  , color = color , line_width = 1 )

@app.route("/")
def index():
    # 创建 Bokeh 图表
    ticker = "6618.HK"
    p = plotting.figure(title=ticker,sizing_mode = "fixed",
                        width = 5000,height = 600,
                        output_backend = "webgl",
                        x_axis_label="X 轴", y_axis_label="Y 轴",
                        tools="pan,wheel_zoom,box_zoom,reset,hover")

    render = FRender(ticker)
    render.draw(p)

    # 将图表转换为 HTML 组件
    script, div = embed.components(p)

    # 渲染模板并传递组件
    return render_template("index.html", bokeh_script=script, bokeh_div=div)


if __name__ == "__main__":
    app.run(debug=True)