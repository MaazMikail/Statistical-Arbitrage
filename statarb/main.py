import pandas as pd
from get_symbols import get_symbols
from prices_to_json import store_prices
from cointegration import get_cointegrated_pairs
from plot_trends import plot_trends
import os
import os.path
import json


if __name__ == "__main__":

    if os.path.exists("statarb/price_list.json"):
        print("Price file exists")
    else:
        symbols = get_symbols()
        if len(symbols) > 0:
            store_prices(symbols)

    # Cointegration

    if os.path.exists("statarb/cointegrated_pairs.csv"):
        print("Cointegrated Pairs file exists")
    else:
        print("Calculating Co-Integrated Pairs")
        with open("statarb/price_list.json") as file:
            price_data = json.load(file)
            if len(price_data):
                cint_pairs = get_cointegrated_pairs(price_data)


    
    # plot trends

    sym1 = "EOSUSDT"
    sym2 = "GLMRUSDT"
    with open("statarb/price_list.json") as file:
        price_data = json.load(file)
        if len(price_data) > 0 :
            plot_trends(sym1, sym2, price_data)