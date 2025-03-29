import random

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
from dataclasses import dataclass

from alatavica.datatype import FCandleData


class FCandle:
    def __init__(self):
        self.fig, self.ax = plt.subplots(constrained_layout = True)
        self.candle:[FCandleData] = []
        self.max_price = 0
        self.min_price = 0
        self.line_render = []
        self.fig.set_size_inches(20, 10)

    def set_data(self,data:[FCandleData]):
        total = len(data)
        self.candle = data
        for i in range(0,total):
            if self.max_price == 0 :
                self.max_price = self.candle[i].high_price
                self.min_price = self.candle[i].low_price
            else:
                self.max_price = max(self.max_price,self.candle[i].high_price)
                self.min_price = min(self.min_price,self.candle[i].low_price)

        total = len(self.candle)
        x_max = total + 0.5
        y_min = self.min_price - (self.max_price - self.min_price) / 4 - 0.1
        y_max = (self.max_price - self.min_price) / 4 + self.max_price + 0.1
        self.ax.set_xlim(0, x_max)
        self.ax.set_ylim(y_min, y_max)

    def draw(self):
        candle_render = FCandleRender(self.ax)
        total = len(self.candle)
        for i in range(0,total):
            candle_render.draw(i + 1, self.candle[i])

        for line_batch in self.line_render:
            line_batch.draw(self.ax,self.candle)
        #self.ax.legend()

        self.fig.show()
    def save(self):
        self.fig.savefig("output1.png", dpi=300)

    def add_line(self,line_render):
        self.line_render.append(line_render)

class FCandleRender:
    def __init__(self,ax):
        self.ax = ax

    def draw(self,index,data:FCandleData):
        x_offset = index
        candle_width = 0.8
        if data.begin_price > data.end_price:
            head = lines.Line2D([x_offset, x_offset], [data.begin_price, data.high_price],
                                                 color='green')
            rect = patches.Rectangle((x_offset - candle_width / 2, data.end_price), candle_width,
                                                      data.begin_price - data.end_price, linewidth=1, facecolor='g')
            foot = lines.Line2D([x_offset, x_offset], [data.low_price, data.end_price],
                                                 color='green')
        else:
            head = lines.Line2D([x_offset, x_offset], [data.end_price, data.high_price],
                                                 color='red')
            rect = patches.Rectangle((x_offset - candle_width / 2, data.begin_price), candle_width,
                                                      data.end_price - data.begin_price, linewidth=1, facecolor='r')
            foot = lines.Line2D([x_offset, x_offset], [data.low_price, data.begin_price],
                                                 color='red')
        self.ax.add_line(head)
        self.ax.add_patch(rect)
        self.ax.add_line(foot)



class FAverageLineRender:
    def __init__(self,day):
        self.day = day
    def draw(self,ax,array:[FCandleData]):
        total = len(array)
        if total <= 1:
            return
        value = (array[0].high_price + array[0].low_price)
        points = [value / 2.0]
        for i in range(1,total):
            data:FCandleData = array[i]
            value += (data.high_price + data.low_price)
            if i < self.day:
                points.append(value / (i + 1) / 2.0)
            else:
                value -= (array[i - self.day].high_price + array[i - 5].low_price)
                points.append(value / self.day / 2.0)

        xdata = [x for x in range(1,total+1)]

        line = lines.Line2D(xdata, points,color='black')
        ax.add_line(line)

# 取相领的K线的最高与最低的中间值
class FMoveAverageLineRender:
    def __init__(self,day):
        self.day = day
    def draw(self,ax,array:[FCandleData]):
        total = len(array)
        if total <= 1:
            return
        points = [(array[0].high_price + array[0].low_price) / 2.0]
        for i in range(1,total):
            high_price = max(array[max(0,i - self.day):i], key=lambda item: item.high_price)
            low_price = min(array[max(0,i - self.day):i], key=lambda item: item.low_price)
            points.append((high_price.high_price + low_price.low_price) / 2.0)
        line = lines.Line2D([x for x in range(1,total + 1)], points,color='Red')
        ax.add_line(line)


if __name__ == '__main__':
    candle_data = []
    candle_data.append(FCandleData(6.190000057220459, 6.2, 6.090000152587891, 6.300000190734863))
    candle: FCandle = FCandle()
    candle.set_data(candle_data)

    candle.draw()
    candle.save()


