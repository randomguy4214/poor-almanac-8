#!/usr/bin/python

import os
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
symbols = pd.read_csv(os.path.join(cwd,"6_notes.csv"), low_memory=False)
output_unfiltered = pd.read_excel(os.path.join(cwd,"5_df_output_unflitered.xlsx"))
df_merged = pd.merge(symbols, output_unfiltered
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_to_merge = df_merged
dataset_merged = pd.read_csv(os.path.join(cwd,input_folder,"4_merged.csv"), low_memory=False)
df_merged = pd.merge(df_to_merge, dataset_merged
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged.to_excel(os.path.join(cwd,'6_notes_processed.xlsx'))

