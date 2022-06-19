import backtrader as bt
from functions import *
from sklearn.preprocessing import MinMaxScaler
from sklearn import linear_model


class LrInd(bt.SignalStrategy):
    params = (('b', None), ('s', None))

    def __init__(self):
        pass

    def start(self):
        pass

    def next(self):
        diff = ((self.data.lstm_prediction[0] - self.data.close[0]) / self.data.close[0]) * 100
        if self.position.size == 0:
            if diff > self.params.b:
                self.buy()
        elif self.position.size != 0:
            if diff < -self.params.s:
                self.sell()

    def stop(self):
        pass

    #         print('End')

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                pass
            else:  # Sell
                pass


class AdxRsi(bt.SignalStrategy):
    params = (('rsi_r', None), ('adx_r', None), ('adx_op', None), ('rsi_op', None))

    def __init__(self):
        self.rsi = bt.ind.RSI(period=20)
        self.adx = bt.ind.AverageDirectionalMovementIndex(period=20)

    def start(self):
        pass

    def next(self):
        if self.position.size == 0:
            if not (self.params.adx_op(self.adx, self.params.adx_r) and self.params.rsi_op(self.rsi, self.params.rsi_r)):
                self.buy()
        elif self.position.size != 0:
            if self.params.adx_op(self.adx, self.params.adx_r) and self.params.rsi_op(self.rsi, self.params.rsi_r):
                self.sell()

    def stop(self):
        pass

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                pass
            else:  # Sell
                pass


def ret_bd(df, end_train_day, adx_r, rsi_r, adx_op, rsi_op):
    stg_return = 0
    all_days = 0
    stg_days = 0
    start_date = end_train_day
    end_date = start_date + timedelta(days=500)
    stocks = profitable_stocks(df, start_date)
    for s in stocks[2]:
        new_df = df[(df['dt'] > start_date - timedelta(days=100)) &
                    (df['dt'] <= end_date) & (df['Name'] == s)]
        new_df = new_df.set_index('dt')
        new_df['dt'] = pd.to_datetime(new_df['Date'])
        contract_history = new_df
        data_pd = bt.feeds.PandasData(dataname=contract_history,
                                      fromdate=start_date - timedelta(days=40),
                                      todate=start_date + timedelta(days=360))
        cerebro = bt.Cerebro()
        cerebro.addstrategy(AdxRsi, rsi_r=rsi_r, adx_r=adx_r, adx_op=adx_op, rsi_op=rsi_op)
        cerebro.adddata(data_pd)
        cerebro.addsizer(bt.sizers.PercentSizer, percents=100)
        cerebro.run()
        stg_return = stg_return + cerebro.broker.getvalue()
        all_days = all_days + len(contract_history)
    return [((stg_return/100000)-1)*100, stocks[1], stocks[0]]


def result_check_bd(df, adx_r, rsi_r, days_for_check, interval, adx_op, rsi_op):
    r = []
    days_for_check = days_for_check
    interval = interval
    for d in range(0, days_for_check, interval):
        start_date = datetime(2016, 1, 1) + timedelta(days=d)
        #start_date = datetime(2011, 1, 1) + timedelta(days=d)
        end_train_day = start_date + timedelta(days=500)
        print(((d + interval) / days_for_check) * 100)
        p = ret_bd(df, start_date, adx_r, rsi_r, adx_op, rsi_op)
        r.append(
            {
                'start_date': f"{start_date:%Y-%m-%d}",
                'return_buy_and_hold': p[1],
                'stg_return': p[0],
                'return_snp': p[2]
            })

    results_df_check = pd.DataFrame(r)
    return results_df_check


def optimization_bd(df, days_for_check, interval, adx_op, rsi_op):
    l = []
    days_for_check = days_for_check
    interval = interval
    for d in range(0, days_for_check, interval):
        end_train_day = datetime(2010, 1, 1) + timedelta(days=d)
        portfolio = profitable_stocks(df, end_train_day)
        print(((d + interval) / days_for_check) * 100)
        for adx_r in range(0, 100, 5):
            for rsi_r in range(0, 100, 5):
                p = ret_bd(df, end_train_day, adx_r, rsi_r, adx_op, rsi_op)
                l.append(
                    {
                        'start_date': f"{end_train_day:%Y-%m-%d}",
                        'adx_r': adx_r,
                        'rsi_r': rsi_r,
                        'return_buy_and_hold': p[1],
                        'stg_return': p[0],
                        'return_snp': p[2],
                        'stg_return_est': p[0] if p[0] > 0 else p[0]*-p[0]*-p[0]
                    })
    results_df = pd.DataFrame(l)
    results_df_mean = results_df.groupby(['adx_r', 'rsi_r']).mean().sort_values('stg_return_est', ascending=False)
    return results_df_mean


