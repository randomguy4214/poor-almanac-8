#!/usr/bin/python

import os
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"

# import files
df_prices_EV = pd.read_csv(os.path.join(cwd,input_folder,"4_recent_EV_prices_diff.csv"), low_memory=False)
df_OwnEa = pd.read_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa.csv"), low_memory=False)
df_other = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_other.csv"), low_memory=False)

df_merged = pd.merge(df_prices_EV, df_OwnEa
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_to_merge = df_merged
df_merged = pd.merge(df_to_merge, df_other
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged.reset_index(inplace=True)
#
df = df_merged[['symbol','price','EV'
    ,'from_low','from_high','OwnEa'
    ,'maint_capex_ratio','name','industry','description'
    ,'country','isFund','isEtf']]
df['EV/OwnEa'] = df['EV'] / df['OwnEa']

# sort and export unfiltered
output_raw = '5_df_output_unflitered.xlsx'
df.to_excel(os.path.join(cwd,output_raw), index=False)

print('please check the results')