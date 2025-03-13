from alatavica.db import FDatabase,FTable
from datetime import datetime, timedelta


def main():
    db = FDatabase()
    table:FTable = db.get_table("6618.HK","1d")
    rows = table.fetch_rows()
    rows.sort(key = lambda row: datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S'))
    #print(rows)
    for i in range(0,len(rows) - 1):
        if rows[i][5] > rows[i + 1][5] and rows[i][3] < rows[i + 1][3]:
            if i < len(rows) - 2:
                if rows[i + 2][3] < rows[i][3] :
                    print(rows[i])
                    print(rows[i + 1])
                    print(rows[i + 2])




if __name__ == '__main__':
    main()