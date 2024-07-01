import  pyupbit
import os
import json
import jwt  # PyJWT
import uuid
import websocket  # websocket-client
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

access_key = os.environ['ACCESS_KEY']
secret_key = os.environ['SECRET_KEY']

eth = pd.read_csv('./eth.csv')

eth['short'] = eth['close'].rolling(5).mean()
eth['middle'] = eth['close'].rolling(20).mean()
eth['long'] = eth['close'].rolling(40).mean()

eth.to_csv('eth_ver3.csv')

## 매도랑 매수를 0,1 로 나누면 되겠는디?
## 이걸 먼저 하자

eth_csv = pd.read_csv('./eth_ver3.csv')

eth_csv = eth_csv.dropna()

short = eth_csv['short']
middle = eth_csv['middle']
long = eth_csv['long']

eth_csv['label'] = 0


for i, data in enumerate(eth_csv.iterrows()):
    if short.iloc[i] > middle.iloc[i] > long.iloc[i] and short.iloc[i] > long.iloc[i]:
        eth_csv['label'].iloc[i] = 1
    elif long.iloc[i] > short.iloc[i] > middle.iloc[i] and long.iloc[i] > middle.iloc[i]:
        eth_csv['label'].iloc[i] = 1
    elif short.iloc[i] > long.iloc[i] >  middle.iloc[i] and short.iloc[i] > middle.iloc[i]:
        eth_csv['label'].iloc[i] = 1
    elif middle.iloc[i] > short.iloc[i] > long.iloc[i] and  middle.iloc[i] >  long.iloc[i]:
        eth_csv['label'].iloc[i] = 0
    elif  middle.iloc[i] > long.iloc[i] > short.iloc[i] and middle.iloc[i] > short.iloc[i]:
        eth_csv['label'].iloc[i] = 0
    elif long.iloc[i] > middle.iloc[i] >  short.iloc[i] and long.iloc[i] > short.iloc[i] :
        eth_csv['label'].iloc[i] = 0
eth_csv.to_csv('label_eth.csv')