def check_10_stocks_bd(df, start_date_test, adx_r, rsi_r, adx_op, rsi_op):
    stg_return = 0
    buy_and_hold_return = 0
    start_date = start_date_test
    end_train_day = start_date + timedelta(days=500)
    stocks = profitable_stocks(df, start_date)
    for s in stocks[2]:
        new_df = df[(df['dt'] > start_date - timedelta(days=100)) &
                    (df['dt'] <= end_train_day) & (df['Name'] == s)]
        new_df = new_df.set_index('dt')
        new_df['dt'] = pd.to_datetime(new_df['Date'])
        contract_history = new_df
        data_pd = bt.feeds.PandasData(dataname=contract_history,
                                      fromdate=start_date - timedelta(days=40),
                                      todate=start_date + timedelta(days=360))
        df_buy_and_hold = contract_history[(contract_history['dt'] >= start_date) &
                                           (contract_history['dt'] <= (start_date + timedelta(days=360)))]

        cerebro = bt.Cerebro()
        cerebro.addstrategy(AdxRsi, rsi_r=rsi_r, adx_r=adx_r, adx_op=adx_op, rsi_op=rsi_op)
        cerebro.adddata(data_pd)
        cerebro.addsizer(bt.sizers.PercentSizer, percents=100)

        # Print out the starting conditions
        print(s)
        # Run over everything
        # cerebro.addwriter(bt.WriterFile, out='test.csv', csv=True)
        cerebro.run()

        # Print out the final result
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        print("buy_and_hold_return: " + str(10000 * (1 + calculate_returns(df_buy_and_hold) / 100)))
        stg_return = stg_return + cerebro.broker.getvalue()
        buy_and_hold_return = buy_and_hold_return + 10000 * (1 + calculate_returns(df_buy_and_hold) / 100)
        cerebro.plot()
        plt.savefig('rsi_adx_bd_photos/' + start_date_test.strftime("%Y-%m-%d") + ' ' + s + '.png', bbox_inches='tight')

    print("stg_return: " + str(stg_return))
    print("buy_and_hold_return: " + str(buy_and_hold_return))


def optimization_bd_lr(df, days_for_check, interval):
    r = []
    for d in range(0, days_for_check, interval):
        start_date = datetime(2014, 1, 1) + timedelta(days=d)
        end_date = start_date + timedelta(360)
        print(((d + interval) / days_for_check) * 100)
        for b in range(-10, -4, 1):
            for s in range(4, 10, 1):
                p = bd_check_lr(df, start_date, end_date, b/10, s/10)
                r.append(
                    {
                        'b': b/10,
                        's': s/10,
                        'start_date': f"{start_date:%Y-%m-%d}",
                        'return_buy_and_hold': p[0],
                        'stg_return': p[1],
                        'return_snp': p[2],
                        'stg_return_est': p[1] if p[1] > 0 else p[1]*-p[1]*-p[1]
                    })
    results_df = pd.DataFrame(r)
    results_df_mean = results_df.groupby(['b', 's']).mean().sort_values('stg_return_est', ascending=False)
    return results_df_mean



def linear_reg(df_stock, start_date, end_date):

    sc_one = MinMaxScaler()
    norm_columns = ['Close']
    x_norm_one = sc_one.fit_transform(df_stock[norm_columns].values)

    norm_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'TEMA10']
    sc_five = MinMaxScaler()
    x_norm_five = sc_five.fit_transform(df_stock[norm_columns].values)
    df_stock['target'] = df_stock['Close'].shift(-1)
    df_stock.head(5)

    cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'TEMA10']
    train = df_stock[(df_stock['Date'] < start_date)]
    test = df_stock[(df_stock['Date'] >= start_date) & (df_stock['Date'] <= end_date)]
    X_train = train[cols]
    y_train = train['target']
    X_test = test[cols]
    y_test = test['target']
    X_all = df_stock[cols]

    # LinearRegression
    lm = linear_model.LinearRegression()
    model = lm.fit(X_train, y_train)
    y_pred = lm.predict(X_all)
    y_pred_test = lm.predict(X_test)

    pred = y_pred.reshape(-1, 1)
    actual = y_test.to_numpy()
    pred_test = y_pred_test.reshape(-1, 1)

    results = pd.DataFrame(actual, columns=['actual'])
    results2 = pd.DataFrame(pred_test, columns=['pred_test'])
    results['pred_test'] = results2['pred_test'].values
    squered_error = ((results['actual'] - results['pred_test']) ** 2).mean() ** 0.5

    df_stock = df_stock.reset_index()
    df_stock['pred'] = pred

    df_spy_to_csv = df_stock[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'pred']]
    df_spy_to_csv = df_spy_to_csv.set_index('Date')
    df_spy_to_csv.to_csv('csv/stock_lr.csv')


