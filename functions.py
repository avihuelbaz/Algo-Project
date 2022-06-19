import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def optimization_part1(df):
    r = []
    for qtr in range(90, 450, 90):
        for d in range(0, 1760, 30):
            end_train_day = datetime(2010, 3, 1) + timedelta(days=d)
            for delta in range(50, 400, 10):  # כמה ימים אחורה לבדוק
                start_train_day = end_train_day - timedelta(days=delta)
                train = df[(df['dt'] > start_train_day) & (df['dt'] < end_train_day)]
                stock_returns = train.groupby('Name').apply(calculate_returns).sort_values(ascending=False)
                stock_returns_table = stock_returns.reset_index()
                stock_returns_table.columns = ['Name', 'Returns']  # שמות לעמודות
                for i in range(10, 300, 10):  # כמות מניות לבדוק
                    profitable_stock = stock_returns_table[:i]
                    new_stock_returns = df[
                        (df['dt'] > end_train_day) & (df['dt'] < end_train_day + timedelta(days=qtr))].groupby(
                        'Name').apply(calculate_returns).sort_values(ascending=False)
                    new_stock_returns_table = new_stock_returns.reset_index()
                    new_stock_returns_table.columns = ['Name', 'Returns']  # שמות לעמודות
                    o = new_stock_returns_table.mean(axis=0)  # ממוצע כל המניות החדשות
                    profitable_stock_name = profitable_stock['Name']
                    train_profitable_stock = profitable_stock_name.to_list()
                    part_new_stock_returns_table = new_stock_returns_table[
                        new_stock_returns_table['Name'].isin(train_profitable_stock)]
                    p = part_new_stock_returns_table.mean(axis=0)
                    r.append(
                        {
                            'days_for_invest': qtr,
                            'start_date': start_train_day,
                            'end_date': end_train_day,
                            'delta': delta,
                            'amount': i,
                            'old_mean': o[0],
                            'mean': p[0],
                            'diff': p[0] - o[0]

                        })
            print((d / (1760 * 4)) * 100)
    results_df = pd.DataFrame(r)
    results_df.sort_values('diff', ascending=False)
    results_df.dropna()
    results_df['est'] = results_df['diff']
    results_df['est'] = np.where((results_df['est'] < 0), results_df['est'] * -results_df['est'],
                                 results_df['est'])  # כלכלה , כריית מידע, כהנמן כלכלה התנהגותית
    results_df['loss'] = np.where((results_df['diff'] < 0), 1, 0)
    return results_df


def heat_map(df):
    heatmap1_data = pd.pivot_table(df, values='est',
                                   index=['amount'],
                                   columns='delta')
    fig, ax = plt.subplots(figsize=(7, 7))
    sns.heatmap(heatmap1_data, ax=ax)
    plt.show()


def compare_to_snp(df, days, amount,days_for_invest):
    r = []
    for d in range(0, 1110, 31):
        end_train_day = datetime(2016, 1, 1)+timedelta(days=d)
        start_train_day = end_train_day - timedelta(days=days)
        train = df[(df['dt'] > start_train_day) & (df['dt'] < end_train_day)]
        stock_returns = train.groupby('Name').apply(calculate_returns).sort_values(ascending=False)
        stock_returns_table = stock_returns.reset_index()
        stock_returns_table.columns=['Name', 'Returns']   # שמות לעמודות
        profitable_stock= stock_returns_table[:amount]
        new_stock_returns= df[(df['dt'] > end_train_day) & (df['dt'] < end_train_day+timedelta(days=days_for_invest))].groupby('Name').apply(calculate_returns).sort_values(ascending=False)
        new_stock_returns_table=new_stock_returns.reset_index()
        new_stock_returns_table.columns=['Name', 'Returns']   # שמות לעמודות
        # o = new_stock_returns_table.mean(axis=0)        # ממוצע כל המניות החדשות
        stocks = profitable_stock['Name'].values
        profitable_stock_return_table = new_stock_returns_table[new_stock_returns_table['Name'].isin(stocks)]
        p = profitable_stock_return_table.mean(axis=0)
        snp_return = new_stock_returns_table[new_stock_returns_table['Name'] == 'SPY']['Returns']

        r.append(
            {
                'start_invest': end_train_day,
                'snp_return': snp_return.astype(float).values[0],
                # 'snp_return': o[0],
                'stg_return': p[0],
                'diff': p[0]-snp_return.astype(float).values[0]
                # 'diff': p[0] - o[0]

            })

    results_df_check = pd.DataFrame(r)
    results_df_check['start_invest'] = results_df_check['start_invest'].dt.date
    return results_df_check


