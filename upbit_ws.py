import os
import json
import jwt  # PyJWT
import uuid
import websocket  # websocket-client
from dotenv import load_dotenv
import pyupbit

load_dotenv()

access_key = os.environ['ACCESS_KEY']
secret_key = os.environ['SECRET_KEY']
short = []
middle = []
long = []
value = []

upbit = pyupbit.Upbit(access_key, secret_key)


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

ETH_now = get_balance('ETH')
# print(f"{value[-1]} price: Sell")
msg = upbit.sell_market_order('KRW-ETH', ETH_now)
def on_message(ws, message):
    global value, short, middle, long

    data = json.loads(message)
    value.append(data['trade_price'])

    if len(value) >= 10:
        avg_short = sum(value[-10:]) / 10
        short.append(avg_short)

    if len(value) >= 40:
        avg_middle = sum(value[-40:]) / 40
        middle.append(avg_middle)

    if len(value) >= 140:
        avg_long = sum(value[-140:]) / 140
        long.append(avg_long)

    if len(value) >= 140:



        # 1
        if short[-1] > middle[-1] > long[-1] and short[-1] > long[-1]:  # 단 중 장
            print(f"{value[-1]} 안정 하게 상승중")

            # 둘의 차이가 거의 안날 때 팔아
            if 1 > short[-1] - middle[-1] > 0 or 0 > short[-1] - middle[-1] > -1 :
                ETH_now = get_balance('ETH')
                print(f"{value[-1]} price: Sell")
                msg = upbit.sell_market_order('KRW-ETH', ETH_now)
                for m in msg:
                    if m == 'error':
                        print("이미 팔았음")
                    else:
                        print(msg)


            # 기울기가 세개가 다 우상향이면 그냥 사
            if (short[-1] - short[-2])/10 > 0 and (long[-1] - long[-2])/140 > 0 and (middle[-1] - middle[-2])/40 > 0:
                print("그래프 세개 다 우 상향 ")
                ETH_now = get_balance('ETH')
                if ETH_now == 0:
                    print(f"{value[-1]} price: Buy")
                    msg = upbit.buy_market_order("KRW-ETH", 8000)
                    if msg == None:
                        print("이미 샀음")
                    else:
                        print(msg)







        # 2
        elif middle[-1] > short[-1] > long[-1] and middle[-1] > long[-1]:  # 중 단 장
            print(f"{value[-1]} 상승 추세의 끝")
            # 중기선과 장기선이 우상향 이면 그냥 패스
            if (long[-1] - long[-2])/140 > 0 and (middle[-1] - middle[-2])/40 > 0:
                pass





        # 3
        elif middle[-1] > long[-1] > short[-1] and middle[-1] > short[-1]:  # 중 장 단
            print(f"{value[-1]} 하락 추세의 시작")
            if value[-1] < value[-2]:
                try:
                    ETH_now = get_balance('ETH')
                    print(f"{value[-1]} price: Sell")
                    msg = upbit.sell_market_order('KRW-ETH', ETH_now)
                    for m in msg:
                        if m == 'error':
                            print("이미 팔았음")
                        else:
                            print(msg)
                    pass
                except:
                    pass



        # 4
        elif long[-1] > middle[-1] > short[-1] and long[-1] > short[-1]:  # 장 중 단
            print(f"{value[-1]} 안정 하락")
            if value[-1] < value[-2]:
                try:
                    ETH_now = get_balance('ETH')
                    print(f"{value[-1]} price: Sell")
                    msg = upbit.sell_market_order('KRW-ETH', ETH_now)
                    for m in msg:
                        if m == 'error':
                            print("이미 팔았음")
                        else:
                            print(msg)
                    pass
                except:
                    pass
            # 팔아




        # 5
        elif long[-1] > short[-1] > middle[-1] and long[-1] > middle[-1]: # 장 단 중
            # 전 단계가 4단계면 구매하자
            print(f"{value[-1]} 하락 추세의 끝")
            # 4
            if long[-2] > middle[-2] > short[-2] and long[-2] > short[-2]:
                if short[-1] > short and middle[-1] > middle[-1]:
                    print(f"{value[-1]} price: Buy")
                    msg = upbit.buy_market_order("KRW-ETH", 8000)
                    if msg == None:
                        print("이미 샀음")
                    else:
                        print(msg)





        # 6
        elif short[-1] > long[-1] > middle[-1] and short[-1] > middle[-1]:# 단 장 중
            # 전 단계가 5단계 이면 구매하자
            if long[-2] > short[-2] > middle[-2] and long[-2] > middle[-2]:
                print(f"{value[-1]} 상승 추세의 시작")
                if short[-1] > short and middle[-1] > middle[-1]:
                    print(f"{value[-1]} price: Buy")
                    msg = upbit.buy_market_order("KRW-ETH", 8000)
                    if msg == None:
                        print("이미 샀음")
                    else:
                        print(msg)


def on_connect(ws):
    print("connected!")
    # Request after connection
    subscribe_message = ('[{"ticket": "test" }, {"type": "trade", "codes": ["KRW-ETH" ] }, {"format": "DEFAULT" } ]')
    ws.send(subscribe_message)


def on_error(ws, err):
    print("error: " + err)


def on_close(ws, status_code, msg):
    print(status_code)
    print(msg)
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
