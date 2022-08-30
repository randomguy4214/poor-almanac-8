#!/usr/bin/python
print('cross referencing tickers')
#import warnings
#warnings.filterwarnings("ignore")
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from datetime import datetime
from pathlib import Path
import sys
import subprocess

pd.options.mode.chained_assignment = None  # default='warn'
pd.options.mode.use_inf_as_na = True

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"

# import
tickers_all = pd.read_csv(os.path.join(cwd,"0_symbols_original.csv"), index_col=0)
tickers_all.drop_duplicates(inplace=True)
tickers_all.reset_index(drop=True)
#print(tickers_all)
df_q = pd.read_csv(os.path.join(cwd,input_folder,"3_symbols_financials_q.csv")
                   , usecols = ['symbol']
                   , low_memory=False)
df_q['s_q'] = df_q['symbol']
df_q.drop_duplicates(inplace=True)
df_q.reset_index(drop=True)
#print(df_q)

df_a = pd.read_csv(os.path.join(cwd,input_folder,"3_symbols_financials_a.csv")
                   , usecols = ['symbol']
                   , low_memory=False)
df_a['s_a'] = df_a['symbol']
df_a.drop_duplicates(inplace=True)
df_a.reset_index(drop=True)
#print(df_a)

df_EV_q = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_EV_q.csv")
                   , usecols = ['symbol']
                   , low_memory=False)
df_EV_q['s_EV_q'] = df_EV_q['symbol']
df_EV_q.drop_duplicates(inplace=True)
df_EV_q.reset_index(drop=True)
#print(df_EV_q)

df_other = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_other.csv")
                   , usecols = ['symbol'], low_memory=False)
df_other['s_other'] = df_other['symbol']
df_other.drop_duplicates(inplace=True)
df_other.reset_index(drop=True)
#print(df_other)

# merge
# symbols to quarterly
df_merged = pd.merge(tickers_all, df_q
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_q'))
#df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_to_merge = df_merged.drop_duplicates()
df_to_merge.reset_index(drop=True)
#print(df_to_merge)
# to annually
df_merged = pd.merge(df_to_merge, df_a
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_q'))
#df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_to_merge = df_merged.drop_duplicates()
df_to_merge.reset_index(drop=True)
#print(df_to_merge)
# to EV_q
df_merged = pd.merge(df_to_merge, df_EV_q
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_EV_q'))
#df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_to_merge = df_merged.drop_duplicates()
df_to_merge.reset_index(drop=True)
print(df_to_merge)
# to other
df_merged = pd.merge(df_to_merge, df_other
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_other'))
#df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)

symbols_comparison_xlsx = '3_symbols_comparison.xlsx'
df_merged.to_excel(os.path.join(cwd,input_folder,symbols_comparison_xlsx), index=False)

