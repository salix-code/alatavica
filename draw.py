from alatavica.db import FDatabase,FTable
from datetime import datetime, timedelta
import alatavica.render as Render

def main():
    db = FDatabase()
    table:FTable = db.get_table("NIO","1d")

    rows = table.fetch_rows()
    candle_data = []
    rows.sort(key = lambda row: datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S'))
    for row in rows:
        candle_data.append(Render.FCandleData(row[1],row[2],row[3],row[4]))

    candle:Render.FCandle = Render.FCandle()
    candle.set_data(candle_data[1:100])
    candle.add_line(Render.FAverageLineRender(5))
    candle.add_line(Render.FMoveAverageLineRender(5))
    candle.draw()
    candle.save()



if __name__ == '__main__':
    main()