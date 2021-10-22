from binance import Client
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env")
except:
    pass


def main():
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    x = Client(api_key)


if __name__ == "__main__":
    main()
