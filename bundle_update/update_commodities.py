#!/usr/bin/python
print('commodities - initiating')

import os
import pandas as pd

cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"

### prepare dataframe
# https://financialmodelingprep.com/api/v3/symbol/available-commodities?datatype=csv&apikey=24396e170b4c9805ada69a4770ce52b0
# https://thedocs.worldbank.org/en/doc/5d903e848db1d1b83e0ec8f744e55570-0350012021/related/CMO-Historical-Data-Monthly.xlsx
url_to_commodities_from_WorldBank = 'https://thedocs.worldbank.org/en/doc/5d903e848db1d1b83e0ec8f744e55570-0350012021/related/CMO-Historical-Data-Monthly.xlsx'
commodities_df = pd.read_excel(url_to_commodities_from_WorldBank, sheet_name='Monthly Prices', skiprows=4)
labels_df = commodities_df[:1] # read only 2 rows
labels_df_T = labels_df.transpose().reset_index(drop=False) # transpose to prepare
labels_df_T['full_label'] = labels_df_T['index'] + ' ' + labels_df_T[0] # merge columns values
labels_full_df = labels_df_T['full_label'].reset_index(drop=True) # select only new labels
labels_full_df[0:1] = 'Date'
#labels_full_df = labels_full_df.iloc[1:] # delete first unnecessary row
commodities_df.columns = labels_full_df # rename columns to new labels
commodities_df = commodities_df[2:] # delete wrong rows
years_to_consider = 20 * 12 * -1 #-1 is to start counting from the bottom of the data
commodities_df = commodities_df[years_to_consider:]
commodities_df.set_index('Date', drop=True, inplace=True)
commodities_df = commodities_df.apply(pd.to_numeric, errors='coerce').fillna(0) # fix wrong values
#commodities_df = commodities_df.drop(commodities_df.columns[[]], axis=1)
commodities_df.to_csv(os.path.join(cwd,input_folder,"2_processed_commodities.csv"))