import random

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
from dataclasses import dataclass

@dataclass
class FCandleData:
    begin_price : float
    end_price : float
    high_price : float
    low_price : float

class FCandleView:
    rect : patches.Rectangle
    head : lines.Line2D
    foot : lines.Line2D
    def __init__(self):
        pass

class FCandleItem:
    view : FCandleView
    data : FCandleData
    def __init__(self):
        self.view = FCandleView()
        self.data = FCandleData(0,0,0,0)


def draw_one_candle(index,candle_item : FCandleItem):
    candle_item.view = FCandleView()
    data = candle_item.data
    x_offset = index + 1
    candle_width = 0.8

    if candle_item.data.begin_price > candle_item.data.end_price:
        candle_item.view.head = lines.Line2D([x_offset, x_offset], [data.begin_price, data.high_price],
                                             color='green')
        candle_item.view.rect = patches.Rectangle((x_offset - candle_width / 2, data.end_price), candle_width,
                                                  data.begin_price - data.end_price, linewidth=1, facecolor='g')
        candle_item.view.foot = lines.Line2D([x_offset, x_offset], [data.low_price, data.end_price],
                                             color='green')
    else:
        candle_item.view.head = lines.Line2D([x_offset, x_offset], [data.end_price, data.high_price],
                                             color='red')
        candle_item.view.rect = patches.Rectangle((x_offset - candle_width / 2, data.begin_price), candle_width,
                                                  data.end_price - data.begin_price, linewidth=1, facecolor='r')
        candle_item.view.foot = lines.Line2D([x_offset, x_offset], [data.low_price, data.begin_price],
                                             color='red')

class FCandle:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.candle:[FCandleItem] = []
    def random_data(self):
        total = 72
        for i in range(0,total):
            self.candle.append(FCandleItem())
            begin_price = random.random() * 200
            end_price = random.random() * 200
            if begin_price > end_price:
                high_price = begin_price + random.random() * (200 - begin_price)
                low_price = random.random() * end_price
            else:
                high_price = end_price + random.random() * (200 - end_price)
                low_price = random.random() * begin_price

            self.candle[i].data = FCandleData(begin_price,end_price,high_price,low_price)

    def draw(self):
        render = FCandleRender(self.ax)
        total = len(self.candle)
        draw_num = 72
        render.set_range(0, 72, 0, 200)

        for i in range(0,total):
            draw_one_candle(i, self.candle[i])

        for i in range(0,min(draw_num,total)):
            self.ax.add_line(self.candle[i].view.head)
            self.ax.add_patch(self.candle[i].view.rect)
            self.ax.add_line(self.candle[i].view.foot)
        self.fig.show()


class FCandleRender:
    def __init__(self,ax):
        self.ax = ax

    def set_range(self,x_min,x_max,y_min,y_max):
        self.ax.set_xlim(x_min,x_max)
        self.ax.set_ylim(y_min,y_max)




candle:FCandle = FCandle()
candle.random_data()
candle.draw()


