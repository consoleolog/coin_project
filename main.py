import pyupbit
import time
import os
import pandas as pd
from dotenv import load_dotenv
from upbit_module import *

load_dotenv()

access_key = os.environ['ACCESS_KEY']
secret_key = os.environ['SECRET_KEY']

ticker = "KRW-BTC"

current_time = time.strftime('%Y-%m-%d_%H%M', time.localtime(time.time()))

while True:
    price = pyupbit.get_ohlcv(ticker, interval='day')
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=360)
    df['close'] = df['close'].astype(int)
    df['ma20'] = df['close'].astype(int).rolling(20).mean()
    df['ma60'] = df['close'].astype(int).rolling(60).mean()
    df['ma120'] = df['close'].astype(int).rolling(120).mean()

    df['ema10'] = df['close'].ewm(span=9, adjust=False).mean()

    current_stage = ma_stage(df['ma20'].iloc[-1], df['ma60'].iloc[-1], df['ma120'].iloc[-1])

    if current_stage == 'stage1':
        stage1(df['close'], df['ma20'], df['ma60'], df['ma120'])

    if current_stage == 'stage2':
        stage2(df['close'], df['ma20'], df['ma60'], df['ma120'])

    if current_stage == 'stage3':
        stage3(df['close'], df['ma20'], df['ma60'], df['ma120'])

    if current_stage == 'stage4':
        stage4(df['close'], df['ma20'], df['ma60'], df['ma120'])

    if current_stage == 'stage5':
        stage5(df['close'], df['ma20'], df['ma60'], df['ma120'])

    if current_stage == 'stage6':
        stage6(df['close'], df['ma20'], df['ma60'], df['ma120'])

    time.sleep(60)
