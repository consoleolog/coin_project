import time
import config
from upbit_module import *
import normal_log

access_key = config.UPBIT_ACCESS_KEY
secret_key = config.UPBIT_SECRET_KEY

ticker = "KRW-BTC"

while True:
    normal_log.set_loglevel("I")

    df = get_income(ticker, "minute1")

    functions = {
        'stage1': stage1,
        'stage2': stage2,
        'stage3': stage3,
        'stage4': stage4,
        'stage5': stage5,
        'stage6': stage6
    }

    current_stage = ma_stage(df['ma20'].iloc[-1], df['ma60'].iloc[-1], df['ma120'].iloc[-1])

    if current_stage in functions:
        functions[current_stage](df['close'], df['ma20'], df['ma60'], df['ma120'])

    time.sleep(60)
