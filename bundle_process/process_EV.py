#!/usr/bin/python
print('process_EV - initiating.')
import os
import pandas as pd

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"
EV = "EV"

from pathlib import Path
paths = Path(os.path.join(cwd,input_folder,temp_folder,EV)).glob('**/*.csv')
table = []
for path in paths:
    path_in_str = str(path)
    try:
        tickers_parse = pd.read_csv(path,low_memory=False)
        if tickers_parse.size > 10:
            table.append(tickers_parse)
            print(path_in_str)
        else:
            pass
    except:
        pass

# export everything
table = pd.concat(table)
table.drop_duplicates()
table = table.iloc[: , 1:]
table.to_csv(os.path.join(cwd,input_folder,"3_processed_EV_q.csv"), index=False)
print('process_EV - done')