# Function that check what is the stock return
def calculate_returns(x):
    return 100*(x['Close'].iloc[-1] - x['Open'].iloc[0])/x['Open'].iloc[0]


def profitable_stocks(df, start_date):
    end_train_day = start_date
    start_train_day = end_train_day - timedelta(days=80)
    train = df[(df['dt'] < end_train_day) & (df['dt'] > start_train_day)]
    stock_returns = train.groupby('Name').apply(calculate_returns).sort_values(ascending=False)
    stock_returns_table = stock_returns.reset_index()
    stock_returns_table.columns = ['Name', 'Returns']  # שמות לעמודות
    profitable_stock = stock_returns_table[:10]
    new_stock_returns = df[(df['dt'] > end_train_day) & (df['dt'] < end_train_day + timedelta(days=360))].groupby(
        'Name').apply(calculate_returns).sort_values(ascending=False)
    new_stock_returns_table = new_stock_returns.reset_index()
    new_stock_returns_table.columns = ['Name', 'Returns']  # שמות לעמודות
    # snp_return = new_stock_returns_table.mean(axis=0)
    stocks = profitable_stock['Name'].values
    profitable_stock_return_table = new_stock_returns_table[new_stock_returns_table['Name'].isin(stocks)]
    profitable_stock_return = profitable_stock_return_table.mean(axis=0)
    snp_return = new_stock_returns_table[new_stock_returns_table['Name'] == 'SPY']['Returns']
    return [snp_return.astype(float).values[0], profitable_stock_return[0], stocks]


def sell_adx(adx, rsi, adx_r, rsi_r, adx_op, rsi_op):
    return adx_op(adx, adx_r) and rsi_op(rsi, rsi_r)


def ret(df, stocks, end_train_day, adx_r, rsi_r, adx_op, rsi_op):
    stg_money = 0
    all_days = 0
    stg_days = 0
    for s in stocks:
        new_df = df[df['Name'] == s]
        new_df.reset_index(drop=True, inplace=True)
        amount = 10000
        new_amount = amount
        start_price = new_df.iloc[0]['Open']
        in_position = False
        for d in range(len(new_df) - 1):
            df_row = new_df.iloc[d]
            if not sell_adx(df_row['ADX'], df_row['RSI'], adx_r, rsi_r, adx_op, rsi_op) and not in_position:
                start_price = new_df.iloc[d + 1]['Open']
                in_position = True
            if sell_adx(df_row['ADX'], df_row['RSI'], adx_r, rsi_r, adx_op, rsi_op) and in_position:
                end_price = new_df.iloc[d + 1]['Open']
                in_position = False
                new_amount = new_amount * (end_price / start_price)
            if in_position:
                stg_days = stg_days + 1

        if in_position:
            end_price = new_df.iloc[-1]['Close']
            new_amount = new_amount * (end_price / start_price)

        stg_money = stg_money + new_amount
        all_days = all_days+(len(new_df) - 1)
    return [all_days / len(stocks), stg_days / 10, 1, (stg_money / 100000) - 1,
            1, stg_money, end_train_day]


def optimization(df, days_for_check, interval, adx_op, rsi_op):
    l = []
    days_for_check = days_for_check
    interval = interval
    for d in range(0, days_for_check, interval):
        end_train_day = datetime(2010, 1, 1) + timedelta(days=d)
        portfolio = profitable_stocks(df, end_train_day)
        new_df = df[(df['dt'] >= (end_train_day - timedelta(days=1))) &
                    (df['dt'] <= (end_train_day + timedelta(days=361)))]
        new_df = new_df[new_df['Name'].isin(portfolio[2])]
        print(((d + interval) / days_for_check) * 100)
        for adx_r in range(0, 100, 5):
            for rsi_r in range(0, 100, 5):
                p = ret(new_df, portfolio[2], end_train_day, adx_r, rsi_r, adx_op, rsi_op)
                l.append(
                    {
                        'start_date': p[6],
                        'all_days': p[0],
                        'stg_days': p[1],
                        'adx_r': adx_r,
                        'rsi_r': rsi_r,
                        'return_buy_and_hold': portfolio[1],
                        'return_stg_per_day': p[3] * p[0] * 100 / (p[1] if p[1] > 0 else 1),
                        'stg_return': p[3] * 100,
                        'return_snp': portfolio[0],
                        'stg_return_est': p[3] * 100 if p[3] > 0 else p[3]*-p[3]*-p[3]
                    })
    results_df = pd.DataFrame(l)
    results_df_mean = results_df.groupby(['adx_r', 'rsi_r']).mean().sort_values('stg_return_est', ascending=False)
    return results_df_mean


