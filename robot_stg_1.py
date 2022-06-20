from functions import *
from prepare_data import *
from ib_insync import *
from datetime import *
import pandas as pd

def buy_stg_1(cash,df):

    cash = cash/10


   # # Find the s&p stock list
   # s_p_500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
   # symbol_list = s_p_500[0]['Symbol']
   # symbol_list = symbol_list.append(pd.Series('SPY'), ignore_index=True)
   # print(symbol_list)
   # symbol_list=symbol_list.drop([442])
   # # Import from yahoo finance and download
#
   # df = pd.DataFrame()
   # d = 180
   # end = datetime.now()
   # start = end - timedelta(days=d)
   # cnt = 0
   # for s in symbol_list:
   #     try:
   #         d = yf.download(s, start=start, end=end)
   #         print(cnt)
   #         print(s)
   #         cnt = cnt + 1
   #         d['Name'] = s
   #         df = df.append(d)
   #     except:
   #         pass
   # df.reset_index(level=0, inplace=True)
#
   # df['dt'] = pd.to_datetime(df['Date'])
   # df = df[df['Name'] != 'MOS']

    ib = IB()
    ib.connect([IP], [PORT], clientId=[])
    amount=10
    stock_returns = df.groupby('Name').apply(calculate_returns).sort_values(ascending=False)
    stock_returns_table = stock_returns.reset_index()
    stock_returns_table.columns = ['Name', 'Returns']
    Profitable_stock = stock_returns_table['Name'][:amount]

    for s in Profitable_stock:

        ticker_yahoo = yf.Ticker(s)
        data = ticker_yahoo.history()
        last_quote = (data.tail(1)['Close'].iloc[0])
        shares = cash/last_quote

        contract = Stock(str(s), exchange='NYSE')
        order = MarketOrder('BUY', round(shares))
        ib.placeOrder(contract, order)
        ib.sleep(1)




