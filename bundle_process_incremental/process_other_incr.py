#!/usr/bin/python
print('process_other_incr - initiating.')
import os
import pandas as pd
from pathlib import Path

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"
other = "other"

# only updated tickers
reduced_symbols = pd.read_csv(os.path.join(cwd,'0_symbols.csv'), low_memory=False, index_col=0)

table = []
for s in reduced_symbols['symbol']:
    paths = Path(os.path.join(cwd,input_folder,temp_folder,other)).glob('**/*.csv')
    for path in paths:
        path_in_str = str(path)
        path_to_folder_only = os.path.join(cwd,input_folder,temp_folder,other)
        name_path_reduced_one = path_in_str.replace(path_to_folder_only, '')
        name_path_reduced_two = name_path_reduced_one.replace('.csv', '')
        name_df = name_path_reduced_two.split('\\')
        csv_name = name_df[1]
        if str(csv_name) == str(s):
            try:
                tickers_parse = pd.read_csv(path,low_memory=False)
                if not tickers_parse.empty:
                    table.append(tickers_parse)
                    #print(path_in_str)
                else:
                    pass
            except:
                pass
        else:
            pass

# concat tables
table = pd.concat(table, axis=0, ignore_index=True)
table.drop_duplicates()
table = table.iloc[: , 1:]

# load old table
table_old = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_other.csv"),low_memory=False)

# concat, clean up, save
df_append = [table, table_old]
df_all = pd.concat(df_append, ignore_index=True, sort=False, axis=0)
df_all.drop_duplicates(subset=['symbol'], inplace=True)

df_all.to_csv(os.path.join(cwd,input_folder,"3_processed_other.csv"), index=False)
print('process_other_incr - done')