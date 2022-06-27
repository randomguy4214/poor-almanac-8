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
df_all['industry'] = df_all['industry'].astype(str)
df_all["companyName"] = df_all["companyName"].astype(str)
df_all['industry'] = df_all['industry'].str.replace('?',' - ', regex=True)
ass_mng_list = 'amundi|invesco|venture|xtrackers|dividen|etf|trust|fund|Growth Opportunities|aberdeen|advisorShares|%|secured|proshares|holdings|alliance|equity|minishares|VelocityShares|REIT|warrant|investment|acquisition|wisdomtree|investors|lazard|ubs|acquisition corp|vanguard|Allianz|financial|capital|blackrock|citigroup'
df_all.loc[(df_all["industry"]=='nan') & (df_all["companyName"].str.contains(ass_mng_list, case=False, na=False)), 'industry'] = 'Asset Management'

df_all.drop_duplicates()
df_all = df_all.iloc[: , 1:]
df_all.to_csv(os.path.join(cwd,input_folder,"3_processed_other.csv"), index=False)
print('process_other_incr - done')