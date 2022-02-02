#!/usr/bin/python
print('getting all tickers')
import pandas as pd
import os
cwd = os.getcwd()
df_tickers = pd.read_csv(os.path.join(cwd,"0_symbols_original.csv"), index_col=0)
df_tickers.to_csv(os.path.join(cwd,"0_symbols.csv"))
