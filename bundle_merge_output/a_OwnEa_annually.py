#!/usr/bin/python

print('OwnEa annually - initiating.')

import os
import pandas as pd

pd.options.mode.chained_assignment = None
pd.set_option('use_inf_as_na', True)

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"

# import
financials_a = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_a.csv")
                           , parse_dates =["date"]
                           , low_memory=False)
#financials_a = financials_a[(financials_a['symbol'].str.contains('AAPL|MSFT'))]

# find recent q and a, merge and fix missing values in q from a, then calculate EV, and yearly price diffs5
recent_a = financials_a.sort_values(['symbol','date'], ascending=[False, True])
main_fin = recent_a[['symbol', 'date', 'revenue', 'propertyPlantEquipmentNet', 'netCashProvidedByOperatingActivites']]
PPE_Sales = main_fin[['symbol', 'revenue', 'propertyPlantEquipmentNet', 'netCashProvidedByOperatingActivites']].rolling(5, on='symbol', min_periods=0).sum(numeric_only=True)
PPE_Sales.rename(columns={'revenue': 'revenue_5', 'propertyPlantEquipmentNet': 'PPE_5'}, inplace=True)
PPE_Sales.drop(['symbol','netCashProvidedByOperatingActivites'], axis=1, inplace=True)
df_roll5 = pd.concat([main_fin,PPE_Sales],axis=1)
df_roll5['maint_capex_ratio']=df_roll5['PPE_5'] / df_roll5['revenue_5']
df_roll5['Capex'] = recent_a['capitalExpenditure']
df_roll5 = df_roll5.sort_values(['symbol','date'], ascending=[True, False])
df_roll5['Sales_diff'] = df_roll5['revenue'] - df_roll5['revenue'].shift(-1) #get diff in sales p.a.
df_roll5.loc[df_roll5.groupby('symbol').tail(1).index, 'Sales_diff'] = 0.0 #fix first year of every symbol
df_roll5['maint_capex'] = df_roll5['Sales_diff'] * df_roll5['maint_capex_ratio'] * -1
#df_roll5.loc[df_roll5['maint_capex'] < df_roll5['Capex'], 'maint_capex'] = df_roll5['Capex']
df_roll5['OwnEa_a'] = df_roll5['netCashProvidedByOperatingActivites'] + df_roll5['maint_capex']

# export maint_capex_ratio and OwnEa
df_maint_capex_ratio_temp = df_roll5.groupby('symbol').head(1).drop_duplicates(['symbol'], keep='first')
df_maint_capex_ratio = df_maint_capex_ratio_temp[['symbol', 'maint_capex_ratio', 'date']]
df_OwnEa_temp = df_roll5.groupby('symbol').sum().reset_index()
df_OwnEa = df_OwnEa_temp[['symbol', 'OwnEa_a']]
df_merged = pd.merge(df_OwnEa, df_maint_capex_ratio, how='left', left_on=['symbol'], right_on=['symbol'])

# export
df = df_merged
df.to_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa_a.csv"), index = False)

print('4_recent_OwnEa_a created')




