from config import Config
from api_utils import authenticate, get_announces
import pandas as pd
from parse_data import clean_table


def main():
    config = Config()
    authenticate(config)
    announces_available = get_announces(config)
    dataframe = pd.DataFrame(announces_available)
    dataframe = clean_table(config.TOKEN, dataframe)
    dataframe.to_csv("announces.csv", index=False)


if __name__ == "__main__":
    main()
