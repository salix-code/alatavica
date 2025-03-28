from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class FCandleData:
    time: datetime
    begin_price : float
    end_price : float
    low_price : float
    high_price: float
    adjusted_close:float
    volume:float