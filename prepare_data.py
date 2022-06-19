import yfinance as yf
import pandas as pd
from datetime import datetime
import talib

def create_df_from_yahoo_russel():
    # Find the s&p stock list
    russell = pd.read_csv('csv/russell.csv')
    symbol_list = russell['Ticker']
    symbol_list = symbol_list.append(pd.Series('SPY'), ignore_index=True)
    print(symbol_list)

    # Import from yahoo finance and download

    df = pd.DataFrame()
    start = datetime(2009, 1, 1)
    end = datetime(2020, 12, 31)
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
            d['TEMA10']=talib.TEMA(d['Close'], 10)
            df = df.append(d)
        except:
            pass
    df.reset_index(level=0, inplace=True)
    return df

def create_df_from_yahoo():
    # Find the s&p stock list
    s_p_500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    symbol_list = s_p_500[0]['Symbol']
    symbol_list = symbol_list.append(pd.Series('SPY'), ignore_index=True)
    print(symbol_list)

    # Import from yahoo finance and download

    df = pd.DataFrame()
    start = datetime(2009, 1, 1)
    end = datetime(2020, 12, 31)
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
            d['TEMA10']=talib.TEMA(d['Close'], 10)
            df = df.append(d)
        except:
            pass
    df.reset_index(level=0, inplace=True)
    return df


def prepare_df(df):
    # df-הוספת עמודות ל
    df['dt'] = pd.to_datetime(df['Date'])
    df['year'] = df['dt'].dt.year
    df['month'] = df['dt'].dt.month
    df['year_month'] = df['month'].astype(str) + '_' + df['year'].astype(str)
    df = df[df['ADX'].notna()]
    return df
