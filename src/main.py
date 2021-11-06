import os
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env")
except:
    pass

from utils import DataClass, get_combinations, get_correlation
from scipy.stats import chisquare


def main():
    # Initialize the API
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    data_class = DataClass(api_key, api_secret)

    # https://youtu.be/mJTrQfzr0R4 - Modern portfolio theory
    # https://youtu.be/vHzlZECzyPE - Correlation

    pairs = [x + "USDT" for x in ["BTC", "ETH", "BNB", "SOL",
                                  "FTM", "LINK", "AVAX", "GRT", "RUNE", "ALGO", "BUSD"
                                  ]]
    cache = {pair: data_class.get_data(pair, 30) for pair in pairs}

    combinations = get_combinations(pairs)
    correlations = []
    for combo in combinations:
        correlation = get_correlation(cache[combo[0]], cache[combo[1]])
        correlations.append(correlation)

    result = chisquare(correlations)
    print(result)
    print(list(zip(combinations, correlations)))


if __name__ == "__main__":
    main()
