#!/usr/bin/python

print('Recent_EV - initiating.')

import os
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None
pd.set_option('use_inf_as_na', True)

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"

# import
prices_table = pd.read_csv(os.path.join(cwd,input_folder,"2_processed_prices.csv"), low_memory=False)
financials_a = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_a.csv"), low_memory=False)
financials_q = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_q.csv"), low_memory=False)
#EV_table = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_EV_q.csv"), low_memory=False)

prices_table = prices_table #.head(50)
prices_table = prices_table[(prices_table['marketCap'] > 0)]

# find recent q and a, merge and fix missing values in q from a, then calculate EV, and yearly price diffs
recent_q = financials_q.sort_values(['symbol','date']
                        , ascending=False).groupby('symbol').head(1).drop_duplicates(['symbol'], keep='first')
recent_a = financials_a.sort_values(['symbol','date']
                        , ascending=False).groupby('symbol').head(1).drop_duplicates(['symbol'], keep='first')
df_merged = pd.merge(recent_q, recent_a
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_a'))
df_merged['capitalExpenditure_a_to_q'] = df_merged['capitalExpenditure_a']/4
df_merged['capitalExpenditure'] = df_merged['capitalExpenditure'].fillna(df_merged['capitalExpenditure_a_to_q'])
df_merged['capitalExpenditure'] = df_merged['capitalExpenditure'].fillna(df_merged['capitalExpenditure_a_to_q'])
df_merged['capitalExpenditure'] = np.where(df_merged['capitalExpenditure'] == 0, df_merged['capitalExpenditure_a_to_q'], df_merged['capitalExpenditure'])

df_merged['totalDebt'] = df_merged['totalDebt'].fillna(df_merged['totalDebt_a'])
df_merged['cashAndCashEquivalents'] = df_merged['cashAndCashEquivalents'].fillna(df_merged['cashAndCashEquivalents_a'])
df_merged['preferredStock'] = df_merged['preferredStock'].fillna(df_merged['preferredStock_a'])
df_merged['minorityInterest'] = df_merged['minorityInterest'].fillna(df_merged['minorityInterest_a'])

df_recent = df_merged[['symbol','capitalExpenditure','totalDebt','cashAndCashEquivalents','preferredStock','minorityInterest']]
df_merged = pd.merge(prices_table, df_recent
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged['EV'] = df_merged['marketCap'] + df_merged['totalDebt'] - df_merged['cashAndCashEquivalents'] + df_merged['preferredStock'] + df_merged['minorityInterest']

df_merged['from_low'] = (df_merged['price'] - df_merged['yearLow']) / df_merged['yearLow'] * 100
df_merged.loc[(df_merged['from_low'] < 0), 'from_low'] = 0
df_merged['from_high'] = (df_merged['price'] - df_merged['yearHigh']) / df_merged['yearHigh'] * 100

# export
df = df_merged
df.to_csv(os.path.join(cwd,input_folder,"4_recent_EV_prices_diff.csv"), index = False)
print('4_recent_EV_prices_diff created')




