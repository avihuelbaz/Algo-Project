from functions_bd import *
import operator as op
# create the df
# df = create_df_from_yahoo()
# df = prepare_df(df)
# df.to_csv('csv/snp_2009_2020_with_spy.csv')
df = pd.read_csv('csv/snp_2009_2020_with_spy.csv')
df['dt'] = pd.to_datetime(df['Date'])

# optimization for the stg
adx_gr_rsi_gr_bd = optimization_bd(df, 2070, 90, op.gt, op.gt)
adx_gr_rsi_gr_bd['ADX_S'] = 'gr'
adx_gr_rsi_gr_bd['RSI_S'] = 'gr'

adx_gr_rsi_de_bd = optimization_bd(df, 2070, 90, op.gt, op.lt)
adx_gr_rsi_de_bd['ADX_S'] = 'gr'
adx_gr_rsi_de_bd['RSI_S'] = 'de'

adx_de_rsi_gr_bd = optimization_bd(df, 2070, 90, op.lt, op.gt)
adx_de_rsi_gr_bd['ADX_S'] = 'de'
adx_de_rsi_gr_bd['RSI_S'] = 'gr'

adx_de_rsi_de_bd = optimization_bd(df, 2070, 90, op.lt, op.lt)
adx_de_rsi_de_bd['ADX_S'] = 'de'
adx_de_rsi_de_bd['RSI_S'] = 'de'

optimization_adx_rsi_bd = pd.concat([adx_de_rsi_de_bd, adx_de_rsi_gr_bd, adx_gr_rsi_gr_bd, adx_gr_rsi_de_bd])
optimization_adx_rsi_bd.to_csv('csv/optimization_adx_rsi_bd.csv')
optimization_adx_rsi_bd = pd.read_csv('csv/optimization_adx_rsi_bd.csv')
optimization_adx_rsi_bd.sort_values('stg_return_est', ascending=False, inplace=True)


# results_df_check = result_check_bd(df, 10, 50, 1110, 30, op.gt, op.gt)
plt.style.use('dark_background')
results_df_check = result_check_bd(df, 10, 50, 1110, 31,  op.gt, op.gt)
print('return_buy_and_hold: ' + str(results_df_check['return_buy_and_hold'].mean()))
print('stg_return: ' + str(results_df_check['stg_return'].mean()))
print('return_snp: ' + str(results_df_check['return_snp'].mean()))
results_df_check.plot.bar(x='start_date', y=['return_buy_and_hold', 'return_snp','stg_return' ], figsize=(30, 16))

print(results_df_check['stg_return'].std())

start_date = datetime(2017, 1, 24)
check_10_stocks_bd(df, start_date, 10, 50, op.gt, op.gt)
