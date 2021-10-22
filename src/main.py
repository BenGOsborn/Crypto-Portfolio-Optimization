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

    # Get the data pairs
    print(sorted_correlations)


if __name__ == "__main__":
    main()
