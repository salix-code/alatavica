from polygon import RESTClient


class FDownload:
    def __init__(self,ticker_symbol:str):
        self.client = RESTClient("mlvUwxPV57JITuJE3NRaBtT03VHKxgqp")
    def download(self):
        data = self.client.get_aggs("1816.HK", 1, "day", "2025-01-01", "2025-03-01")
        print(data)
    def detail(self):
        details = self.client.get_ticker_details(
            "1816.HK",
        )
        print(details)


FB3QC6DIE6PSSPEB

if __name__ == "__main__":
    download = FDownload(ticker_symbol="1816.HK")
    download.detail()