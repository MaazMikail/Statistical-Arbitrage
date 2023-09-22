from config import session

def get_symbols():
    tradable_symbols = []
    symbols = session.query_symbol()
    if "ret_msg" in symbols.keys():
        if symbols['ret_msg'] == 'OK':
            symbols = symbols['result']

    tradable_symbols = [sym for sym in symbols if sym['quote_currency']=='USDT' if sym["status"]=="Trading"]
    
    return tradable_symbols