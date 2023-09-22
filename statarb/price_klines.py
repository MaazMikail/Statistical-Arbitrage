from config import session, timeframe, kline_limit
import datetime
import time

start_date = 0

if timeframe == 60:
    start_date = datetime.datetime.now() - datetime.timedelta(hours=kline_limit)
elif timeframe == 'D':
    start_date = datetime.datetime.now() - datetime.timedelta(date=kline_limit)

start_date_seconds = int(start_date.timestamp())


def get_prices(symbol):

    prices = session.query_mark_price_kline(

        symbol = symbol,
        interval = timeframe,
        limit = kline_limit,
        from_time = start_date_seconds
    )


    time.sleep(0.1)

    if len(prices['result']) != kline_limit:
        return []
    else:
        return prices['result']

    