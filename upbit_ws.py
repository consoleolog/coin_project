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

upbit = pyupbit.Upbit(access_key, secret_key)

short = []
middle = []
long = []
value = []
current_price = []
ticker = "BTC"

last_processed_timestamp = None


def on_message(ws, message):
    global value, short, middle, long, last_processed_timestamp

    data = json.loads(message)

    current_timestamp = data.get('trade_time', None)

    if last_processed_timestamp == current_timestamp:
        pass
    else:
        value.append(data['trade_price'])

    last_processed_timestamp = current_timestamp

    print(f"===== count : {len(value)} =====")

    if len(value) >= 20:
        avg_short = sum(value[-20:]) / 20
        short.append(avg_short)

    if len(value) >= 60:
        avg_middle = sum(value[-60:]) / 60
        middle.append(avg_middle)

    if len(value) >= 120:
        avg_long = sum(value[-120:]) / 120
        long.append(avg_long)
    # if len(value) >= 5:
    #     avg_short = sum(value[-5:]) / 5
    #     short.append(avg_short)
    # if len(value) >= 10:
    #     avg_middle = sum(value[-10:]) / 10
    #     middle.append(avg_middle)
    # if len(value) >= 15:
    #     avg_long = sum(value[-15:]) / 15
    #     long.append(avg_long)
    if len(value) > 120:

        if len(current_price) > 0:
            if value[-1]*0.99 > current_price[-1]:
                print(f"===== SELL : {value[-1]} =====")
                now = get_balance(upbit, ticker)
                try:
                    sell_result = sell(upbit, f"KRW-{ticker}", now)
                    print(sell_result)
                except Exception as e:
                    print(f"===== ERROR : {e} =====")
                    pass
        print(f"===== 단기선 - 중기선 : {abs(short[-1] - middle[-1])} =====")
        print(f"===== 단기선 - 장기선 : {abs(short[-1] - long[-1])} =====")
        print(f"===== 중기선 - 장기선 : {abs(middle[-1] - long[-1])} =====")

        # ===================================================================
        # 1 스테이지

        if short[-1] >= middle[-1] >= long[-1] and short[-1] >= long[-1]:  # 단 중 장
            print(f"===== stage 1 : {value[-1]} 안정 하게 상승중 =====")

            short1 = inclination(short, 20, 1)

            middle1 = inclination(middle, 60, 1)

            long1 = inclination(long, 120, 1)

            # 단기선이랑 중기선이랑 만났을 때
            if short[-1] == middle[-1] or 100 > abs(short[-1] - middle[-1]) > 0:
                print("===== 단기선 중기선 교차 =====")

                if short1 > middle1:
                    print("===== still stage 1 =====")
                elif short1 < middle1:
                    print("===== move to stage 2 =====")
                    print(f"===== SELL : {value[-1]} =====")
                    now = get_balance(upbit, ticker)
                    try:
                        sell_result = sell(upbit, f"KRW-{ticker}", now)
                        print(sell_result)
                    except Exception as e:
                        print(f"===== ERROR : {e} =====")
                        pass

                # --
                elif short1 < 0 and middle1 < 0:
                    if abs(short1) > abs(middle1):
                        print("===== move to stage 2 =====")
                        print(f"===== SELL : {value[-1]} =====")
                        now = get_balance(upbit, ticker)
                        try:
                            sell_result = sell(upbit, f"KRW-{ticker}", now)
                            print(sell_result)
                        except Exception as e:
                            print(f"===== ERROR : {e} =====")
                            pass
                    elif abs(short1) < abs(middle1):
                        print("===== still stage 1 =====")

            elif middle[-1] == long[-1] or 1 > abs(middle[-1] - long[-1]) > 0:
                print("===== 중기선 장기선 교차 =====")
                if middle1 > long1:
                    print("===== still stage 1 =====")
                elif middle1 < long1:
                    print("===== move to stage 6 =====")
                    print(f"===== SELL : {value[-1]} =====")
                    now = get_balance(upbit, ticker)
                    try:
                        sell_result = sell(upbit, f"KRW-{ticker}", now)
                        print(sell_result)
                    except Exception as e:
                        print(f"===== ERROR : {e} =====")
                        pass
                elif middle1 < 0 and long1 < 0:
                    if abs(middle1) > abs(long1):
                        print("===== move to stage 6 =====")
                        print(f"===== SELL : {value[-1]} =====")
                        now = get_balance(upbit, ticker)
                        try:
                            sell_result = sell(upbit, f"KRW-{ticker}", now)
                            print(sell_result)
                        except Exception as e:
                            print(f"===== ERROR : {e} =====")
                            pass
                    elif abs(middle1) < abs(long1):
                        print("===== still stage 1 =====")


        # ===================================================================

        # ===================================================================
        # 2
        elif middle[-1] >= short[-1] >= long[-1] and middle[-1] >= long[-1]:  # 중 단 장
            print(f"===== stage2 : {value[-1]} 상승 추세의 끝 =====")

            short1 = inclination(short, 20, 1)

            middle1 = inclination(middle, 60, 1)

            long1 = inclination(long, 120, 1)

            if middle[-1] == short[-1] or 100 > abs(middle[-1] - short[-1]) > 0:
                print("===== 단기랑 중기랑 교차함 =====")
                if middle1 > short1:
                    print("====== still stage 2 =====")
                elif middle1 < short1:
                    print("===== move to stage 1 =====")
                    print(f'===== BUY : {value[-1]} ======')
                    current_price.append(value[-1])
                    now = get_balance(upbit, ticker)
                    buy_result = buy(upbit, f"KRW-{ticker}", now, 6000)
                    if buy_result == 'error_buy':
                        return
                    else:
                        print(buy_result)


                elif middle1 < 0 and short1 < 0:
                    if abs(middle1) > abs(short1):
                        print("===== move to stage 1 =====")
                        print(f'===== BUY : {value[-1]} ======')
                        current_price.append(value[-1])
                        now = get_balance(upbit, ticker)
                        buy_result = buy(upbit, f"KRW-{ticker}", now, 6000)
                        if buy_result == 'error_buy':
                            return
                        else:
                            print(buy_result)
                    elif abs(middle1) < abs(short1):
                        print("===== still stage 2 =====")

            elif short[-1] == long[-1] or 100 > abs(short[-1] - long[-1]) > 0:
                print("===== 단기랑 장기랑 교차 =====")
                if short1 > long1:
                    print("===== still stage 2 =====")
                elif short1 < long1:
                    print("===== move to stage 3 =====")
                    print(f"===== SELL : {value[-1]} =====")
                    now = get_balance(upbit, ticker)
                    try:
                        sell_result = sell(upbit, f"KRW-{ticker}", now)
                        print(sell_result)
                    except Exception as e:
                        print(f"===== ERROR : {e} =====")
                        pass
                elif short1 < 0 and long1 < 0:
                    if abs(short1) > abs(long1):
                        print("===== move to stage 3 =====")
                        print(f"===== SELL : {value[-1]} =====")
                        now = get_balance(upbit, ticker)
                        try:
                            sell_result = sell(upbit, f"KRW-{ticker}", now)
                            print(sell_result)
                        except Exception as e:
                            print(f"===== ERROR : {e} =====")
                            pass
                    elif abs(short1) < abs(long1):
                        print("===== still stage 2 =====")



        # ===================================================================

        # ===================================================================
        # 3
        elif middle[-1] >= long[-1] >= short[-1] and middle[-1] >= short[-1]:  # 중 장 단
            print(f"===== stage3 : {value[-1]} 하락 추세의 시작 ======")
            short1 = inclination(short, 20, 1)

            middle1 = inclination(middle, 60, 1)

            long1 = inclination(long, 120, 1)

            if middle[-1] == long[-1] or 100 > abs(middle[-1] - long[-1]) > 0:
                print("===== 중기랑 장기랑 교차 =====")
                if middle1 > long1:
                    print("===== still stage 3 =====")
                elif middle1 < long1:
                    print("===== move to stage 4 =====")
                    print(f"===== SELL : {value[-1]} =====")
                    now = get_balance(upbit, ticker)
                    try:
                        sell_result = sell(upbit, f"KRW-{ticker}", now)
                        print(sell_result)
                    except Exception as e:
                        print(f"===== ERROR : {e} =====")
                        pass
                elif middle1 < 0 and long1 < 0:
                    if abs(middle1) > abs(long1):
                        print("===== move to stage 4 =====")
                        print(f"===== SELL : {value[-1]} =====")
                        now = get_balance(upbit, ticker)
                        try:
                            sell_result = sell(upbit, f"KRW-{ticker}", now)
                            print(sell_result)
                        except Exception as e:
                            print(f"===== ERROR : {e} =====")
                            pass
                    elif abs(middle1) < abs(long1):
                        print("===== still stage 3 =====")


            elif long[-1] == short[-1] or 100 > abs(long[-1] - short[-1]) > 0:
                print("===== 단기랑 장기랑 교차 =====")
                if long1 > short1:
                    print("===== still stage 3 =====")
                elif long1 < short1:
                    print("===== move to stage 2 =====")
                    print(f"===== SELL : {value[-1]} =====")
                    now = get_balance(upbit, ticker)
                    try:
                        sell_result = sell(upbit, f"KRW-{ticker}", now)
                        print(sell_result)
                    except Exception as e:
                        print(f"===== ERROR : {e} =====")
                        pass
                elif long1 < 0 and short1 < 0:
                    if abs(long1) > abs(short1):
                        print("===== move to stage 2 =====")
                        print(f"===== SELL : {value[-1]} =====")
                        now = get_balance(upbit, ticker)
                        try:
                            sell_result = sell(upbit, f"KRW-{ticker}", now)
                            print(sell_result)
                        except Exception as e:
                            print(f"===== ERROR : {e} =====")
                            pass
                    elif abs(long1) < abs(short1):
                        print("===== still stage 3 =====")


        # ===================================================================

        # ===================================================================
        # 4
        elif long[-1] >= middle[-1] >= short[-1] and long[-1] >= short[-1]:  # 장 중 단
            print(f"===== stage4 : {value[-1]} 안정 하락 =====")
            short1 = inclination(short, 20, 1)

            middle1 = inclination(middle, 60, 1)

            long1 = inclination(long, 120, 1)

            if long[-1] == middle[-1] or 100 > abs(long[-1] - middle[-1]) > 0:
                print("===== 장기랑 중기랑 교차 =====")
                if long1 > middle1:
                    print("===== still stage 4 =====")
                elif long1 < middle1:
                    print("===== move to stage 3 =====")
                    print(f"===== SELL : {value[-1]} =====")
                    now = get_balance(upbit, ticker)
                    try:
                        sell_result = sell(upbit, f"KRW-{ticker}", now)
                        print(sell_result)
                    except Exception as e:
                        print(f"===== ERROR : {e} =====")
                        pass
                elif long1 < 0 and middle1 < 0:
                    if abs(long1) > abs(middle1):
                        print("===== move to stage 3 =====")
                        print(f"===== SELL : {value[-1]} =====")
                        now = get_balance(upbit, ticker)
                        try:
                            sell_result = sell(upbit, f"KRW-{ticker}", now)
                            print(sell_result)
                        except Exception as e:
                            print(f"===== ERROR : {e} =====")
                            pass
                    elif abs(long1) < abs(middle1):
                        print("===== still stage 4 =====")

            elif middle[-1] == short[-1] or 100 > abs(middle[-1] - short[-1]) > 0:
                print("===== 중기랑 단기랑 교차 =====")
                if middle1 > short1:
                    print("===== still stage 4 =====")
                elif middle1 < short1:
                    print("===== move to stage 5 =====")
                    print(f"===== SELL : {value[-1]} =====")
                    now = get_balance(upbit, ticker)
                    try:
                        sell_result = sell(upbit, f"KRW-{ticker}", now)
                        print(sell_result)
                    except Exception as e:
                        print(f"===== ERROR : {e} =====")
                        pass
                elif middle1 < 0 and short1 < 0:
                    if abs(middle1) > abs(short1):
                        print("===== move to stage 5 =====")
                        print(f"===== SELL : {value[-1]} =====")
                        now = get_balance(upbit, ticker)
                        try:
                            sell_result = sell(upbit, f"KRW-{ticker}", now)
                            print(sell_result)
                        except Exception as e:
                            print(f"===== ERROR : {e} =====")
                            pass
                    elif abs(middle1) < abs(short1):
                        print("===== still stage 4 =====")

        # ===================================================================

        # ===================================================================
        # 5
        elif long[-1] >= short[-1] >= middle[-1] and long[-1] >= middle[-1]:  # 장 단 중
            print(f"===== stage5 : {value[-1]} 하락 추세의 끝 =====")
            short1 = inclination(short, 20, 1)

            middle1 = inclination(middle, 60, 1)

            long1 = inclination(long, 120, 1)

            if long[-1] == short[-1] or 100 > abs(long[-1] - short[-1]) > 0:
                print("===== 장기 단기 교차 =====")
                if long1 > short1:
                    print("===== still stage 5 =====")
                elif long1 < short1:
                    print("===== move to stage 6 ======")
                    print(f'===== BUY : {value[-1]} ======')
                    current_price.append(value[-1])
                    now = get_balance(upbit, ticker)
                    buy_result = buy(upbit, f"KRW-{ticker}", now, 6000)
                    if buy_result == 'error_buy':
                        return
                    else:
                        print(buy_result)
                elif long1 < 0 and short1 < 0:
                    if abs(long1) > abs(short1):
                        print("===== move to stage 6 =====")
                        print(f'===== BUY : {value[-1]} ======')
                        current_price.append(value[-1])
                        now = get_balance(upbit, ticker)
                        buy_result = buy(upbit, f"KRW-{ticker}", now, 6000)
                        if buy_result == 'error_buy':
                            return
                        else:
                            print(buy_result)
                    elif abs(long1) < abs(short1):
                        print("===== still stage 5 =====")




            elif short[-1] == middle[-1] or 100 > abs(short[-1] - middle[-1]) > 0:
                print("===== 단기 중기 교차 =====")
                if short1 > middle1:
                    print("===== still stage 5 =====")
                elif short1 < middle1:
                    print("===== move to stage 4 =====")
                    print(f"===== SELL : {value[-1]} =====")
                    now = get_balance(upbit, ticker)
                    try:
                        sell_result = sell(upbit, f"KRW-{ticker}", now)
                        print(sell_result)
                    except Exception as e:
                        print(f"===== ERROR : {e} =====")
                        pass
                elif short1 < 0 and middle1 < 0:
                    if abs(short1) > abs(middle1):
                        print("===== move to stage 4 =====")
                        print(f"===== SELL : {value[-1]} =====")
                        now = get_balance(upbit, ticker)
                        try:
                            sell_result = sell(upbit, f"KRW-{ticker}", now)
                            print(sell_result)
                        except Exception as e:
                            print(f"===== ERROR : {e} =====")
                            pass
                    elif abs(short1) < abs(middle1):
                        print("===== still stage 5 =====")

        # ===================================================================

        # ===================================================================
        # 6
        elif short[-1] >= long[-1] >= middle[-1] and short[-1] >= middle[-1]:  # 단 장 중
            print(f"===== stage6 : {value[-1]} 상승 추세의 시작 =====")
            short1 = inclination(short, 20, 1)

            middle1 = inclination(middle, 60, 1)

            long1 = inclination(long, 120, 1)

            if short[-1] == long[-1] or 100 > abs(short[-1] - long[-1]) > 0:
                print("===== 단기 장기 교차 =====")
                if short1 > long1:
                    print("===== still stage 6 =====")
                elif short1 < long1:
                    print("===== move to stage 5 =====")
                    print(f"===== SELL : {value[-1]} =====")
                    now = get_balance(upbit, ticker)
                    try:
                        sell_result = sell(upbit, f"KRW-{ticker}", now)
                        print(sell_result)
                    except Exception as e:
                        print(f"===== ERROR : {e} =====")
                        pass
                elif short1 < 0 and long1 < 0:
                    if abs(short1) > abs(long1):
                        print("===== move to stage 5 =====")
                        print(f"===== SELL : {value[-1]} =====")
                        now = get_balance(upbit, ticker)
                        try:
                            sell_result = sell(upbit, f"KRW-{ticker}", now)
                            print(sell_result)
                        except Exception as e:
                            print(f"===== ERROR : {e} =====")
                            pass
                    elif abs(short1) < abs(long1):
                        print("===== still stage 6 =====")


            elif long[-1] == middle[-1] or 100 > abs(long[-1] - middle[-1]) > 0:
                print("===== 장기 중기 교차 =====")
                if long1 > middle1:
                    print("===== still stage 6 =====")
                elif long1 < middle1:
                    print("===== move to stage 1 =====")
                    print(f'===== BUY : {value[-1]} ======')
                    current_price.append(value[-1])
                    now = get_balance(upbit, ticker)
                    buy_result = buy(upbit, f"KRW-{ticker}", now, 6000)
                    if buy_result == 'error_buy':
                        return
                    else:
                        print(buy_result)
                elif long1 < 0 and middle1 < 0:
                    if abs(long1) > abs(middle1):
                        print("===== move to stage 1 =====")
                        print(f'===== BUY : {value[-1]} ======')
                        current_price.append(value[-1])
                        now = get_balance(upbit, ticker)
                        buy_result = buy(upbit, f"KRW-{ticker}", now, 6000)
                        if buy_result == 'error_buy':
                            return
                        else:
                            print(buy_result)
                    elif abs(long1) < abs(middle1):
                        print("===== still stage 6 =====")
        # ===================================================================


def on_connect(ws):
    print("connected!")
    subscribe_message = [
        {"ticket": "test-websocket"},
        {
            "type": "ticker",
            "codes": [f"KRW-{ticker}"],
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
