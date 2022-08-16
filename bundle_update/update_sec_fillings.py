#!/usr/bin/python
print('update_sec_fillings - initiating.')

import os
import pandas as pd
import shutil
from sec_edgar_downloader import Downloader

cwd = os.getcwd()
input_folder = "0_input"
temp_folder = "temp"
sec_fillings_folder = "5_sec_fillings"

# check sec_fillings folder
if not os.path.exists(os.path.join(cwd, sec_fillings_folder)):
    os.mkdir(os.path.join(cwd, sec_fillings_folder))

# set up downloader
dl = Downloader(os.path.join(cwd, sec_fillings_folder))

# prepare tickers list
tickers_narrowed = pd.read_csv(os.path.join(cwd,"0_symbols.csv"))
ticker_narrowed = tickers_narrowed.values.tolist()
tickers = ' '.join(tickers_narrowed["symbol"].astype(str)).strip()


# start importing
index_max = pd.to_numeric(tickers_narrowed.index.values.max())
for t in tickers.split(' '):
    try:
        #print(os.path.join(cwd, sec_fillings_folder))
        # check ticker folder
        if not os.path.exists(os.path.join(cwd, sec_fillings_folder, t)):
            os.mkdir(os.path.join(cwd, sec_fillings_folder, t))

        # download
        dl.get("10-K", t, amount=5)
        dl.get("10-Q", t, amount=5)
        dl.get("8-K", t, amount=10, include_amends=True)

        print('downloading SEC fillings: ' + t)
    except:
        pass