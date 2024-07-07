import time
import os
import json
import jwt  # PyJWT
import uuid
import websocket  # websocket-client
import pyupbit
import pandas as pd
from dotenv import load_dotenv
from upbit_module import ma_stage, stage1, stage2, stage3, stage4, stage5, stage6

load_dotenv()
access_key = os.environ['ACCESS_KEY']
secret_key = os.environ["SECRET_KEY"]

ticker = "KRW-BTC"

# login
upbit = pyupbit.Upbit(access_key, secret_key)


df = pd.read_csv('./data/btc.csv')

value = []
short = []
middle = []
long = []

last_processed_timestamp = None


ma20 = df['close'].rolling(20).mean().dropna().tolist()
ma60 = df['close'].rolling(60).mean().dropna().tolist()
ma120 = df['close'].rolling(120).mean().dropna().tolist()


# def get_coin_money(balances, ticker):
#     coin_money = 0.0
#     for b in balances:
#         coin_ticker = b['unit_currency'] + "-" + b['currency']
#
#         if ticker == coin_ticker:
#             coin_money = float(b['avg_buy_price']) + float(b['balance'])
#             break
#
#     return coin_money
#
# balances = upbit.get_balances()
#
# print(balances)



def on_message(ws, message):
    global value, short, middle, long, last_processed_timestamp

    data = json.loads(message)

    current_timestamp = data.get('trade_time', None)

    if last_processed_timestamp == current_timestamp:
        pass
    else:
        value.append(data['trade_price'])

    last_processed_timestamp = current_timestamp

    short.append(  (sum(short[-19:]) + sum(value[-1:])) / 20 )
    middle.append(  (sum(middle[-59:]) + sum(value[-1:])) / 20 )
    long.append(  (sum(long[-119:]) + sum(value[-1:])) / 20 )

    current_stage = ma_stage(short, middle, long)

    if current_stage == 'stage1':
        stage1(value,short,middle,long)

    if current_stage == 'stage2':
        stage2(value,short,middle,long)

    if current_stage == 'stage3':
        stage3(value,short,middle,long)

    if current_stage == 'stage4':
        stage4(value,short,middle,long)

    if current_stage == 'stage5':
        stage5(value,short,middle,long)

    if current_stage == 'stage6':
        stage6(value,short,middle,long)







def on_connect(ws):
    print("connected!")

    subscribe_message = [
        {"ticket": "test-websocket"},
        {
            "type": "ticker",
            "codes": ["KRW-BTC"],
            "isOnlyRealtime": True
        },
        {"format": "DEFAULT"}
    ]

    subscribe_data = json.dumps(subscribe_message)

    ws.send(subscribe_data)


def on_error(ws, err):
    print("error: " + err)


def on_close(ws, status_code, msg):
    print("closed!")


payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorization_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorization_token}

ws_app = websocket.WebSocketApp("wss://api.upbit.com/websocket/v1",
                                header=headers,
                                on_message=on_message,
                                on_open=on_connect,
                                on_error=on_error,
                                on_close=on_close)
ws_app.run_forever()
















