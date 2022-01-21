#!/usr/bin/python
print('process_prices - initiating.')
import os
import pandas as pd

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"
prices_temp = "prices"

from pathlib import Path
paths = Path(os.path.join(cwd,input_folder,temp_folder,prices_temp)).glob('**/*.csv')
prices_table = []
for path in paths:
    path_in_str = str(path)
    try:
        tickers_parse = pd.read_csv(path,low_memory=False)
        if tickers_parse.size > 10:
            prices_table.append(tickers_parse)
            print(path_in_str)
        else:
            pass
    except:
        pass

# export everything
prices_table = pd.concat(prices_table)
prices_table.drop_duplicates()
prices_table.to_csv(os.path.join(cwd,input_folder,"2_process_prices.csv"), index=False)
print('process_prices - done')