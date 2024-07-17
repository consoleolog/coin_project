import time
import config
from upbit_module import *
import normal_log
import coloredlogs

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

    email_detail = {
        "subject": "업비트 자동 매매 결과 보고",
            'html': """
            <table>
                <thead>
                    <tr>
                        <th style="width: 18.181818181818183%">일시</th>
                        <th style="width: 18.181818181818183%">종목</th>
                        <th style="width: 9.090909090909092%">매도/매매</th>
                        <th style="width: 27.27272727272727%">가격</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="text-align:center">2023</td>
                        <td>btc</td>
                        <td style="text-align:center">매매</td>
                        <td>1800</td>
                    </tr>
                </tbody>
            </table>
            """
    }

    print(email_detail)
    time.sleep(60)
