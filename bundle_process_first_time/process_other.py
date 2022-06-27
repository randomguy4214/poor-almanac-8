#!/usr/bin/python
print('process_other - initiating.')
import os
import pandas as pd

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"
other = "other"

from pathlib import Path
paths = Path(os.path.join(cwd,input_folder,temp_folder,other)).glob('**/*.csv')
table = []
for path in paths:
    path_in_str = str(path)
    try:
        tickers_parse = pd.read_csv(path,low_memory=False)
        if tickers_parse.size > 10:
            table.append(tickers_parse)
            #print(path_in_str)
        else:
            pass
    except:
        pass

# export everything
df_all = pd.concat(table)
df_all['industry'] = df_all['industry'].astype(str)
df_all["companyName"] = df_all["companyName"].astype(str)
df_all['industry'] = df_all['industry'].str.replace('?',' - ', regex=True)
ass_mng_list = 'amundi|invesco|venture|xtrackers|dividen|etf|trust|fund|Growth Opportunities|aberdeen|advisorShares|%|secured|proshares|holdings|alliance|equity|minishares|VelocityShares|REIT|warrant|investment|acquisition|wisdomtree|investors|lazard|ubs|acquisition corp|vanguard|Allianz|financial|capital|blackrock|citigroup'
df_all.loc[(df_all["industry"]=='nan') & (df_all["companyName"].str.contains(ass_mng_list, case=False, na=False)), 'industry'] = 'Asset Management'

df_all.drop_duplicates()
df_all = df_all.iloc[: , 1:]
df_all.to_csv(os.path.join(cwd,input_folder,"3_processed_other.csv"), index=False)
print('process_other - done')