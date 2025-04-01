from functools import reduce

from flask import Flask, render_template
import bokeh.plotting as plotting
import bokeh.embed as embed

from alatavica.datatype import FCandleData
from alatavica.db import FDatabase,FTable
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from bokeh . models import Range1d
from bokeh . models import ColumnDataSource , HoverTool
from bokeh.layouts import Column, Row



app = Flask(__name__)

def format_tip(row:FCandleData):
    return "{time}".format(time = row.time.strftime("%Y-%m-%d"))
class FRender:
    def __init__(self,ticker):
        self.ticker = ticker
        self.figure: plotting.figure = plotting.figure(title=self.ticker, sizing_mode="fixed",
                                             width=4096, height=600,
                                             x_range=Range1d(0, 400, bounds=(0, 600)),
                                             output_backend="webgl",
                                             x_axis_label="X 轴", y_axis_label="Y 轴",
                                             tools="pan,wheel_zoom,box_zoom,reset,hover")

        self.volume_figure = plotting.figure(title=self.ticker, sizing_mode="fixed",
                                             width=4096, height=200,
                                             x_range=Range1d(0, 400, bounds=(0, 600)),
                                             output_backend="webgl",
                                             x_axis_label="X 轴", y_axis_label="Y 轴",
                                             tools="pan,wheel_zoom,box_zoom,reset,hover")

        self.volume_figure.yaxis.visible = False

    def draw_ma(self,rows:[FCandleData],num,color):
        if len(rows) < 2:
            return
        line_y = [rows[0].adjusted_close,rows[0].adjusted_close]

        for i in range(2, len(rows)):
            end_index = i
            start_index = max(0, end_index - num)
            #  2 -> [0,1] -> [0,2)
            # 3 -> [0,1,2] -> [0,3)
            # 60 -> [0,59]  -> [0,60)
            # 61 -> [1,60] -> [1,61)
            s = sum([x.adjusted_close for x in rows[start_index:end_index]]) / (end_index - start_index)
            line_y.append(s)

        data = ColumnDataSource(data={
            'x': [i for i in range(0, len(rows))],
            'y': line_y,
        })
        self.figure.line(x='x', y='y',line_color=color, line_dash="dashed", source=data)

    # 以最大阴线的实顶画水平线
    def draw_1(self,rows:[FCandleData]):
        if len(rows) < 2:
            return

        def add_line(a,b,num):
            h = []

            for i in range(0,min(len(rows),num if num > 0 else len(rows))):
                row:FCandleData = rows[i]
                if a(row) > b(row):
                    n = a(row) - b(row)
                    if len(h) >= 5:
                        sorted(h,key=lambda x:x[1])
                        if n > h[-1][1]:
                            h[-1] = (i,n)
                    else:
                        h.append((i,n))


            print(h)
            self.figure.multi_line(xs=[[x[0],x[0] + 10] for x in h],ys= [[a(rows[p[0]]),a(rows[p[0]])] for p in h],
                                   color = ['green' for x in h])

        add_line(a = lambda x : x.begin_price,b = lambda x : x.adjusted_close,num = 60)
        add_line(a = lambda x : x.adjusted_close,b = lambda x : x.begin_price,num = 60)



    def draw(self):

        db = FDatabase()
        table: FTable = db.get_table(self.ticker, "1d")

        rows:[FCandleData] = table.fetch_rows()
        rows.sort(key=lambda x: x.time)
        rows = rows[max(0,len(rows)-360):]

        candle_data = ColumnDataSource(data={
            'x': np.array([x + 1 for x in range(0,len(rows))]),
            'y': np.array([(y.begin_price + y.adjusted_close) / 2 for y in rows ]),
            'height': np.array([abs(y.begin_price - y.adjusted_close)  for y in rows ]),
            'line_begin_point_y':[x.low_price for x in rows],
            'line_end_point_y':[x.high_price for x in rows],
            'color': ["red" if data.begin_price <= data.adjusted_close else "green" for data in rows],
            'tip': [format_tip(x) for x in rows]}
        )

        self.figure.rect(x = 'x',y = 'y',width=0.8,height = 'height',color = 'color',source = candle_data)
        self.figure.segment(x0='x', y0= 'line_begin_point_y',
                  x1 = 'x' , y1 = 'line_end_point_y'  ,
                  color = 'color' , line_width = 1 ,source = candle_data)

        self.draw_ma(rows,60,"red")
        self.draw_ma(rows,120,"blue")

        self.draw_1(rows)

        volume_data = ColumnDataSource(data={
            'x' : np.array([x + 1 for x in range(0,len(rows))]),
            'y' : np.array([x.volume / 2 for x in rows]),
            'top' : np.array([x.volume for x in rows]),
            'color': ["red" if data.begin_price <= data.adjusted_close else "green" for data in rows]
        })
        self.volume_figure.vbar(x='x', bottom = 0, width=0.8, top='top', color='color', source=volume_data)

        hover = self.figure.select_one(HoverTool)
        hover.tooltips = [("日期", "@tip")]

    def to_components(self)->dict():
        return embed.components(Column(self.figure,self.volume_figure))

@app.route("/<ticker>")
def get_ticker(ticker):
    # 创建 Bokeh 图表
    ticker = "1816.HK" if ticker is None else ticker

    render = FRender(ticker)
    render.draw()
    # 将图表转换为 HTML 组件
    script,div = render.to_components()
    # 渲染模板并传递组件
    return render_template("index.html", bokeh_script = script,bokeh_div = div)
@app.route("/")
def index():
    return get_ticker("9690.HK")

if __name__ == "__main__":
    app.run(debug=True)