def bd_check_lr(df, start_date, end_date, b, s):
    stocks = profitable_stocks(df, start_date)
    mean_stg_return = 0
    mean_basic_return = 0
    for stock in stocks[2]:
        df_stock = df[df['Name'] == stock]
        linear_reg(df_stock, start_date, end_date)
        start_cash = 10000
        cerebro = bt.Cerebro()
        cerebro.addstrategy(LrInd, b=b, s=s)
        cerebro.addsizer(bt.sizers.PercentSizer, percents=90)
        cerebro.broker.setcash(start_cash)
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name="dd")

        class GenericCSV(bt.feeds.GenericCSVData):
            lines = ('lstm_prediction',)
            params = (('nullvalue', float('NaN')),
                      ('fromdate', start_date),
                      ('todate', end_date),
                      ('dtformat', '%Y-%m-%d'),
                      ('lstm_prediction', 6),
                      )

        data = GenericCSV(dataname="csv/stock_lr.csv")
        cerebro.adddata(data)
        cerebro.run()
        current_value = (100 * (cerebro.getbroker().get_value() - start_cash) / start_cash)
        mean_stg_return = mean_stg_return + current_value
        # print('Max drawdown: ' +str(round(firstStrat.analyzers.dd.get_analysis().max.drawdown,2))+'%')
        # cerebro.plot()
        cerebro = bt.Cerebro()
        cerebro.addstrategy(LrInd, b=-10000, s=10000)
        cerebro.addsizer(bt.sizers.PercentSizer, percents=90)
        cerebro.broker.setcash(start_cash)
        data = GenericCSV(dataname="csv/stock_lr.csv")
        cerebro.adddata(data)
        cerebro.run()
        current_basic_value = (100 * (cerebro.getbroker().get_value() - start_cash) / start_cash)
        mean_basic_return = mean_basic_return + current_basic_value
    return [mean_basic_return/10, mean_stg_return/10, stocks[0]]


def results_bd_lr(df, b, s, days_for_check, interval):
        lr = []
        for d in range(0, days_for_check, interval):
            start_date = datetime(2016, 1, 1) + timedelta(days=d)
            end_date = start_date + timedelta(days=360)
            print(((d + interval) / days_for_check) * 100)
            p = bd_check_lr(df, start_date, end_date, b, s)
            lr.append(
                {
                    'start_date': f"{start_date:%Y-%m-%d}",
                    'return_buy_and_hold': p[0],
                    'stg_return': p[1],
                    'return_snp': p[2]
                })

        results_df_check = pd.DataFrame(lr)
        return results_df_check


def check_10_stocks_lr(df, start_date, b, s):
    end_date = start_date + timedelta(days=360)
    stocks = profitable_stocks(df, start_date)
    mean_stg_return = 0
    mean_basic_return = 0
    for stock in stocks[2]:
        df_stock = df[df['Name'] == stock]
        linear_reg(df_stock, start_date, end_date)
        start_cash = 10000
        cerebro = bt.Cerebro()
        cerebro.addstrategy(LrInd, b=b, s=s)
        cerebro.addsizer(bt.sizers.PercentSizer, percents=90)
        cerebro.broker.setcash(start_cash)
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name="dd")

        class GenericCSV(bt.feeds.GenericCSVData):
            lines = ('lstm_prediction',)
            params = (('nullvalue', float('NaN')),
                      ('fromdate', start_date),
                      ('todate', end_date),
                      ('dtformat', '%Y-%m-%d'),
                      ('lstm_prediction', 6),
                      )

        data = GenericCSV(dataname="csv/stock_lr.csv")
        cerebro.adddata(data)
        cerebro.run()
        current_value = (100 * (cerebro.getbroker().get_value() - start_cash) / start_cash)
        mean_stg_return = mean_stg_return + current_value
        cerebro.plot()
        plt.savefig('lr/' + start_date.strftime("%Y-%m-%d") + ' ' + stock + '.png', bbox_inches='tight')
        print(stock)
        print('stg_return: '+str(current_value))

        cerebro = bt.Cerebro()
        cerebro.addstrategy(LrInd, b=-10000, s=10000)
        cerebro.addsizer(bt.sizers.PercentSizer, percents=90)
        cerebro.broker.setcash(start_cash)
        data = GenericCSV(dataname="csv/stock_lr.csv")
        cerebro.adddata(data)
        cerebro.run()
        current_basic_value = (100 * (cerebro.getbroker().get_value() - start_cash) / start_cash)
        mean_basic_return = mean_basic_return + current_basic_value
        print('basic_return: '+str(current_basic_value))
    print('mean_basic_return: '+str(mean_basic_return/10))
    print('mean_stg_return: '+str(mean_stg_return/10))
    print('snp_return: '+str(stocks[0]))


