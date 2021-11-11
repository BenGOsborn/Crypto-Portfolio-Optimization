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
    assets = {}
    for balance in balances:
        asset = balance["asset"]
        ticker = asset + "BUSD" if asset != "BUSD" else asset + "USDT"
        asset_amount = float(balance["free"])

        # Calculate the USD invested in each token
        if float(asset_amount) > 0:
            price = float(client.get_avg_price(symbol=ticker)["price"])
            owned[asset] = price * asset_amount
            assets[asset] = asset_amount

    # Get the weighting of each asset in the portfolio
    total_invested = sum(x for x in owned.values())
    weights = {key: value / total_invested for key, value in owned.items()}

    # Load in the specified portfolio
    new_weights = json.load(open("portfolio.json"))

    # Now we want to go through and find the assets that we will be removing / adding and what we need to swap them out for
    rel_changes = {}

    for key, value in weights.items():
        rel_changes[key] = -value

    for key, value in new_weights.items():
        if key in rel_changes:
            rel_changes[key] += value
        else:
            rel_changes[key] = value

    changes = {key: int(value * total_invested) for key,
               value in rel_changes.items()}

    # Order the lists to have the most subtracted go with the most added first
    pos_changes = {key: changes[key] for key in sorted(
        changes, key=lambda x: changes[x]) if changes[key] <= 0}
    neg_changes = {key: changes[key] for key in sorted(
        changes, key=lambda x: changes[x], reverse=True) if changes[key] > 0}

    # Contains tuples of (pair, amount)
    neg_assets = neg_changes.keys()
    pos_assets = pos_changes.keys()

    # **** CONSIDER THE CASE WHERE YOU CAN ONLY BUY OR SELL ASSETS ALSO - LENGTH OF THE POS OR NEG WILL BE 0 (this cant even happen - there must be a pair to trade or you have run out of money)
    # **** Also consider the case where there is no portfolio ?

    pairs = []
    pos_index = 0
    neg_index = 0
    while True:
        # We will loop through and remove the amounts, once an amount has been depleted then we can get rid of it ?

        # Break when the loop exceeds its restrictions
        if (pos_index >= len(pos_assets) or neg_index >= len(neg_assets)):
            break

        neg_asset = neg_assets[neg_index]
        neg_change = neg_changes[neg_asset]

        pos_asset = pos_assets[pos_index]
        pos_change = pos_changes[pos_asset]

        # 3 cases - one is bigger than the other, or both resources have depleted to 0 ?
        # **** I ALSO NEED SOME SORT OF WAY OF CONVERTING THIS PRICE TO THE ONE SPECIFIED BY THE PAIR ????

        cumulative = neg_change + pos_change

        if cumulative == 0:
            pairs.append((pos_asset + neg_asset, pos_change))

            neg_changes[neg_asset] += pos_change
            pos_changes[pos_asset] -= neg_change

            pos_index += 1
            neg_index += 1

        elif cumulative > 0:
            # In this case we will just set the negative amount to 0 and the positive amount to the cumulative
            pairs.append((pos_asset + neg_asset, abs(neg_change)))

            neg_changes[neg_asset] = 0
            pos_changes[pos_asset] -= neg_change

            neg_index += 1

        else:
            pass


        # Run the program if the file is run directly
if __name__ == "__main__":
    main()
