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
#financials_q = financials_q[(financials_q['symbol'].str.contains('AGRX'))] # for testing |
financials_q = financials_q.sort_values(['symbol','date'], ascending=[False, False])
df_merged = pd.merge(financials_q, recent_OwnEa_a, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_a'))

# take last 8 quarters ie last 2 years, find the difference in sales. calculate OwnEa.
# we need 9 because we want to have 8 quarters of "sales growth" QoQ
eight_q = df_merged.groupby('symbol').head(9).reset_index(drop=True)
eight_q['Sales_diff'] = eight_q['revenue'] - eight_q['revenue'].shift(-1) #get diff in sales per quarter
eight_q['maint_capex'] = eight_q['Sales_diff'] * eight_q['maint_capex_ratio'] * -1
eight_q['OwnEa_eight_q'] = eight_q['netCashProvidedByOperatingActivites'] + eight_q['maint_capex']
eight_q.loc[eight_q['OwnEa_eight_q'] < 0, 'OwnEa_eight_q'] = 0
eight_q['OwnEa_eight_q_avg'] = (eight_q['OwnEa_eight_q'] / 8).round(0) # averaging out quarters

eight_q_sum = eight_q.groupby('symbol').sum().reset_index()
eight_q_sum = eight_q_sum.loc[~(eight_q_sum['revenue'] <= 0),:] # drop where no revenues
#eight_q_sum.to_csv(os.path.join(cwd,input_folder,"test.csv"), index = False)

# export maint_capex_ratio and OwnEa
df_OwnEa = eight_q_sum[['symbol', 'OwnEa_eight_q', 'OwnEa_eight_q_avg']]
df_OwnEa.to_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa_OwnEa_q_last_8.csv"), index = False)

print('4_recent_OwnEa_q_last_8 created')