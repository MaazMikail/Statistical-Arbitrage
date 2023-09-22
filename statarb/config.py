"""
Config for Bybit Python API

"""
from pybit import HTTP

# CONFIG

mode = 'test'
timeframe = 60
kline_limit = 200
z_score_window = 15

# api keys
api_key = "BgbuZcvEz6t6Cjet4s"
api_secret = "5sEz7FiRwQrPsO1HGFNrtDlaeoUNVeW5Qo0y"
api_url = "https://api-testnet.bybit.com"
session = HTTP(api_url)

