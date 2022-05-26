#!/usr/bin/python
print('FED Balance Sheet - initiating')

import os
import pandas as pd
import requests

cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"

### prepare dataframe
# latest pdf report - https://www.federalreserve.gov/releases/H41/current/h41.pdf
url_to_FED_BS = 'https://www.federalreserve.gov/datadownload/Output.aspx?rel=H41&series=f99fa10ab98aa7f22c00e5333c7628f5&lastobs=1000&from=&to=&filetype=csv&label=include&layout=seriescolumn'

# https://stackoverflow.com/questions/51092889/receiving-http-error-403-forbidden-csv-download
storage_options = {'User-Agent': 'Mozilla/5.0'}
df_FED_BS_all = pd.read_csv(url_to_FED_BS, storage_options=storage_options)

# clean a bit
df = df_FED_BS_all[df_FED_BS_all.columns.drop(list(df_FED_BS_all.filter(regex='Memorandum')))]
df.columns = df.columns.str.replace(": Wednesday level", "")
rows_to_drop = [0,1,2,3,4]
df = df.drop(df.index[rows_to_drop])
df = df.rename(columns={df.columns[0]: 'Date'})
df.set_index('Date', inplace=True, drop=True)
df = df.apply(pd.to_numeric, errors='coerce').astype('int64')
#df['Equity'] = -1 * (df['Assets: Total Assets: Total assets (Less eliminations from consolidation)'] - df['Liabilities and Capital: Liabilities: Total liabilities'])

list_to_drop = [
        'Assets: Other: Repurchase agreements: Maturing within 15 days'
        , 'Assets: Securities Held Outright: U.S. Treasury securities: Notes and bonds'
        , 'Assets: Securities Held Outright: Securities held outright'
        , 'Assets: Securities Held Outright: Mortgage-backed securities'
        , 'Assets: Total Assets: Total assets (Less eliminations from consolidation)'
        , 'Liabilities and Capital: Liabilities: Deposits (Less eliminations from consolidation)'
        , 'Liabilities and Capital: Liabilities: Deposits'
        , 'Liabilities and Capital: Liabilities: Deposits with F.R. Banks, other than reserve balances: Term deposits held by depository institutions'
        , 'Liabilities and Capital: Liabilities: Deposits: Other deposits held by depository institutions'
        , 'Liabilities and Capital: Liabilities: Deposits: Other'
        , 'Liabilities and Capital: Liabilities: Reverse repurchase agreements'
        , 'Liabilities and Capital: Liabilities: Reverse repurchase agreements: Others'
        , 'Liabilities and Capital: Liabilities: Reverse repurchase agreements: Foreign official and international accounts'
        , 'Liabilities and Capital: Liabilities: Federal Reserve notes outstanding'
        , 'Liabilities and Capital: Liabilities: Total liabilities'
        ]

df.drop(list_to_drop, axis=1, inplace=True)
df.loc[:, df.columns.str.contains('Liabilities')] = df * -1
df.columns = df.columns.str.replace("Assets: Central Bank Liquidity Swaps: ", "")
df.columns = df.columns.str.replace("Maturing within : ", "")
df.columns = df.columns.str.replace("Maturing in : ", "")
df.columns = df.columns.str.replace("Assets: Securities Held Outright: ", "")
df.columns = df.columns.str.replace("Assets: Other: ", "")
df.columns = df.columns.str.replace("Mortgage-backed securities:", "MBS")
df.columns = df.columns.str.replace("Liabilities and Capital: ", "")

df = df.sort_index(axis=1) # sort columns


df.to_csv(os.path.join(cwd,input_folder,"2_processed_BS_FED.csv"))
#print(df)