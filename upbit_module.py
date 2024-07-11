from log_setting import log_info

import logging
def get_balance(upbit, ticker):
    balances = upbit.get_balances()  # Assuming upbit.get_balance() returns a single float
    print(balances)
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


def gradient(value, rolling):
    return (value.iloc[-2].astype(int) - value.iloc[-1].astype(int)) / rolling


def buy(upbit, ticker, amount, price):
    if amount == 0:
        msg = upbit.buy_market_order(ticker, price)
        if msg is None:
            return "already_buy"
    else:
        return "error_buy"
    return msg


def sell(upbit, ticker, amount):
    msg = upbit.sell_market_order(ticker, amount)
    for m in msg:
        if m == 'error':
            return "already_sell"
    return msg


def ma_stage(short, middle, long):
    if short >= middle >= long:  # 단 중 장
        return "stage1"

    if middle >= short >= long:  # 중 단 장
        return "stage2"

    if middle >= long >= short:  # 중 장 단
        return "stage3"

    if long >= middle >= short:  # 장 중 단
        return "stage4"

    if long >= short >= middle:  # 장 단 중
        return "stage5"

    if short >= long >= middle:  # 단 장 중
        return "stage6"


def stage1(value, short, middle, long):  # 단 중 장
    log_info.info(f"===== stage1 : {value.iloc[-1]} 안정하게 상승 중 =====")

    if short.iloc[-1] == middle.iloc[-1]:
        log_info.info(f"============= 단기 중기 교차   =============")

    if middle.iloc[-1] == long.iloc[-1]:
        log_info.info(f"============= 중기 장기 교차   =============")

    if middle.iloc[-1] == long.iloc[-1]:
        log_info.info(f"============= 중기 장기 교차   =============")

    pass


def stage2(value, short, middle, long):  # 중 단 장
    log_info.info(f"===== stage2 : {value.iloc[-1]} 상승 추세의 끝  =====")

    if middle.iloc[-1] == short.iloc[-1]:
        log_info.info(f"============= 중기 단기 교차  =============")

    if short.iloc[-1] == long.iloc[-1]:
        log_info.info(f"============= 단기 장기 교차  =============")

    if middle.iloc[-1] == long.iloc[-1]:
        log_info.info(f"=============  즁기 장기 교차  =============")

    pass


def stage3(value, short, middle, long):  # 중 장 단
    log_info.info(f"===== stage3 : {value.iloc[-1]} 하락 추세의 시작 =====")

    if middle.iloc[-1] == long.iloc[-1]:
        log_info.info(f"============= 중기 장기 교차   =============")

    if long.iloc[-1] == short.iloc[-1]:
        log_info.info(f"=============장기 단기 교차  =============")

    if middle.iloc[-1] == short.iloc[-1]:
        log_info.info(f"============= 중기 단기 교차  =============")

    pass


def stage4(value, short, middle, long):  # 장 중 단
    log_info.info(f"===== stage4 : {value.iloc[-1]} 안정하게 하락 중 =====")

    if long.iloc[-1] == middle.iloc[-1]:
        log_info.info(f"============= 장기 중기 교차   =============")

    if middle.iloc[-1] == short.iloc[-1]:
        log_info.info(f"============= 중기 단기 교차  =============")

    if long.iloc[-1] == short.iloc[-1]:
        log_info.info(f"============= 장기 단기 교차   =============")

    pass


def stage5(value, short, middle, long):  # 장 단 중
    log_info.info(f"===== stage5 : {value.iloc[-1]} 하락 추세의 끝  =====")

    if long.iloc[-1] == short.iloc[-1]:
        log_info.info(f"============= 장기 단기 교차  =============")

    if short.iloc[-1] == middle.iloc[-1]:
        log_info.info(f"============= 단기 중기 교차  =============")

    if long.iloc[-1] == middle.iloc[-1]:
        log_info.info(f"============= 장기 중기 교차  =============")

    pass

#desire-decide-cartel-peru-milk-1545
def stage6(value, short, middle, long):  # 단 장 중
    log_info.info(f"===== stage6 : {value.iloc[-1]} 상승 추세의 시작 =====")

    if short.iloc[-1] == long.iloc[-1]:
        log_info.info(f"============= 단기 장기 교차  =============")

    if long.iloc[-1] == middle.iloc[-1]:
        log_info.info(f"============= 장기 중기 교차   =============")

    if short.iloc[-1] == middle.iloc[-1]:
        log_info.info(f"============= 단기 중기 교차   =============")

    pass
