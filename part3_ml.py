from prepare_data import *
from functions_bd import *
# create the df
df = create_df_from_yahoo()
df = prepare_df(df)
df.to_csv('csv/snp_2009_2020_with_spy_with_tema.csv')
df = pd.read_csv('csv/snp_2009_2020_with_spy_with_tema.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['dt'] = pd.to_datetime(df['Date'])
df = df[df['Name'] != 'MOS']

# optimization
#find_b_S = optimization_bd_lr(df, 720, 90)

# check the test
results_df_check = results_bd_lr(df, -0.3, 0.3, 1110, 30)
print('return_buy_and_hold: ' + str(results_df_check['return_buy_and_hold'].mean()))
print('stg_return: ' + str(results_df_check['stg_return'].mean()))
print('return_snp: ' + str(results_df_check['return_snp'].mean()))
print('return_buy_and_hold: ' + str(results_df_check['return_buy_and_hold'].std()))
print('stg_return: ' + str(results_df_check['stg_return'].std()))
print('return_snp: ' + str(results_df_check['return_snp'].std()))
results_df_check.plot.bar(x='start_date', y=['return_buy_and_hold', 'stg_return', 'return_snp'],
                          figsize=(30, 16))

# check 10 stocks
start_date = datetime(2016, 8, 28)
check_10_stocks_lr(df, start_date, -0.5, 0.5)

