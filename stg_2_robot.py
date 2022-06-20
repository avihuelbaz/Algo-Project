from functions import *
from prepare_data import *
from ib_insync import *
from datetime import *
import pandas as pd

def buy_stg_2(cash):
    cash = cash/10


    # Find the s&p stock list
    s_p_500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    symbol_list = s_p_500[0]['Symbol']
    symbol_list = symbol_list.append(pd.Series('SPY'), ignore_index=True)
    symbol_list=symbol_list.drop([442])
    print(symbol_list)

    # Import from yahoo finance and download

    df = pd.DataFrame()
    d = 180
    end = datetime.now()
    start = end - timedelta(days=d)
    cnt = 0
    for s in symbol_list:
        try:
            d = yf.download(s, start=start, end=end)
            print(cnt)
            print(s)
            cnt = cnt + 1
            d['Name'] = s
            d['ADX'] = talib.ADX(d['High'].values, d['Low'].values, d['Close'].values, timeperiod=20)
            d['RSI'] = talib.RSI(d['Close'], 20)
            df = df.append(d)
        except :
            pass
    df.reset_index(level=0, inplace=True)

    df['dt'] = pd.to_datetime(df['Date'])
    df = df[df['Name'] != 'MOS']

    ib = IB()
    ib.connect([IP], [PORT], clientId=[])
    amount = 10
    stock_returns = df.groupby('Name').apply(calculate_returns).sort_values(ascending=False)
    stock_returns_table = stock_returns.reset_index()
    stock_returns_table.columns = ['Name', 'Returns']
    Profitable_stock = stock_returns_table['Name'][:amount]

    end = datetime(end.year, end.month, end.day)
    new_df = df[(df['dt'] == end) & (df['Name'].isin(Profitable_stock))]
    new_df['rsi_adx'] = ((new_df['ADX'] > 10) & (new_df['RSI'] > 50))

    positions = ib.positions()
    all_positions = []
    for p in positions:
        pos_dict = {
                    'conID': p[1].conId,
                    'symbol': p[1].symbol,
                    'exchage': p[1].exchange,
                    'position': p[2],
                    'avgCost': p[3]
                    }
        all_positions.append(pos_dict)

    pos = pd.DataFrame(all_positions)
    pos = pos.rename(columns={"symbol": "Name"})
    mer = pd.merge(new_df, pos, on='Name', how='left')
    mer = mer.fillna(0)
    for index, r in mer.iterrows():
        if (r['position'] > 0) and not ((r['ADX'] > 10) and (r['RSI'] > 50)):
            contract = Stock(r['Name'], exchange='NYSE')
            order = MarketOrder('SELL', r['position'])
            ib.placeOrder(contract, order)
            ib.sleep(1)
    for index, r in mer.iterrows():
        if (r['position'] == 0) and (r['ADX'] > 10) and (r['RSI'] > 50):
            contract = Stock(r['Name'], exchange='NYSE')
            order = MarketOrder('BUY', round(cash/r['Close']))
            ib.placeOrder(contract, order)
            ib.sleep(1)


    # for s in Profitable_stock:
    #
    #     ticker_yahoo = yf.Ticker(s)
    #     data = ticker_yahoo.history()
    #     last_quote = (data.tail(1)['Close'].iloc[0])
    #     shares = cash/last_quote
    #
    #     contract = Stock(str(s), exchange='NYSE')
    #     order = MarketOrder('BUY', round(shares))
    #     ib.placeOrder(contract, order)

    #     ib.sleep(1)



