from binance import Client
import os
import pandas as pd
import numpy as np
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env")
except:
    pass


def main():
    # Initialize the API
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    client = Client(api_key, api_secret)

    data = client.get_historical_klines(
        "ETHUSDT", client.KLINE_INTERVAL_1HOUR, "1 day ago UTC")

    cols = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume",
            "num_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"]

    df = pd.DataFrame(data, columns=cols)
    df = df.iloc[:, 0:5]
    print(df)


if __name__ == "__main__":
    main()
