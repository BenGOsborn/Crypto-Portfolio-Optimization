# Rearranges the users portfolio to the new assets based off of their old portfolio

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env")
except:
    pass

from binance import Client
import os
import json

# Steps
# 1. Get the previous percentages and compare them with the new ones
# 2. Seperate the ones that are decreasing in allocation vs the ones that are gaining in allocation
# 3. Remove the specified amount from the ones that are decreasing and then use this to fill up the ones that are increasing bit by bit


def main():
    # Initialize the API
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    client = Client(api_key, api_secret)

    # Get the owned balances
    balances = client.get_account()["balances"]
    owned = {}
    for balance in balances:
        ticker = balance["asset"]
        ticker = ticker + "BUSD" if ticker != "BUSD" else ticker + "USDT"
        asset_amount = float(balance["free"])

        # Calculate the USD invested in each token
        if float(asset_amount) > 0:
            price = float(client.get_avg_price(symbol=ticker)["price"])
            owned[ticker] = price * asset_amount

    # Get the weighting of each asset in the portfolio
    total_invested = sum(x for x in owned.values())
    weights = {key: value / total_invested for key, value in owned.items()}

    print(weights)

    # Load in the specified portfolio
    new_weights = json.load(open("portfolio.json"))
    print(new_weights)


if __name__ == "__main__":
    main()
