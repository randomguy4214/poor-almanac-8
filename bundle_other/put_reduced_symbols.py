#!/usr/bin/python

import os
import pandas as pd
import datetime
pd.options.mode.chained_assignment = None  # default='warn'

cwd = os.getcwd()
input_folder = "0_input"

df_other = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_other.csv"), low_memory=False)
other_country = df_other.sort_values(['symbol','country'])

drop_list = pd.read_excel(os.path.join(cwd,"0_drop_list.xlsx"))
drop_list_country = drop_list['country'].tolist()
df_export = df_other[df_other['country'].isin(drop_list_country)] # drop some industries
#other_filtered_by_country = other_country[other_country['country'].str.contains("US|DE|FR|NL|GB|SK|CH")]

financials_q = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_q.csv"), low_memory=False)
financials_q_latest = financials_q.sort_values(['symbol','date'], ascending=False).groupby('symbol').head(1)

df_merged = pd.merge(df_export, financials_q_latest
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))

df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)

latest_dates = df_merged[['symbol', 'date']]
latest_dates = latest_dates[(latest_dates['date'].str.len() > 0)]
latest_dates['today'] = datetime.datetime.now()
latest_dates['today'] = pd.to_datetime(latest_dates['today'], errors='coerce').dt.date
latest_dates['date'] = pd.to_datetime(latest_dates['date'], errors='coerce').dt.date
latest_dates['date_diff'] = (latest_dates['date'] - latest_dates['today']).dt.days *-1
latest_dates['date_diff'] = latest_dates['date_diff'].astype(int).fillna(0)
latest_dates = latest_dates[(latest_dates['date_diff'] > 85) & (latest_dates['date_diff'] < 390)]
# financials update once per quarter, ie ca 90 days. to be on a safe side
# and if company doesnt have any financials for one year, it is pretty much a dead company
symbol_list = latest_dates['symbol']
symbol_list.reset_index(drop=True, inplace=True)
symbol_list.to_csv(os.path.join(cwd,"0_symbols.csv"))
