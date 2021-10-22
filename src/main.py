import os
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env")
except:
    pass

from utils import DataClass


def main():
    # Initialize the API
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    data = DataClass(api_key, api_secret)

    # https://www.youtube.com/watch?v=mJTrQfzr0R4&t=1s

    print(data.get_data("ETHUSDT", 20))
    # print(data.get_pairs())


if __name__ == "__main__":
    main()
