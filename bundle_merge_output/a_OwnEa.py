#!/usr/bin/python

print('OwnEa - initiating.')

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
recent_OwnEa_a = pd.read_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa_a.csv"), usecols=['symbol','OwnEa_a'], low_memory=False)
recent_OwnEa_q = pd.read_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa_q.csv"), usecols=['symbol','OwnEa_q'], low_memory=False)
recent_OwnEa_eight_q = pd.read_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa_OwnEa_q_last_8.csv"), usecols=['symbol','OwnEa_eight_q_avg'], low_memory=False)

recent_OwnEa_a.rename(columns={'symbol': 'symbol', 'OwnEa_a': 'OwnEa'}, inplace=True)
recent_OwnEa_q.rename(columns={'symbol': 'symbol', 'OwnEa_q': 'OwnEa'}, inplace=True)

# append annuals and unprocessed quarters
recent_OwnEa = recent_OwnEa_a.append(recent_OwnEa_q)
recent_OwnEa = recent_OwnEa.groupby('symbol').sum().reset_index()

# add as a separate column last 8 quarters
df_merged = pd.merge(recent_OwnEa, recent_OwnEa_eight_q
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'])

recent_OwnEa_all = df_merged
recent_OwnEa_all.to_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa_all.csv"), index = False)
print('4_recent_OwnEa_all created')