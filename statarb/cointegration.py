# co-integration
import math
from statsmodels.tsa.stattools import coint
from config import z_score_window
from statsmodels.api import OLS
import pandas as pd
import numpy as np


def calculate_zscore(spread):
    df = pd.DataFrame(spread)
    mean = df.rolling(center=False, window=z_score_window).mean()
    std = df.rolling(center=False, window=z_score_window).std()
    x = df.rolling(center = False, window=1).mean()
    df['zscore'] = (x - mean) / std
    
    return df["zscore"].astype(float).values


def calculate_spread(sym1_prices, sym2_prices,hedge_r):
    spread = pd.Series(sym1_prices) - pd.Series(sym2_prices) * hedge_r
    return spread

def calculate_cointegration(sym1_prices, sym2_prices):

    coint_flag = 0
    coint_res = coint(sym1_prices, sym2_prices)
    t_val, p_val, c_value = coint_res[0], coint_res[1], coint_res[2][1]
    hr_model = OLS(sym1_prices, sym2_prices).fit()
    hedge_r = hr_model.params[0]
    spread = calculate_spread(sym1_prices, sym2_prices, hedge_r)
    zeros = len(np.where(np.diff(np.sign(spread)))[0])
    if p_val < 0.5 and t_val < c_value:
        coint_flag = 1

    return (coint_flag, round(t_val,2), round(p_val,2), round(c_value,2), round(hedge_r, 2), zeros)

def get_close_price(prices):
    
    close_prices = []

    for price in prices:
        if math.isnan(price['close']):
            return []
        else:
            close_prices.append(price['close'])
    return close_prices
    

def get_cointegrated_pairs(price_data):

    pair_list = []
    found_list = []

    for symbol in price_data.keys():
        
        for symbol_other in price_data.keys():
            if symbol_other != symbol:
                
                sorted_pair = "".join(sorted(symbol + symbol_other))
                
                if sorted_pair in found_list:
                    continue

                # get close price
                sym1_prices = get_close_price(price_data[symbol])
                sym2_prices = get_close_price(price_data[symbol_other])

                coint_flag, t_Val, p_val, c_val, hedge_r, zeros = calculate_cointegration(sym1_prices, sym2_prices)
                if coint_flag:
                    found_list.append(sorted_pair)
                    pair_list.append({

                        "sym1" : symbol,
                        "sym2" : symbol_other,
                        "p_value" : p_val,
                        "t_value" : t_Val,
                        "c_value" : c_val,
                        "hedge_ratio" : hedge_r,
                        "zero_crossings" : zeros

                    })

    # return pairs
    df = pd.DataFrame(pair_list).sort_values("zero_crossings", ascending=False)
    df.to_csv("cointegrated_pairs.csv")
    print("Cointegrated Pairs Saved!")

    return df