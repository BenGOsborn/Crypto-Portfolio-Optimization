from binance import Client
import math

# Steps
# 1. Get the previous percentages and compare them with the new ones
# 2. Seperate the ones that are decreasing in allocation vs the ones that are gaining in allocation
# 3. Remove the specified amount from the ones that are decreasing and then use this to fill up the ones that are increasing bit by bit

USD_STABLECOINS = ["BUSD", "USDT"]
DECIMALS = 2


def round_floor(number: float, decimals: int):
    return math.floor(number * decimals) / decimals


def arrange(api_key: str, api_secret: str, new_weights: dict) -> tuple:
    '''
    Rearranges the users portfolio to the new assets based off of their old portfolio
    '''

    if sum(x for x in new_weights.values()) != 1:
        return (False, "Portfolio weights must sum to one")

    # Initialize the API
    client = Client(api_key, api_secret)

    # Get the owned balances
    balances = client.get_account()["balances"]
    owned = {}
    assets = {}
    for balance in balances:
        asset = balance["asset"]
        ticker = asset + \
            USD_STABLECOINS[0] if asset != USD_STABLECOINS[0] else asset + \
            USD_STABLECOINS[1]
        asset_amount = float(balance["free"])

        # Calculate the USD invested in each token
        if float(asset_amount) > 0:
            price = float(client.get_avg_price(symbol=ticker)["price"])
            owned[asset] = price * asset_amount
            assets[asset] = asset_amount

    # Get the weighting of each asset in the portfolio
    total_invested = sum(x for x in owned.values())
    weights = {key: value / total_invested for key, value in owned.items()}

    # Now we want to go through and find the assets that we will be removing / adding and what we need to swap them out for
    rel_changes = {}

    for key, value in weights.items():
        rel_changes[key] = -value

    for key, value in new_weights.items():
        if key in rel_changes:
            rel_changes[key] += value
        else:
            rel_changes[key] = value

    changes = {key: value * total_invested for key,
               value in rel_changes.items()}

    # Order the lists to have the most subtracted go with the most added first
    pos_changes = {key: changes[key] for key in sorted(
        changes, key=lambda x: changes[x]) if changes[key] > 0}
    neg_changes = {key: changes[key] for key in sorted(
        changes, key=lambda x: changes[x], reverse=True) if changes[key] <= 0}

    # Contains tuples of (pair, amount)
    neg_assets = list(neg_changes.keys())
    pos_assets = list(pos_changes.keys())

    pairs = []
    pos_index = 0
    neg_index = 0
    while True:
        # Break when the loop exceeds its restrictions
        if (pos_index >= len(pos_assets) or neg_index >= len(neg_assets)):
            break

        # Get the assets and changes
        neg_asset = neg_assets[neg_index]
        neg_change = neg_changes[neg_asset]

        pos_asset = pos_assets[pos_index]
        pos_change = pos_changes[pos_asset]

        # Record the combined remainder and the ticker
        cumulative = pos_change + neg_change
        new_ticker = (pos_asset, neg_asset)

        # Get the trading worths in USD for the assets + the conversion rate
        pos_usd_rate = float(client.get_avg_price(symbol=(
            pos_asset + USD_STABLECOINS[0] if pos_asset != USD_STABLECOINS[0] else pos_asset + USD_STABLECOINS[1]))["price"])
        neg_usd_rate = float(client.get_avg_price(symbol=(
            neg_asset + USD_STABLECOINS[0] if neg_asset != USD_STABLECOINS[0] else neg_asset + USD_STABLECOINS[1]))["price"])
        conversion = pos_usd_rate / neg_usd_rate

        if cumulative == 0:
            qty = round_floor(pos_change / pos_usd_rate, DECIMALS)
            pairs.append((new_ticker, qty, conversion))

            neg_changes[neg_asset] += pos_change
            pos_changes[pos_asset] -= neg_change

            pos_index += 1
            neg_index += 1

        elif cumulative > 0:
            qty = round_floor(abs(neg_change) / pos_usd_rate, DECIMALS)
            pairs.append((new_ticker, qty, conversion))

            neg_changes[neg_asset] = 0
            pos_changes[pos_asset] -= neg_change

            neg_index += 1                # **** ASSET1:ASSET2
            # **** Calculate amount of ASSET2 available
            # **** Sell ASSET2 for USDT
            # **** Swap USDT for ASSET1
            qty = round_floor(pos_change / pos_usd_rate, DECIMALS)
            pairs.append((new_ticker, qty, conversion))

            neg_changes[neg_asset] += pos_change
            pos_changes[pos_asset] = 0

            pos_index += 1

    # Create the buy orders for the different assets
    log = ""
    for pair in pairs:
        # If the pair does not exist, then switch it for BUSD / USDT and back to the other asset
        log += "\n"
        try:
            log += f"Executing BUY order for '{pair[0]}' of amount '{pair[1]}'\n"

            order = client.create_order(
                symbol="".join(pair[0]),
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=pair[1]
            )
            log += f"{order}\n"

        except Exception as e:
            log += str(e) + " - trying to trade assets to USD seperately" + "\n"
            try:
                # Create a sell order for the asset in terms of BUSD / USDT and then resell it for the other asset - ASSUME THAT BUSD / USDT IS ALWAYS VALID

                # Sell the given amount of the token for USD
                sell_pair = pair[0][1] + USD_STABLECOINS[0]
                sell_quantity = round_floor(pair[1] / pair[2], DECIMALS)
                sell_order = client.create_order(
                    symbol=sell_pair,
                    side=Client.SIDE_SELL,
                    type=client.ORDER_TYPE_MARKET,
                    quantity=sell_quantity
                )
                log += f"{sell_order}\n"

                # Buy back the other token in the original pair withthe amount exchanged in USD
                buy_pair = pair[0][0] + USD_STABLECOINS[0]
                buy_quantity = round_floor(pair[1], DECIMALS)
                buy_order = client.create_order(
                    symbol=buy_pair,
                    side=Client.SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=buy_quantity
                )
                log += f"{buy_order}\n"

            except Exception as e:
                log += str(e) + "\n"

    return (True, log)
