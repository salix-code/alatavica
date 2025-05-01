import dataclasses
from typing import List


from alatavica.datatype import FCandleData
from alatavica.db import FDatabase, FTable

@dataclasses.dataclass
class FPolicyData:
    time : str
    min_price : float = dataclasses.field(default = 0)
    max_price : float = dataclasses.field(default = 0)
    factor : tuple[float, float] = dataclasses.field(default = (0, 0))
    profit : tuple[float, float, float] = dataclasses.field(default = (0, 0, 0))


def get_low_price(row:FCandleData) -> float:
    return row.low_price
def get_high_price(row:FCandleData) -> float:
    return row.high_price

class FPolicy_SOXL:
    def __init__(self):
        self.ticker = "SOXL"
        self.interval = 10
    def run(self):
        db = FDatabase()
        table: FTable = db.get_table(self.ticker, "1d")
        rows:List[FCandleData] = table.fetch_rows()
        print(rows[0].time,rows[1].time)

        index = 0
        data = []
        while index < len(rows):
            if index == 0:
                data.append(rows[0].low_price)
            else:
                low_price =  get_low_price(min(rows[max(0,index - self.interval + 1):index + 1],key=lambda x: x.low_price))
                high_price = get_high_price(max(rows[max(0,index - self.interval + 1):index + 1], key=lambda x: x.high_price))
                base_price = (low_price + high_price) / 2.0
                data.append(base_price)
            index += 1

        index = self.interval
        while index < len(rows):
            if data[index] < rows[index].low_price:
                select_index = index
                while index < len(rows) and data[index] < rows[index].high_price:
                    index += 1
                if select_index < index - 1:
                    profit = max([x.high_price for x in rows[select_index + 1:index]]) / rows[select_index].high_price
                    if profit > 1.05:
                        print(rows[select_index],profit * data[select_index],data[select_index],index - select_index)
                    else:
                        print(rows[select_index].time,profit)
                else:
                    print(rows[select_index].time)


            else:
                index += 1





if __name__ == "__main__":
    FPolicy_SOXL().run()