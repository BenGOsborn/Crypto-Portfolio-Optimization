# Rearranges the users portfolio to the new assets based off of their old portfolio

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env")
except:
    pass

from binance import Client

# Steps
# 1. Get the previous percentages and compare them with the new ones
# 2. Seperate the ones that are decreasing in allocation vs the ones that are gaining in allocation
# 3. Remove the specified amount from the ones that are decreasing and then use this to fill up the ones that are increasing bit by bit


def main():
    # Initialize the API
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    client = Client(api_key, api_secret)

    balances = client.get_account()["balances"]
    owned = {}
    for balance in balances:
        if float(balance["free"]) > 0:
            owned[balance["asset"]] = float(balance["free"])

    print(owned)


if __name__ == "__main__":
    main()
