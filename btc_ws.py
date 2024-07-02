import os
import json
import jwt  # PyJWT
import uuid
import websocket  # websocket-client
from dotenv import load_dotenv
import pyupbit
from upbit_module import get_balance, inclination, buy, sell
load_dotenv()
access_key = os.environ['ACCESS_KEY']
secret_key = os.environ['SECRET_KEY']
short = []
middle = []
long = []
value = []
current_price = []

upbit = pyupbit.Upbit(access_key, secret_key)

now = get_balance(upbit, 'BTC')
try:
    sell_result = sell(upbit, "KRW-BTC", now)
    print(sell_result)
except Exception as e:
    print(f"===== ERROR : {e} =====")

exit()
load_dotenv()

access_key = os.environ['ACCESS_KEY']
secret_key = os.environ['SECRET_KEY']
short = []
middle = []
long = []
value = []
current_price = []

upbit = pyupbit.Upbit(access_key, secret_key)

target_price = 6000

def get_balance(ticker):
    balances = upbit.get_balances()  # Assuming upbit.get_balance() returns a single float
    print(balances)
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0






def on_message(ws, message):
    global value, short, middle, long

    data = json.loads(message)

    value.append(data['trade_price'])

    print(len(value))

    if len(value) == 1:
        BTC_now = get_balance('BTC')
        if BTC_now == 0:
            print(f"{value[-1]} price: Buy")
            current_price.append(value[-1])
            msg = upbit.buy_market_order("KRW-BTC", 6000)
            if msg == None:
                print("이미 샀음")
    else:
        pass

    if current_price[-1] < value[-1]:
        BTC_now = get_balance('BTC')
        print(f"{value[-1]} price: Sell")
        msg = upbit.sell_market_order('KRW-BTC', BTC_now)
        for m in msg:
            if m == 'error':
                print("이미 팔았음")

                BTC_now = get_balance('BTC')
                if BTC_now == 0:
                    print(f"{value[-1]} price: Buy")
                    current_price.append(value[-1])
                    msg = upbit.buy_market_order("KRW-BTC", 6000)
                    if msg == None:
                        print("이미 샀음")

            else:
                print(msg)
    else:
        pass




def on_connect(ws):
    print("connected!")
    # Request after connection
    # a = ('[{"ticket": "test" }, {"type": "trade", "codes": ["KRW-ETH" ] }, {"format": "DEFAULT" } ]')

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

## 매도 시점으로 가자
# 1. 일단 web socket 으로 현재를 가져오잖아 그럼 그냥 예전걸 미리 저장해 놓으면 안되나
