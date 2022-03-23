#!/usr/bin/python

print('OwnEa quarterly - initiating.')

import os
import pandas as pd

pd.options.mode.chained_assignment = None
pd.set_option('use_inf_as_na', True)

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"

# import
recent_OwnEa_a = pd.read_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa_a.csv"), low_memory=False)

financials_q = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_q.csv"), low_memory=False)
#financials_q = financials_q[(financials_q['symbol'].str.contains('AAPL|MSFT'))] # for testing

financials_q = financials_q.sort_values(['symbol','date'], ascending=[False, False])
financials_q['Sales_diff'] = financials_q['revenue'] - financials_q['revenue'].shift(-1) #get diff in sales p.a.
financials_q.loc[financials_q.groupby('symbol').tail(1).index, 'Sales_diff'] = 0.0 #fix first year of every symbol

df_merged = pd.merge(financials_q, recent_OwnEa_a
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_a'))

recent_q = df_merged[(df_merged['date']>df_merged['date_a'])]

recent_q['maint_capex'] = recent_q['Sales_diff'] * recent_q['maint_capex_ratio'] * -1
recent_q['Capex'] = recent_q.loc[recent_q['maint_capex'] < recent_q['capitalExpenditure'], 'maint_capex']
recent_q['OwnEa'] = recent_q['netCashProvidedByOperatingActivites'] - recent_q['maint_capex']

# export maint_capex_ratio and OwnEa
df_maint_capex_ratio = recent_q[['symbol', 'OwnEa']]
df_maint_capex_ratio.to_csv(os.path.join(cwd,input_folder,"test.csv"), index = False)
df_OwnEa_temp = recent_q.groupby('symbol').sum().reset_index()
df_OwnEa = df_OwnEa_temp[['symbol', 'OwnEa']]
df_OwnEa.to_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa_q.csv"), index = False)

print('4_recent_OwnEa_q created')