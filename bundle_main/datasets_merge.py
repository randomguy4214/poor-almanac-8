#!/usr/bin/python

print('datasets_merge - initiating.')

import os
import pandas as pd
pd.options.mode.chained_assignment = None

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"

# import
prices_table = pd.read_csv(os.path.join(cwd,input_folder,"2_processed_prices.csv"), low_memory=False)
financials_a = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_a.csv"), low_memory=False)
financials_q = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_q.csv"), low_memory=False)
other_table = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_other.csv"), low_memory=False)

# select only latest year and last X years
financials_a_last = financials_a.sort_values(['symbol','date'], ascending=False).groupby('symbol').head(1)
financials_a_X = financials_a.sort_values(['symbol','date'], ascending=False).groupby('symbol').head(5)

# historical calc
financials_a_last.rename(columns={'revenue': 'revenue_last_y'}, inplace=True)
financials_mean = financials_a_X.groupby(['symbol'])[['revenue'
                        , 'capitalExpenditure', 'costOfRevenue'
                        , 'propertyPlantEquipmentNet']].mean()
financials_mean.rename(columns={'revenue': 'mean_revenue'
                       , 'capitalExpenditures': 'mean_capex'
                       , 'costOfRevenue': 'mean_costOfRevenue'
                       , 'propertyPlantEquipmentNet': 'mean_PPEnet'}
                       , inplace=True)
print("historical averages calculated")

