import os
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env")
except:
    pass

from utils import DataClass, Utils
import itertools


def main():
    # Initialize the API
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    data = DataClass(api_key, api_secret)

    # https://youtu.be/mJTrQfzr0R4 - Modern portfolio theory
    # https://youtu.be/vHzlZECzyPE - Correlation

    # Get the data pairs
    pairs = data.get_pairs()

    correlations = []
    days = 20
    for pair in itertools.combinations(pairs[:20], 2):
        try:
            data1 = data.get_data(pair[0], days)
            data2 = data.get_data(pair[1], days)
            corr = Utils.correlation(data1, data2)
            correlations.append((pair[0], pair[1], corr))
        except Exception as e:
            print(f"Encountered exception '{e}' for pair '{pair}'")

    print(correlations)


if __name__ == "__main__":
    main()
