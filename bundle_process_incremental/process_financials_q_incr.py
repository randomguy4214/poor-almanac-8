#!/usr/bin/python
print('process_financials_q_incr - initiating..')
import os
import sys
import pandas as pd
from pathlib import Path

cwd = os.getcwd()
input_folder = "0_input"
temp_folder = "temp"
financials_temp = "financials_q"

# only updated tickers
reduced_symbols = pd.read_csv(os.path.join(cwd,'0_symbols.csv'), low_memory=False, index_col=0)
financials_table = []
for s in reduced_symbols['symbol']:
    paths = Path(os.path.join(cwd,input_folder,temp_folder,financials_temp)).glob('**/*.csv')
    for path in paths:
        path_in_str = str(path)
        path_to_folder_only = os.path.join(cwd,input_folder,temp_folder,financials_temp)
        name_path_reduced_one = path_in_str.replace(path_to_folder_only, '')
        name_path_reduced_two = name_path_reduced_one.replace('.csv', '')
        name_df = name_path_reduced_two.split('\\')
        csv_name = name_df[1]
        if str(csv_name) == str(s):
            try:
                fundamentals_parse = pd.read_csv(path, low_memory=False)
                if not fundamentals_parse.empty:
                    financials_table.append(fundamentals_parse)
                    print(path_in_str)
                else:
                    pass
            except:
                pass
        else:
            pass

# concat selected tables
financials_table = pd.concat(financials_table, axis=0, ignore_index=True)
financials_table.drop_duplicates()
financials_table = financials_table.iloc[: , 1:]

# load main table with all data
financials_table_old = pd.read_csv(os.path.join(cwd,input_folder,'3_processed_financials_q.csv'), low_memory=False)

# concat, clean up, save
df_append = [financials_table, financials_table_old]
df_financials_all = pd.concat(df_append, ignore_index=True, sort=False, axis=0)
df_financials_all = df_financials_all\
    .sort_values(['symbol','fillingDate'], ascending=[True, False])\
    .drop_duplicates(['symbol','fillingDate'])
df_financials_all.reset_index(drop=True, inplace=True)

# export
df_financials_all.to_csv(os.path.join(cwd,input_folder,"3_processed_financials_q.csv"), index=False)

# export tickers
stocks = df_financials_all[['symbol']].astype(str).drop_duplicates()
stocks = stocks.sort_values(by=['symbol'], ascending= True)
stocks.to_csv(os.path.join(cwd,input_folder,"3_symbols_financials_q.csv"), index = False)
# export column
df_columns=pd.DataFrame(df_financials_all.columns.T)
df_columns.to_excel(os.path.join(cwd,input_folder,'3_columns_financials_q.xlsx'))

print('financials_q_incr - processed')