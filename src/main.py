from binance import Client
import os
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
    client = Client(api_key)

    data = client.get_historical_klines(
        "ETHUSDT", client.KLINE_INTERVAL_1HOUR, "1 day ago UTC")

    print(len(data))


if __name__ == "__main__":
    main()
