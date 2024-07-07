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


def inclination(ma, v,length):
    return (ma[-length] - ma[-(length+1)]) / v


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

def ma_stage(short,middle,long):
    if short[-1] > middle[-1] >= long[-1] and short[-1] >= long[-1]:  # 단 중 장
        return "stage1"

    if middle[-1] >= short[-1] >= long[-1] and middle[-1] >= long[-1]:  # 중 단 장
        return "stage2"

    if middle[-1] >= long[-1] >= short[-1] and middle[-1] >= short[-1]:  # 중 장 단
        return "stage3"

    if long[-1] >= middle[-1] >= short[-1] and long[-1] >= short[-1]:  # 장 중 단
        return "stage4"

    if long[-1] >= short[-1] >= middle[-1] and long[-1] >= middle[-1]:  # 장 단 중
        return "stage5"

    if short[-1] >= long[-1] >= middle[-1] and short[-1] >= middle[-1]:  # 단 장 중
        return "stage6"

def stage1(value, short, middle, long):
    print(f"===== stage1 : 안정하게 상승 중 =====")
    pass

def stage2(value, short, middle, long):
    print(f"===== stage2 : 상승 추세의 끝 =====")
    pass

def stage3(value, short, middle, long):
    print(f"===== stage3 : 하락 추세의 시작 =====")
    pass

def stage4(value, short, middle, long):
    print(f"===== stage4 : 안정하게 하락 중 =====")
    pass

def stage5(value, short, middle, long):
    print(f"===== stage5 : 하락 추세의 끝 =====")
    pass

def stage6(value, short, middle, long):
    print(f"===== stage6 : 상승 추세의 시작 =====")
    pass