def result_check(df, axd_r, rsi_r, days_for_check, interval, adx_op, rsi_op):
    r = []
    days_for_check = days_for_check
    interval = interval
    for d in range(0, days_for_check, interval):
        end_train_day = datetime(2016, 1, 1) + timedelta(days=d)
        portfolio = profitable_stocks(df, end_train_day)
        new_df = df[(df['dt'] >= (end_train_day - timedelta(days=1))) &
                    (df['dt'] <= (end_train_day + timedelta(days=361)))]
        new_df = new_df[new_df['Name'].isin(portfolio[2])]
        print(((d + interval) / days_for_check) * 100)
        p = ret(new_df, portfolio[2], d, axd_r, rsi_r, adx_op, rsi_op)
        r.append(
            {
                'start_date': f"{end_train_day:%Y-%m-%d}",
                'all_days': p[0],
                'stg_days': p[1],
                'return_buy_and_hold': portfolio[1],
                'return_stg_per_day': p[3] * p[0] * 100 / (p[1] if p[1] > 0 else 1),
                'stg_return': p[3] * 100,
                'return_snp': portfolio[0]
            })

    results_df_check = pd.DataFrame(r)
    return results_df_check


def check_10_stocks(df, end_train_day, adx_r, rsi_r, adx_op, rsi_op):
    portfolio = profitable_stocks(df, end_train_day)
    df = df[(df['dt'] >= (end_train_day - timedelta(days=1))) &
            (df['dt'] <= (end_train_day + timedelta(days=361)))]
    df = df[df['Name'].isin(portfolio[2])]
    all_days = 0
    total_amount = 0
    buy_and_hold_return = 0
    for s in portfolio[2]:
        win = 0
        loss = 0
        stg_money = 0
        stg_days = 0
        amount = 10000
        new_amount = amount
        new_df = df[df['Name'] == s]
        new_df.reset_index(drop=True, inplace=True)
        start_price = new_df.iloc[0]['Open']
        new_df['pos'] = new_df['Close'].min() - 4
        in_position = False
        for d in range(len(new_df) - 1):
            df_row = new_df.iloc[d]
            df_tomorrow = new_df.iloc[d+1]

            if not sell_adx(df_row['ADX'], df_row['RSI'], adx_r, rsi_r, adx_op, rsi_op) and not in_position:
                start_price = df_tomorrow['Open']
                in_position = True
            if sell_adx(df_row['ADX'], df_row['RSI'], adx_r, rsi_r, adx_op, rsi_op) and in_position:
                end_price = df_tomorrow['Open']
                in_position = False
                new_amount = new_amount * (end_price / start_price)
            if in_position:
                stg_days = stg_days + 1
                new_df.loc[d+1, 'pos'] = df_tomorrow['Open']

        if in_position:
            end_price = new_df.iloc[-1]['Close']
            new_amount = new_amount * (end_price / start_price)
        stock_return = calculate_returns(new_df)
        stg_money = stg_money + new_amount
        all_days = all_days + (len(new_df) - 1)
        total_amount = total_amount + ((new_amount/10000)-1)*100
        buy_and_hold_return = buy_and_hold_return + (calculate_returns(new_df))
        print(s)
        print(((stg_money/10000)-1)*100)
        print(stock_return)
        print(stg_days)
        print(win)
        print(loss)
        ax = new_df.plot.line(x='dt', y=['Open'], figsize=(25, 10), title=s, color=['blue'])
        new_df.plot.line(x='dt', y=['pos'], figsize=(25, 10), title=s, color=['orange'], alpha=0.5, ax=ax)
        # new_df.plot.line(x='dt', y=['Open', 'pos'], figsize=(25, 10), title=s, color=['blue', 'orange'],
        # alpha=[0.9, 0.5])
        plt.show()

    print('end')
    print(total_amount/10)
    print(buy_and_hold_return/10)



