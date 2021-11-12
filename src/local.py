try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env")
except:
    pass

import os
import json
from arranger import arranger


def main():
    # Load the local API keys
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    # Load the portfolio
    new_weights = json.load(open("portfolio.json"))

    # Execute the arrange
    valid, logs = arranger(api_key, api_secret, new_weights)


# Execute the main function if the file is run directly
if __name__ == "__main__":
    main()
