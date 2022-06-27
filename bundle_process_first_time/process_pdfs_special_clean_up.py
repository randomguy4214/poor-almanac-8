#!/usr/bin/python
print('deleting unnecessary plots')

import os
from pathlib import Path
import sys
import pandas as pd
import subprocess

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts_all"

df_other = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_other.csv")
                   , usecols = ['symbol','description', 'country', 'industry'], low_memory=False)
tickers_narrowed = pd.read_csv(os.path.join(cwd,"0_symbols.csv"))
df_merged = pd.merge(tickers_narrowed, df_other, how='left', left_on=['symbol'], right_on=['symbol'],
                     suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)

useless_industries = 'asset management|shell|biotechnology|banks|capital markets|credit|REIT'
df_merged_reduced = df_merged[df_merged['industry'].str.contains(useless_industries, case=False, na=False)]
#df_merged_reduced.to_csv(os.path.join(cwd, 'test_df_merged_reduced.csv'), index=False)
#sys.exit()
df_symbols = df_merged_reduced['symbol']
df_symbols = df_symbols.reset_index(drop=False)
for i in range(0, df_symbols.index[-1]+1):
    ticker_str = str(df_symbols['symbol'][i])
    ticker_str_pdf = ticker_str + '.pdf'
    path = Path(os.path.join(cwd,input_folder,charts_folder,ticker_str_pdf))
    if os.path.isfile(path):
        os.remove(path)
        print(ticker_str + ' deleted')
    else:
        pass
        #sys.exit()