#!/usr/bin/python
print('process_financials_q - initiating.')
import os
import pandas as pd
from pathlib import Path
import datetime as dt

cwd = os.getcwd()
input_folder = "0_input"
temp_folder = "temp"
financials_temp = "financials_q"

#check year to filter out zombie companies
todays_date = dt.date.today()
curr_year = todays_date.year
two_years_ago = curr_year - 2

paths = Path(os.path.join(cwd,input_folder,temp_folder,financials_temp)).glob('**/*.csv')
financials_table = []
for path in paths:
    path_in_str = str(path)
    try:
        fundamentals_parse = pd.read_csv(path,low_memory=False)
        fundamentals_parse['recent_year_check'] = fundamentals_parse['calendarYear'] >= two_years_ago
        if fundamentals_parse['recent_year_check'].sum() >= 1:
            fundamentals_parse = fundamentals_parse[(fundamentals_parse['calendarYear'] >= two_years_ago)]
            if not fundamentals_parse.empty:
                financials_table.append(fundamentals_parse)
                print(path_in_str)
            else:
                pass
        else:
            pass
    except:
        pass

# export
financials_table = pd.concat(financials_table)
financials_table.drop_duplicates()
financials_table = financials_table.iloc[: , 1:]
financials_table.to_csv(os.path.join(cwd,input_folder,"3_processed_financials_q.csv"), index=False)
# export tickers
stocks = financials_table[['symbol']].astype(str).drop_duplicates()
stocks = stocks.sort_values(by=['symbol'], ascending= True)
stocks.to_csv(os.path.join(cwd,input_folder,"3_symbols_financials_q.csv"), index = False)
# export column
df_columns=pd.DataFrame(financials_table.columns.T)
df_columns.to_excel(os.path.join(cwd,input_folder,'3_columns_financials_q.xlsx'))

print('process_financials_q - processed')

