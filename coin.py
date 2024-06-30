import os
import time
import pyupbit
import datetime
import pandas as pd
from dotenv import load_dotenv
import requests
import numpy as np

load_dotenv()

access_key = os.environ['ACCESS_KEY']
secret_key = os.environ['SECRET_KEY']

upbit = pyupbit.Upbit(access_key, secret_key)

target_ticker = "KRW-BTC"
# print(upbit.buy_market_order(target_ticker, 100))

amount = upbit.get_balance(target_ticker)

print(upbit.sell_market_order(target_ticker, amount))

