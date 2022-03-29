#!/usr/bin/python

print('4_recent_OwnEa_q_last_8 - initiating.')

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

eight_quarters = financials_q.groupby('symbol').head(8).reset_index(drop=True)
eight_quarters['quarter_count'] = eight_quarters.groupby(['symbol']).cumcount()+1
eight_quarters['quarter_count'] = eight_quarters['quarter_count'].mask(eight_quarters['quarter_count'] <= 4, 1)
eight_quarters['quarter_count'] = eight_quarters['quarter_count'].mask(eight_quarters['quarter_count'] > 4, 2)

eight_quarters['rev1'] = eight_quarters.loc[eight_quarters['quarter_count'] == 1, 'revenue']
eight_quarters['rev2'] = eight_quarters.loc[eight_quarters['quarter_count'] == 2, 'revenue']
eight_quarters.fillna(0)
eight_quarters_sales_temp = eight_quarters.groupby('symbol').sum().reset_index()
eight_quarters_sales_temp['Sales_diff_eight_quarters'] = eight_quarters_sales_temp['rev1'] - eight_quarters_sales_temp['rev2']
eight_quarters_sales_diff = eight_quarters_sales_temp[['symbol', 'Sales_diff_eight_quarters', 'capitalExpenditure', 'netCashProvidedByOperatingActivites']]
df_merged = pd.merge(eight_quarters_sales_diff, recent_OwnEa_a, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_a'))

eight_q = df_merged
eight_q['maint_capex'] = eight_q['Sales_diff_eight_quarters'] * eight_q['maint_capex_ratio'] * -1
eight_q['Capex'] = eight_q.loc[eight_q['maint_capex'] < eight_q['capitalExpenditure'], 'maint_capex']
eight_q['OwnEa_eight_q'] = eight_q['netCashProvidedByOperatingActivites'] - eight_q['maint_capex']

# export maint_capex_ratio and OwnEa
df_maint_capex_ratio = eight_q[['symbol', 'OwnEa_eight_q']]
df_OwnEa_temp = eight_q.groupby('symbol').sum().reset_index()
df_OwnEa = df_OwnEa_temp[['symbol', 'OwnEa_eight_q']]
df_OwnEa.to_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa_OwnEa_q_last_8.csv"), index = False)

print('4_recent_OwnEa_q_last_8 created')