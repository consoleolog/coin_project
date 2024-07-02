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
