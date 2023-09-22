from price_klines import get_prices
import json


def store_prices(symbols):
    
    count = 0
    price_history = {}

    for symbol in symbols:
        sym = symbol['name']
        prices = get_prices(sym)
        if len(prices) > 0:
            price_history[sym] = prices
            count += 1
            print(f"{count} items stored")
        else:
            print(f"{count} items not stored")

    
    if len(price_history) > 0:
        with open("price_list.json", 'w') as file:
            json.dump(price_history, file, indent=4)
        print("Prices Stored!!")