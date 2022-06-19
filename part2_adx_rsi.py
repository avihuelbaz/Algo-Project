from functions import *
from prepare_data import *
import operator as op

# create the df
# df = create_df_from_yahoo()
# df = prepare_df(df)
# df.to_csv('csv/snp_2009_2020_with_spy.csv')
df = pd.read_csv('csv/snp_2009_2020_with_spy.csv')
df['dt'] = pd.to_datetime(df['Date'])
df = df[df['Name'] != 'MOS']


# optimization for the stg
# adx_gr_rsi_gr = optimization(df, 2070, 90, op.gt, op.gt)
# adx_gr_rsi_gr['ADX_S'] = 'gr'
# adx_gr_rsi_gr['RSI_S'] = 'gr'
#
# adx_gr_rsi_de = optimization(df, 2070, 90, op.gt, op.lt)
# adx_gr_rsi_de['ADX_S'] = 'gr'
# adx_gr_rsi_de['RSI_S'] = 'de'
#
# adx_de_rsi_gr = optimization(df, 2070, 90, op.lt, op.gt)
# adx_de_rsi_gr['ADX_S'] = 'de'
# adx_de_rsi_gr['RSI_S'] = 'gr'
#
# adx_de_rsi_de = optimization(df, 2070, 90, op.lt, op.lt)
# adx_de_rsi_de['ADX_S'] = 'de'
# adx_de_rsi_de['RSI_S'] = 'de'
#
# optimization_adx_rsi = pd.concat([adx_de_rsi_de, adx_de_rsi_gr, adx_gr_rsi_gr, adx_gr_rsi_de])
# optimization_adx_rsi.to_csv('csv/optimization_adx_rsi.csv')
optimization_adx_rsi = pd.read_csv('csv/optimization_adx_rsi.csv')
optimization_adx_rsi.sort_values('return_stg_per_day', ascending=False, inplace=True)


# check the test
results_df_check = result_check(df, 10, 50, 1110, 30, op.gt, op.gt)
print('return_stg_per_day: ' + str(results_df_check['return_stg_per_day'].mean()))
print('return_buy_and_hold: ' + str(results_df_check['return_buy_and_hold'].mean()))
print('stg_return: ' + str(results_df_check['stg_return'].mean()))
print('return_snp: ' + str(results_df_check['return_snp'].mean()))
results_df_check.plot.bar(x='start_date', y=['return_buy_and_hold', 'return_stg_per_day', 'stg_return', 'return_snp'],
                          figsize=(30, 16))

# check specific case
check_10_stocks(df, datetime(2018, 1, 20), 10, 45, op.gt, op.gt)
