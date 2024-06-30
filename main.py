import pandas as pd
from pandas_datareader import data
import yfinance as yfin
import matplotlib.pyplot as plt
import pyupbit as upbit


yfin.pdr_override()

smp500 = data.get_data_yahoo('^GSPC',start='2024-01-01',end='2024-06-28')

apple = data.get_data_yahoo('AAPL',start='2024-01-01',end='2024-06-28')

smp500['rolling_5'] = smp500['Close'].rolling(5).mean()

smp500['rolling_20'] = smp500['Close'].rolling(20).mean()

apple['rolling_5'] = apple['Close'].rolling(5).mean()

apple['rolling_20'] = apple['Close'].rolling(20).mean()

plt.plot(smp500.index,smp500['Close'],color='crimson')
plt.xlabel('time')
plt.ylabel('price')
plt.legend(['smp500'])
plt.plot(apple.index,apple['Close'],color='skyblue')
plt.savefig('smp500.png')
plt.show()


def get_company_data(company_name,start,end):
    return data.get_data_yahoo(company_name,start=start,end=end)



def income(date,company_name):
    before_data = get_company_data(company_name,date-1,date)
    after_data = get_company_data(company_name,date,date+1)

    before_price = before_data['Close']
    after_price = after_data['Close']

    return (after_price - before_price)/before_price






# if __name__ == '__main__':


