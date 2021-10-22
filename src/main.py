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

    x = Client()


if __name__ == "__main__":
    main()
