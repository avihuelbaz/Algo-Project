from functions import *
from prepare_data import *

# create the df
df = create_df_from_yahoo()
df = prepare_df(df)
# df.to_csv('csv/snp_2009_2020_with_spy.csv')
# df = pd.read_csv('csv/snp_2009_2020_with_spy.csv')
df['dt'] = pd.to_datetime(df['Date'])


df_russel = create_df_from_yahoo_russel()
df_russel = prepare_df(df_russel)
# df.to_csv('csv/snp_2009_2020_with_spy.csv')
# df = pd.read_csv('csv/snp_2009_2020_with_spy.csv')
df_russel['dt'] = pd.to_datetime(df_russel['Date'])

optimization_portfolio = optimization_part1(df)
# optimization_portfolio.to_csv('csv/optimization_portfolio.csv')
# optimization_portfolio = pd.read_csv('csv/optimization_portfolio.csv')


df_1qtr = optimization_portfolio[optimization_portfolio['days_for_invest'] == 90]
df_2qtr = optimization_portfolio[optimization_portfolio['days_for_invest'] == 180]
df_3qtr = optimization_portfolio[optimization_portfolio['days_for_invest'] == 270]
df_4qtr = optimization_portfolio[optimization_portfolio['days_for_invest'] == 360]

df_1qtr_mean = df_1qtr.groupby(['amount', 'delta']).mean().sort_values('est', ascending=False)
df_1qtr_mean = df_1qtr_mean.reset_index()
heat_map(df_1qtr_mean)

invest_table_1qtr = compare_to_snp(df, 170, 50, 90)
invest_table_1qtr.plot.bar(x='start_invest', y=['stg_return', 'snp_return'], figsize=(15, 6))
print(((1+invest_table_1qtr['snp_return'].mean()/100)**4-1)*100)
print(((1+invest_table_1qtr['stg_return'].mean()/100)**4-1)*100)

df_2qtr_mean = df_2qtr.groupby(['amount', 'delta']).mean().sort_values('est', ascending=False)
df_2qtr_mean = df_2qtr_mean.reset_index()
heat_map(df_2qtr_mean)

invest_table_2qtr = compare_to_snp(df, 220, 50, 180)
invest_table_2qtr.plot.bar(x='start_invest', y=['stg_return', 'snp_return'], figsize=(15, 6))
print(((1+invest_table_2qtr['snp_return'].mean()/100)**2-1)*100)
print(((1+invest_table_2qtr['stg_return'].mean()/100)**2-1)*100)


df_3qtr_mean = df_3qtr.groupby(['amount', 'delta']).mean().sort_values('est', ascending=False)
df_3qtr_mean = df_3qtr_mean.reset_index()
heat_map(df_3qtr_mean)

invest_table_3qtr = compare_to_snp(df, 250, 50, 270)
invest_table_3qtr.plot.bar(x='start_invest', y=['stg_return', 'snp_return'], figsize=(15, 6))
print(((1+invest_table_3qtr['snp_return'].mean()/100)**1.5-1)*100)
print(((1+invest_table_3qtr['stg_return'].mean()/100)**1.5-1)*100)

df_4qtr_mean = df_4qtr.groupby(['amount', 'delta']).mean().sort_values('est', ascending=False)
df_4qtr_mean = df_4qtr_mean.reset_index()
heat_map(df_4qtr_mean)

plt.style.use('dark_background')
invest_table_4qtr = compare_to_snp(df, 180, 5, 1000)
invest_table_4qtr.plot.bar(x='start_invest', y=['stg_return', 'snp_return'], figsize=(15, 6))
print(((1+invest_table_4qtr['snp_return'].mean()/100)-1)*100)
print(((1+invest_table_4qtr['stg_return'].mean()/100)-1)*100)

invest_table_4qtr = compare_to_snp(df_russel, 180, 5, 1000)
invest_table_4qtr.plot.bar(x='start_invest', y=['stg_return', 'snp_return'], figsize=(15, 6))
print(((1+invest_table_4qtr['russel_return'].mean()/100)-1)*100)
print(((1+invest_table_4qtr['stg_return'].mean()/100)-1)*100)


print(invest_table_4qtr['stg_return'].std())

