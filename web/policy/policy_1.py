import dataclasses

from alatavica.datatype import FCandleData
from web.policy.policy_type import FBaseRendingPolicy

@dataclasses
class FRect:
    xmin: float
    xmax: float
    ymin: float
    ymax: float

class FRendingPolicy(FBaseRendingPolicy):
    def __init__(self,rows):
        super().__init__()
        self.rows:[FCandleData] = rows
    def draw(self):
        rect = FRect(-1,-1,-1,-1)
        start_index = len(self.rows) - 1

        prices = list(map(lambda row:(min(row.begin_price,row.adjusted_close),max(row.begin_price,row.adjusted_close)),self.rows))

        xmin = len(prices) - 10
        xmax = len(prices)
        ymin = min([x[0] for x in prices])
        ymax = max([x[1] for x in prices])

