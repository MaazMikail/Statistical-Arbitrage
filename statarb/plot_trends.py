from cointegration import get_close_price, calculate_cointegration, calculate_spread, calculate_zscore
import matplotlib.pyplot as plt
import pandas as pd


def plot_trends(sym1, sym2, price_data):
    
    sym1_prices = get_close_price(price_data[sym1])
    sym2_prices = get_close_price(price_data[sym2])

    coint_flag, t_Val, p_val, c_val, hedge_r, zeros = calculate_cointegration(sym1_prices, sym2_prices)
    spread = calculate_spread(sym1_prices, sym2_prices, hedge_r)
    zscore = calculate_zscore(spread)

    # calculate % changes

    df = pd.DataFrame(columns=[sym1, sym2])
    df[sym1] = sym1_prices
    df[sym2] = sym2_prices
    df[f"{sym1}_pct"] = df[sym1] / sym1_prices[0]
    df[f"{sym2}_pct"] = df[sym2] / sym2_prices[0]
    sym1_series = df[f"{sym1}_pct"].astype(float).values
    sym2_series = df[f"{sym2}_pct"].astype(float).values

    # save results
    df_2 = pd.DataFrame()
    df_2[sym1] = sym1_prices
    df_2[sym2] = sym2_prices
    df_2['spread'] = spread
    df_2['zscore'] = zscore
    df_2.to_csv("for_backtesting.csv")
    print("File saved for Backtesting")

    # charts
    fig, axis = plt.subplots(3, figsize=(16,8))
    fig.suptitle(f"Price & Spread - {sym1} vs {sym2}")
    axis[0].plot(sym1_prices)
    axis[0].plot(sym2_series)
    axis[1].plot(spread)
    axis[2].plot(zscore)
    plt.show()