# merge last annual financials, and prices
df_merged = pd.merge(financials_a_last, prices_table
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged.rename(columns={'yearHigh': '52h'
    , 'yearLow': '52l'
    , 'price': 'p'}, inplace=True)
df_last_ann_and_prices = df_merged

# calculate YoY
financials_a_minus_one_last = financials_a.sort_values(['symbol','date']
                        , ascending=False).groupby('symbol').head(2).drop_duplicates(['symbol'], keep='last')
financials_a_minus_one_last.rename(columns={'revenue': 'revenue_minus_one_y'
                        , 'operatingExpenses':'operatingExpenses_minus_one_y'
                        , 'totalStockholdersEquity' : 'totalStockholdersEquity_minus_one_y'
                        , 'totalCurrentAssets':'totalCurrentAssets_minus_one_y'
                        , 'totalCurrentLiabilities':'totalCurrentLiabilities_minus_one_y'
                        , 'netDebt':'netDebt_minus_one_y'
                        , 'netCashProvidedByOperatingActivites': 'ncfo_minus_one_y'
                                  }
                        , inplace=True)
# YoY merge
df_merged = pd.merge(df_last_ann_and_prices, financials_a_minus_one_last
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_last_ann_and_prices_and_YoY = df_merged

# merge historical financials
df_merged = pd.merge(df_last_ann_and_prices_and_YoY, financials_mean
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_last_ann_and_prices_and_YoY_and_mean = df_merged

# prepare last quarter
financials_q_last = financials_q.sort_values(['symbol','date'], ascending=False).groupby('symbol').head(1)
financials_q_last.rename(columns={'revenue': 'revenue_last_q'
                        , 'operatingExpenses':'operatingExpenses_last_q'
                        , 'totalStockholdersEquity' : 'totalStockholdersEquity_last_q'
                        , 'totalCurrentAssets':'totalCurrentAssets_last_q'
                        , 'totalCurrentLiabilities':'totalCurrentLiabilities_last_q'
                        , 'netDebt':'netDebt_last_q'
                        , 'netCashProvidedByOperatingActivites': 'netCashProvidedByOperatingActivites_last_q'
                                  }
                        , inplace=True)

# prepare last minus one quarter
financials_q_minus_one_last = financials_q.sort_values(['symbol','date']
                        , ascending=False).groupby('symbol').head(2).drop_duplicates(['symbol'], keep='last')
financials_q_minus_one_last.rename(columns={'revenue': 'revenue_minus_one_q'
                        , 'operatingExpenses':'operatingExpenses_minus_one_q'
                        , 'netCashProvidedByOperatingActivites': 'ncfo_minus_one_q'}
                        , inplace=True)

# calc QoQ growth
df_merged = pd.merge(financials_q_last, financials_q_minus_one_last
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
QoQ = df_merged

# merge all with QoQ
df_merged = pd.merge(df_last_ann_and_prices_and_YoY_and_mean, QoQ
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_last_ann_and_prices_and_YoY_and_mean_and_QQ = df_merged

# calculate TTM
financials_TTM = financials_q.sort_values(['symbol','date'], ascending=False).groupby('symbol').head(4)
financials_TTM_sum = financials_TTM.groupby(['symbol']).sum()
financials_TTM_sum.rename(columns={'revenue': 'revenue_TTM'
                        , 'netCashProvidedByOperatingActivites': 'ncfo_TTM'
                        , 'capitalExpenditure': 'capex_TTM'}
                        , inplace=True)

# merge all with TTM
df_merged = pd.merge(df_last_ann_and_prices_and_YoY_and_mean_and_QQ, financials_TTM_sum
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_last_ann_and_prices_and_YoY_and_mean_and_QQ_and_TTM = df_merged

# merge all with other
df_merged = pd.merge(df_last_ann_and_prices_and_YoY_and_mean_and_QQ_and_TTM, other_table
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_last_ann_and_prices_and_YoY_and_mean_and_QQ_and_TTM_and_other = df_merged

#
#
#
df = df_last_ann_and_prices_and_YoY_and_mean_and_QQ_and_TTM_and_other
#
#
#

# adding variables
# growth
df['ImplYoYRev'] = df['revenue_last_y'] / df['revenue_minus_one_y'] - 1
df['ImplYoYncfo'] = df['netCashProvidedByOperatingActivites'] / df['ncfo_minus_one_y'] - 1
df['ImplQoQRev'] = df['revenue_last_q'] / df['revenue_minus_one_q'] -1
df['ImplQoQncfo'] = df['netCashProvidedByOperatingActivites_last_q'] / df['ncfo_minus_one_q'] - 1

# price
df['from_low'] = (df_merged['p'] - df_merged['52l']) / df_merged['52l'] * 100
df.loc[(df['from_low'] < 0), 'from_low'] = 0
df['from_high'] = (df_merged['p'] - df_merged['52h']) / df_merged['52h'] * 100

# sales
df['mean_OpMarg'] = (df['mean_revenue'] - df['mean_costOfRevenue']) / df['mean_revenue'] * 100
df['marg_TTM'] = (df['revenue_TTM'] - df['operatingExpenses_last_q']) / df['revenue_TTM'] * 100
df['Sales_absolute_increase'] = df['revenue_TTM'] - df['revenue_last_y']

# capex
df['maint_capex_ratio'] = df['mean_PPEnet'] / df['mean_revenue']
df['growth_capex'] = df['maint_capex_ratio'] * df['Sales_absolute_increase']
df['capex_more_correct'] = df['capex_TTM'] - df['growth_capex']
df['capex_more_correct'] = df['capex_more_correct'].fillna(df['capex_TTM'])
df['capex_more_correct'] = df['capex_more_correct'].fillna(df['netCashUsedForInvestingActivites'])

# NAV, B/S/p, OwnEa, WC
df['totalStockholdersEquity_last_q'] = df['totalStockholdersEquity_last_q'].fillna(df['totalStockholdersEquity'])
df['NAV/S'] = df['totalStockholdersEquity_last_q'] / df['sharesOutstanding']
df['B/S/p'] = df['NAV/S'] / df['p']
df['OwnEa'] =  df['ncfo_TTM'] + df['capex_more_correct']
df['OwnEa/S'] = df['OwnEa'] / df['sharesOutstanding']
df['OwnEa/S/p'] = df['OwnEa/S'] / df['p']
df['WC'] =  df['totalCurrentAssets_last_q'] - df['totalCurrentLiabilities_last_q']
df['WC/S'] = df['WC']/ df['sharesOutstanding']
df['WC/S/p'] = df['WC/S'] / df['p']
df['WC/D'] = df['WC'] / df['netDebt_last_q']
df['Eq/D'] = df['totalStockholdersEquity_last_q'] / (df['totalStockholdersEquity_last_q'] + df['netDebt_last_q'])
df['Rev/S/p'] = df['revenue_TTM'] / df['sharesOutstanding'] / df['p']

print('variables calculated')

# fixing
cols_to_fillna = [i for i in df.columns]
for col in cols_to_fillna:
    try:
        if col in ['p', 'from_low', 'from_high', 'OpMarg', 'B/S/p', 'marg', 'marCap'
                   , 'B/S/p', '52l', '52h', 'ImplYoYRev', 'ImplQoQRev', 'ImplYoYncfo', 'ImplQoQncfo']:
            df[col]=df[col].fillna(0)
        else:
            pass
    except:
        pass

df['ImplQoQRev'] = df['ImplQoQRev'].fillna(df['ImplYoYRev'] / 4)

# format
cols_to_format = [i for i in df.columns]
for col in cols_to_format:
    try:
        if col in ['p', 'B/S/p', '52l', '52h', 'ImplYoYRev', 'ImplQoQRev', 'ImplYoYncfo', 'ImplQoQncfo']:
            df[col]=df[col].round(2)
        else:
            df[col] = df[col].round(0)
    except:
        pass
print('formatting is done')

# reorder
cols_to_order = ['symbol', 'p', '52l', '52h', 'from_low', 'from_high']
new_columns = cols_to_order + (df_merged.columns.drop(cols_to_order).tolist())
df_merged = df_merged[new_columns]
print('reordering is done')

#  export
print('export')
df_merged.to_csv(os.path.join(cwd,input_folder,"4_merged.csv"))
#df_merged.to_excel(os.path.join(cwd,input_folder,"4_merged.xlsx"))
# export tickers again. just to have more narrowed result
stocks = df_merged[['symbol']].sort_values(by=['symbol'], ascending= True).drop_duplicates()
stocks.to_csv(os.path.join(cwd,input_folder,"4_tickers_narrowed.csv"), index = False)
print("datasets are merged and exported")

# export column
df_columns=pd.DataFrame(df_merged.columns.T)
df_columns.to_excel(os.path.join(cwd,input_folder,'4_merged_columns.xlsx'))

print('datasets_merge - done')

'''
# debug
df.reset_index(drop=False, inplace=True)
df.to_csv(os.path.join(cwd,input_folder,"df.csv"), index = False)
'''