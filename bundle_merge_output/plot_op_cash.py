#!/usr/bin/python
print('drawing charts with operating cash')

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import sys

# figure size in inches
rcParams['figure.figsize'] = 11.7,8.27

pd.options.mode.chained_assignment = None  # default='warn'
pd.options.mode.use_inf_as_na = True

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts"

# import files
df_5_symbols_marg_of_safety = pd.read_csv(os.path.join(cwd,input_folder,"5_symbols_marg_of_safety.csv"), low_memory=False)
df_q = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_q.csv")
                   , usecols = ['symbol','date', 'grossProfitRatio', 'operatingCashFlow', 'calendarYear', 'period']
                   , low_memory=False)
df_merged = pd.merge(df_5_symbols_marg_of_safety, df_q
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
#df = df_merged
#df = df_merged.head(3000)
df = df_merged.groupby('symbol').head(80).reset_index(drop=True) # selecting only 20 years per symbol

#df = df_merged[(df_merged['symbol'].str.contains('SKM|SPWH|RBB'))]
df = df[df['operatingCashFlow'].notna()]
df = df[df['date'].notna()]
df = df[df['calendarYear'].notna()]
df['calendarYear'] = df['calendarYear'].astype(int)
df['marg_of_saf_perp'] = df['marg_of_saf_perp'].round(0)
df['yearQ'] = df['calendarYear'].astype(str) + ' ' + df['period'].astype(str)
df['symbol_marg_of_saf'] = df['symbol'].astype(str) + ' / ' + df['marg_of_saf_perp'].astype(str) + ' %'
df = df.sort_values(['symbol','date'], ascending=[True, True])

# create symbols df
df_symbols = df['symbol'].drop_duplicates()
df_symbols = df_symbols.reset_index(drop=True) # mistery to me

# separate main df by chunk_size tickers and process separately for efficiency
# loop, chart, save pdfs
index_max = pd.to_numeric(df_symbols.index.values.max())
max_chunk_processed = []
chunk_size = 4
for i in range(0, len(df_symbols), chunk_size):
    df_chunk = df_symbols[i:i + chunk_size] # take chunk of unique symbols
    df_chunk = df_chunk.to_frame() #convert from Series to DataFrame
    df_chunk.columns.values[0] = 'symbol'
    df_merged = pd.merge(df_chunk, df
                         , how='left', left_on=['symbol']
                         , right_on=['symbol'], suffixes=('', '_drop'))
    df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
    df_temp = df_merged
    #print(df_temp)
    #sys.exit()

    # plot
    g = sns.catplot(
        x = 'yearQ'
        , y = 'operatingCashFlow'
        , data = df_temp
        , col = 'symbol_marg_of_saf'
        , col_wrap=2 # 2 symbols per line, ie 4 on 1 page
        , kind='bar'
        , aspect = 1.7 #16:9
        , sharey=False #dynamic y-axis
        , sharex=False #dynamic x-axis
        , palette = sns.color_palette('GnBu_d', 4)
        , alpha=.7
        , color = 'blue'
        , ci=None
        )

    # format overall plot
    g.set_xticklabels(rotation=45, size=4)
    g.set_yticklabels(size=5)
    g.set_ylabels('OpCash', size=10, color='gray')
    g.set(xlabel=None)
    g.set_titles("{col_name}", size=10, x=0.9, color='gray')
    plt.subplots_adjust(hspace = 0.3)
    #plt.show()

    # show highest chunk
    max_chunk_processed = i+chunk_size
    #print(max_chunk_processed)

    # save plots as pdf
    output_raw = '1_OpCash_' + str(i+chunk_size) + '.pdf'
    print('OpCash ' + output_raw)
    plt.savefig(os.path.join(cwd, input_folder, charts_folder, output_raw), dpi=300)
    plt.close()

    #sys.exit()