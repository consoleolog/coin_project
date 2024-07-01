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


def on_message(ws, message):
    global value, short, middle, long

    data = json.loads(message)
    value.append(data['trade_price'])

    if len(value) >= 15:
        avg_short = sum(value[-15:]) / 15
        short.append(avg_short)

    if len(value) >= 40:
        avg_middle = sum(value[-40:]) / 40
        middle.append(avg_middle)

    if len(value) >= 140:
        avg_long = sum(value[-140:]) / 140
        long.append(avg_long)

    if len(value) >= 140:




        if short[-1] > middle[-1] > long[-1] and short[-1] > long[-1]:  # 단 중 장
            print(f"{value[-1]} 안정 하게 상승중")
            if middle[-2] > long[-2] > short[-2] and middle[-2] > short[-2]:  # 중 장 단
                if short[-1] > short[-2] and long[-1] > long[-2] and middle[-1] > middle[-2]:
                    print("그래프 세개 다 우 상향 ")
                    try:
                        ETH_now = get_balance('ETH')
                        if ETH_now == 0:
                            print(f"{value[-1]} price: Buy")
                            msg = upbit.buy_market_order("KRW-ETH", 8000)
                            if msg == None:
                                print("이미 샀음")
                            else:
                                print(msg)
                        elif ETH_now < 10:
                            print(f"{value[-1]} price: Buy")
                            msg = upbit.buy_market_order("KRW-ETH", 8000)
                            if msg == None:
                                print("이미 샀음")
                            else:
                                print(msg)
                        pass
                    except:
                        pass
            elif long[-2] > middle[-2] > short[-2] and long[-2] > short[-2]:  # 장 중 단
                if middle[-2] > long[-2] > short[-2] and middle[-2] > short[-2]:  # 중 장 단
                    if short[-1] > short[-2] and long[-1] > long[-2] and middle[-1] > middle[-2]:
                        print("그래프 세개 다 우 상향 ")
                        try:
                            ETH_now = get_balance('ETH')
                            if ETH_now == 0:
                                print(f"{value[-1]} price: Buy")
                                msg = upbit.buy_market_order("KRW-ETH", 8000)
                                if msg == None:
                                    print("이미 샀음")
                                else:
                                    print(msg)
                            elif ETH_now < 10:
                                print(f"{value[-1]} price: Buy")
                                msg = upbit.buy_market_order("KRW-ETH", 8000)
                                if msg == None:
                                    print("이미 샀음")
                                else:
                                    print(msg)
                            pass
                        except:
                            pass






        elif middle[-1] > short[-1] > long[-1] and middle[-1] > long[-1]:  # 중 단 장
            print(f"{value[-1]} 상승 추세의 끝")
            if short[-1] < short[-2] and long[-1] < long[-2] and middle[-1] < middle[-2]:
                print("그래프 세개 다 우 하향 ")
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




        elif middle[-1] > long[-1] > short[-1] and middle[-1] > short[-1]:  # 중 장 단
            print(f"{value[-1]} 하락 추세의 시작")
            if short[-1] > short[-2] and long[-1] > long[-2] and middle[-1] > middle[-2]:
                print("그래프 세개 다 우 상향 ")
            else:
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





        elif long[-1] > middle[-1] > short[-1] and long[-1] > short[-1]:  # 장 중 단
            print(f"{value[-1]} 안정 하락")
            if short[-1] > short[-2] and long[-1] > long[-2] and middle[-1] > middle[-2]:
                print("그래프 세개 다 우 상향 ")
            else:
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






        elif long[-1] > short[-1] > middle[-1] and long[-1] > middle[-1]:  # 장 단 중
            print(f"{value[-1]} 하락 추세의 끝")
            if short[-1] > short[-2] and long[-1] > long[-2] and middle[-1] > middle[-2]:
                print("그래프 세개 다 우 상향 ")
                try:
                    ETH_now = get_balance('ETH')
                    if ETH_now == 0:
                        print(f"{value[-1]} price: Buy")
                        msg = upbit.buy_market_order("KRW-ETH", 8000)
                        if msg == None:
                            print("이미 샀음")
                        else:
                            print(msg)
                    elif ETH_now < 10:
                        print(f"{value[-1]} price: Buy")
                        msg = upbit.buy_market_order("KRW-ETH", 8000)
                        if msg == None:
                            print("이미 샀음")
                        else:
                            print(msg)
                    pass
                except:
                    pass
            # elif short[-1] < short[-2] and long[-1] < long[-2] and middle[-1] < middle[-2]:
            #     print("그래프 세개 다 우 하향 ")
            #     try:
            #         ETH_now = get_balance('ETH')
            #         print(f"{value[-1]} price: Sell")
            #         msg = upbit.sell_market_order('KRW-ETH', ETH_now)
            #         for m in msg:
            #             if m == 'error':
            #                 print("이미 팔았음")
            #             else:
            #                 print(msg)
            #         pass
            #     except:
            #         pass






        elif short[-1] > long[-1] > middle[-1] and short[-1] > middle[-1]:  # 단 장 중
            print(f"{value[-1]} 상승 추세의 시작")
            if short[-1] > short[-2] and long[-1] > long[-2] and middle[-1] > middle[-2]:
                print("그래프 세개 다 우 상향 ")
                try:
                    ETH_now = get_balance('ETH')
                    if ETH_now == 0:
                        print(f"{value[-1]} price: Buy")
                        msg = upbit.buy_market_order("KRW-ETH", 8000)
                        if msg == None:
                            print("이미 샀음")
                        else:
                            print(msg)
                    elif ETH_now < 10:
                        print(f"{value[-1]} price: Buy")
                        msg = upbit.buy_market_order("KRW-ETH", 8000)
                        if msg == None:
                            print("이미 샀음")
                        else:
                            print(msg)
                    pass
                except:
                    pass
            # elif short[-1] < short[-2] and long[-1] < long[-2] and middle[-1] < middle[-2]:
            #     print("그래프 세개 다 우 하향 ")
            #     try:
            #         ETH_now = get_balance('ETH')
            #         print(f"{value[-1]} price: Sell")
            #         msg = upbit.sell_market_order('KRW-ETH', ETH_now)
            #         for m in msg:
            #             if m == 'error':
            #                 print("이미 팔았음")
            #             else:
            #                 print(msg)
            #         pass
            #     except:
            #         pass





        else:
            pass


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
