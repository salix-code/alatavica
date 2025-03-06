
from alatavica.db import FDatabase
from alatavica.download import F1MinuteDownload
from datetime import datetime, timedelta

def main():
    db = FDatabase()

    download = F1MinuteDownload()

    last_row = db.fetch_last("09888.HK","1m")

    current_date = datetime.now()
    three_days_ago = current_date - timedelta(days=3)

    download.start_date = three_days_ago.strftime("%Y-%m-%d")
    download.end_date = current_date.strftime("%Y-%m-%d")
    download.ticker_symbol = "9888.HK"
    data = download.download()


    #db.save_data(rows)

    db.close()


if __name__ == '__main__':
    main()