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

    print(len(value))

    if len(value) >= 20:
        avg_short = sum(value[-20:]) / 20
        short.append(avg_short)

    if len(value) >= 60:
        avg_middle = sum(value[-60:]) / 60
        middle.append(avg_middle)

    if len(value) >= 120:
        avg_long = sum(value[-120:]) / 120
        long.append(avg_long)

        #매수 신호
        # 1. 이동 평균선이 어느정도의 시간 동안 하락한 뒤 횡보하거나 약간 상승 기조로 전환된 시기에
        # 가격이 그 이동 평균선을 아래서 위로 뚜렷하게 교차했을때
        # 2. 이동 평균선이 지속적으로 상승하는 시기에 가격이 이동 평균선을 왼쪽에서 오른쪽으로
        # 교차했을 때
        # 3. 가격이 상승 기조의 이동 평균선 보다 위에 있고, 그 후 이동 평균선을 향해 접근하지만
        # 이동 평균선과 교차하지 않고 다시 상승하기 시작할때
        # 4. 가격이 하락기조의 이동 평균선보다 아래에 있고, 이동 평균선으로부터 그게 괴리되었을때

        #매도 신호
        # 1. 이동 평균선이 어느정도의 기간 동안 상승한 뒤 횡보하거나 약간 하락 기조로 전환된
        # 시기에 가격이 그 이동 평균선을 위에서 아래로 뚜렷하게 교차했을 때
        # 2. 이동 평균선이 지속적으로 하락하는 시기에 가격이 이동 평균선을 왼쪽에서 오른쪽으로
        # 교차했을때
        # 3. 가격이 하락 기조의 이동 평균선보다 아래에 있고, 그 후 이동 평균선을 향해 접근 하지만
        # 이동 평균선과 교차하지 않고 다시 하락하기 시작했을 때,
        # 4. 가격이 상승 기조의 이동 평균선 보다 위에 있고, 이동 평균선으로 부터 크게
        # 괴리되어 있을 때

        # ===================================================================
        # 전역 매수 시점
        # if short[-1] > long[-1]:
        #     print(f'===== BUY : {value[-1]} ======')
        #     current_price.append(value[-1])
        #     now = get_balance(upbit, 'BTC')
        #     buy_result = buy(upbit, "KRW-BTC", now, 6000)
        #     if buy_result == 'error_buy':
        #         return
        #     else:
        #         print(buy_result)
        # # ===================================================================
        #
        # #
        # elif short[-1] == middle[-1]:
        #     print("===== 단기랑 중기랑 교차함 =====")
        #     a = inclination(short, 20, 2)
        #     b = inclination(short, 20, 3)
        #     c = inclination(short, 20, 1)
        #
        #     if a > b > c > 0 and a > c:
        #         # 매수 시점
        #         print(f'===== BUY : {value[-1]} ======')
        #         current_price.append(value[-1])
        #         now = get_balance(upbit, 'BTC')
        #         buy_result = buy(upbit, "KRW-BTC", now, 6000)
        #         if buy_result == 'error_buy':
        #             return
        #         else:
        #             print(buy_result)
        #
        # elif short[-1] == middle[-1]:
        #     print("===== 단기랑 중기랑 교차함 =====")
        #     a = inclination(short, 20, 2)
        #     b = inclination(short, 20, 3)
        #     c = inclination(short, 20, 1)
        #
        #     if a < b < c < 0 and a < c:
        #         # 매수 시점
        #         print(f'===== BUY : {value[-1]} ======')
        #         current_price.append(value[-1])
        #         now = get_balance(upbit, 'BTC')
        #         buy_result = buy(upbit, "KRW-BTC", now, 6000)
        #         if buy_result == 'error_buy':
        #             return
        #         else:
        #             print(buy_result)

        # ===================================================================
        # 전역 매도 시점 (비상 매도)
        # if short[-1] == long[-1]:
        #     if short[-2] < long[-2]:
        #         print(f"===== SELL : {value[-1]} =====")
        #         now = get_balance(upbit, 'BTC')
        #         try:
        #             sell_result = sell(upbit, "KRW-BTC", now)
        #             print(sell_result)
        #         except Exception as e:
        #             print(f"===== ERROR : {e} =====")
        #             return
        # ===================================================================

        # ===================================================================

        # 1 스테이지

        if short[-1] >= middle[-1] >= long[-1] and short[-1] >= long[-1]:  # 단 중 장
            print(f"===== stage 1 : {value[-1]} 안정 하게 상승중 =====")

            short1 = inclination(short, 20, 1)

            middle1 = inclination(middle, 60, 1)

            long1 = inclination(long, 120, 1)


            # 단기선이랑 중기선이랑 만났을 때
            if short[-1] == middle[-1]:
                print("===== 단기선 중기선 교차 =====")
                if short1 < middle1:
                    print("===== move to stage 2 .... =====")

                elif short1 > middle1:
                    print("===== still stage 1 ..... =====")



            elif middle[-1] == long[-1]:
                print("===== 중기선 장기선 교차 =====")

                if middle1 > long1:
                    print("===== still stage 1 .... =====")

                elif middle1 < long1:
                    print("===== move to stage 6.... =====")




        # ===================================================================

        # ===================================================================
        # 2
        elif middle[-1] >= short[-1] >= long[-1] and middle[-1] >= long[-1]:  # 중 단 장
            print(f"===== stage2 : {value[-1]} 상승 추세의 끝 =====")

            short1 = inclination(short, 20, 1)

            middle1 = inclination(middle, 60, 1)

            long1 = inclination(long, 120, 1)

            if short[-1] == middle[-1]:
                print("===== 단기랑 중기랑 교차함 =====")

                if short1 > middle1:
                    print("===== move to stage 1... =====")

                elif short1 < middle1:
                    print("===== still stage 2.... =====")

            if short[-1] == long[-1]:
                print("===== 단기랑 장기랑 교차 =====")
                if short1 > long1:
                    print("===== still stage 2... =====")
                elif short1 < long1:
                    print("===== move to stage 3 =====")
                    # 매도 신호


        # ===================================================================

        # ===================================================================
        # 3
        elif middle[-1] >= long[-1] >= short[-1] and middle[-1] >= short[-1]:  # 중 장 단
            print(f"===== stage3 : {value[-1]} 하락 추세의 시작 ======")
            short1 = inclination(short, 20, 1)

            middle1 = inclination(middle, 60, 1)

            long1 = inclination(long, 120, 1)

            if middle[-1] == long[-1]:
                print("===== 중기랑 장기랑 교차 =====")
                if middle1 < long1:
                    print("===== move to stage 4 =====")
                elif middle1 > long1:
                    print("===== still stage 3... =====")

            elif long[-1] == short[-1]:
                print("===== 단기랑 장기랑 교차 =====")
                if long1 > short1:
                    print("===== still stage 3... =====")
                elif long1 < short1:
                    print("===== move to stage 2... =====")



        # 4
        elif long[-1] >= middle[-1] >= short[-1] and long[-1] >= short[-1]:  # 장 중 단
            print(f"===== stage4 : {value[-1]} 안정 하락 =====")
            short1 = inclination(short, 20, 1)

            middle1 = inclination(middle, 60, 1)

            long1 = inclination(long, 120, 1)

            if long[-1] == middle[-1]:
                print("===== 장기랑 중기랑 교차 =====")
                if long1 > middle1:
                    print("===== still stage 4 =====")
                elif long1 < middle1:
                    print("===== move to stage 3 =====")

            elif middle[-1] == short[-1]:
                print("===== 중기랑 단기랑 교차 =====")
                if middle1 > short1:
                    print("===== still stage 4 =====")
                elif middle1 < short1:
                    print("===== mobe to stage 5 =====")







        # 5
        elif long[-1] >= short[-1] >= middle[-1] and long[-1] >= middle[-1]:  # 장 단 중
            print(f"===== stage5 : {value[-1]} 하락 추세의 끝 =====")
            short1 = inclination(short, 20, 1)

            middle1 = inclination(middle, 60, 1)

            long1 = inclination(long, 120, 1)

            if long[-1] == short[-1]:
                print("===== 장기 단기 교차 =====")
                if long1 > short1:
                    print("===== still stage 5... =====")
                elif long1 < short1:
                    print("===== move to stage 6 =====")
                    # 매도 신호 확인


            elif short[-1] == middle[-1]:
                print("===== 단기 중기 교차 =====")
                if short1 > middle1:
                    print("===== still stage 5.... =====")
                elif short1 < middle1:
                    print("===== move to stage 4.... =====")






        # 6
        elif short[-1] >= long[-1] >= middle[-1] and short[-1] >= middle[-1]:  # 단 장 중
            print(f"===== stage6 : {value[-1]} 상승 추세의 시작 =====")
            short1 = inclination(short, 20, 1)

            middle1 = inclination(middle, 60, 1)

            long1 = inclination(long, 120, 1)

            if short[-1] == long[-1]:
                print("===== 단기 장기 교차 =====")
                if short1 > long1:
                    print("===== still stage 6... =====")
                elif short1 < long1:
                    print("===== move to stage 5... =====")

            elif long[-1] == middle[-1]:
                print("===== 장기 중기 교차 =====")
                if long1 > middle1:
                    print("===== still stage 6.. =====")
                elif long1 < middle1:
                    print("===== move to stage 1 =====")



def on_connect(ws):
    print("connected!")
    subscribe_message = [
        {"ticket": "test-websocket"},
        {
            "type": "ticker",
            "codes": ["KRW-ETH"],
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
