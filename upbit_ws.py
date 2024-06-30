import os
import json
import jwt  # PyJWT
import uuid
import websocket  # websocket-client
from dotenv import load_dotenv

load_dotenv()

access_key = os.environ['ACCESS_KEY']
secret_key = os.environ['SECRET_KEY']
short = []
middle = []
long = []
value = []
def on_message(ws, message):
    data = json.loads(message)
    value.append(data['trade_price'])
    if (len(value) % 5) == 0:
        short.append(sum(value[-5:]) / 5)
    elif (len(value) % 20) == 0:
        middle.append(sum(value[-20:]) / 20)
    elif (len(value) % 40) == 0:
        long.append(sum(value[-40:]) / 40)
    print(f'short : {short}')
    print(f'middle: {middle}')
    print(f'long: {long}')
    print(f'value: {value}')

def on_connect(ws):
    print("connected!")
    # Request after connection
    subscribe_message = ('[{"ticket": "test" }, {"type": "trade", "codes": ["KRW-BTC" ] }, {"format": "DEFAULT" } ]')
    ws.send(subscribe_message)

def on_error(ws, err):
    print("error: "+err)


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
