#!/usr/bin/python
print('financials_process_annually - initiating.')
import os
import pandas as pd
cwd = os.getcwd()
input_folder = "0_input"
temp_folder = "temp"
financials_temp = "financials_annually"
from pathlib import Path
paths = Path(os.path.join(cwd,input_folder,temp_folder,financials_temp)).glob('**/*.csv')
financials_table = []
for path in paths:
    path_in_str = str(path)
    try:
        fundamentals_parse = pd.read_csv(path,low_memory=False)
        if not fundamentals_parse.empty:
            financials_table.append(fundamentals_parse)
            print(path_in_str)
        else:
            pass
    except:
        pass

# export
financials_table = pd.concat(financials_table)
financials_table.drop_duplicates()
financials_table.to_csv(os.path.join(cwd,input_folder,"3_fundamentals_processed.csv"), index=False)
financials_table.to_excel(os.path.join(cwd,input_folder,"3_fundamentals_processed.xlsx"))
# export tickers
stocks = financials_table[['symbol']].astype(str).drop_duplicates()
stocks = stocks.sort_values(by=['symbol'], ascending= True)
stocks.to_csv(os.path.join(cwd,input_folder,"2_tickers_fundamentals.csv"), index = False)
# export column
df_columns=pd.DataFrame(financials_table.columns.T)
df_columns.to_excel(os.path.join(cwd,input_folder,'3_fundamentals_columns_annually.xlsx'))

print('financials_process_annually - done')

