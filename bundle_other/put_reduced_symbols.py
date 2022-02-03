#!/usr/bin/python

import os
import pandas as pd
import datetime
pd.options.mode.chained_assignment = None  # default='warn'

cwd = os.getcwd()
input_folder = "0_input"

df_other = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_other.csv"), low_memory=False)
other_country = df_other.sort_values(['symbol','country'])
other_filtered_by_country = other_country[other_country['country'].str.contains("US|DE|FR|NL|GB|SK")]

financials_q = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_q.csv"), low_memory=False)
financials_q_latest = financials_q.sort_values(['symbol','date'], ascending=False).groupby('symbol').head(1)

df_merged = pd.merge(other_filtered_by_country, financials_q_latest
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))

df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)

latest_dates = df_merged[['symbol', 'date']]
latest_dates['today'] = datetime.datetime.now()
latest_dates['today'] = pd.to_datetime(latest_dates['today'], errors='coerce').dt.date
latest_dates['date'] = pd.to_datetime(latest_dates['date'], errors='coerce').dt.date
latest_dates['date_diff'] = (latest_dates['date'] - latest_dates['today']).dt.days *-1
print(latest_dates)
latest_dates['date_diff'] = latest_dates['date_diff'].astype(int).fillna(0)
latest_dates = latest_dates[(latest_dates['date_diff'] > 40) & (latest_dates['date_diff'] < 366)]

symbol_list = latest_dates['symbol']

symbol_list.to_csv(os.path.join(cwd,"0_symbols.csv"))
