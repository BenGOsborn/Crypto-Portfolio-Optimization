import os
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env")
except:
    pass

from utils import DataClass, Utils


def main():
    # Initialize the API
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    data = DataClass(api_key, api_secret)

    # https://youtu.be/mJTrQfzr0R4 - Modern portfolio theory
    # https://youtu.be/vHzlZECzyPE - Correlation

    # print(data.get_pairs())

    btc = data.get_data("BTCUSDT", 20)
    eth = data.get_data("ETHUSDT", 20)

    print(Utils.correlation(btc, eth))


if __name__ == "__main__":
    main()
