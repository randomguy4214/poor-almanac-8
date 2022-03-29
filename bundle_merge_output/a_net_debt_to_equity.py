#!/usr/bin/python

print('net_debt_to_equity - initiating.')

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
financials_q = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_q.csv"), low_memory=False)
#financials_q = financials_q[(financials_q['symbol'].str.contains('AAPL|MSFT'))] # for testing

financials_q = financials_q.sort_values(['symbol','date'], ascending=[False, False])
financials_q = financials_q.groupby('symbol').head(1).drop_duplicates(['symbol'], keep='first')
financials_q['netDebtToEquity'] = (financials_q['netDebt'] / (financials_q['netDebt'] + financials_q['totalStockholdersEquity'])).round(2)
df_netDebtToEquity = financials_q[['symbol', 'netDebtToEquity']]
df_netDebtToEquity.to_csv(os.path.join(cwd,input_folder,"4_net_debt_to_equity.csv"), index = False)

print('4_net_debt_to_equity created')