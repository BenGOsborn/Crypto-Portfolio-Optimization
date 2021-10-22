from binance import Client
from numpy import number
import pandas as pd


class DataClass:
    def __init__(self, api_key: str, api_secret: str):
        self.__client = Client(api_key, api_secret)

    # Make a dataframe from the data and return it
    def get_data(self, pair: str, days: int):
        data = self.__client.get_historical_klines(
            pair, self.__client.KLINE_INTERVAL_1HOUR, f"{days} day ago UTC")
        cols = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume",
                "num_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"]
        df = pd.DataFrame(data, columns=cols)
        df = df.iloc[:, 0:5]

        return df
