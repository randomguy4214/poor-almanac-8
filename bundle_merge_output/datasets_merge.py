#!/usr/bin/python

print('datasets_merge - initiating.')

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
prices_table = pd.read_csv(os.path.join(cwd,input_folder,"2_processed_prices.csv"), low_memory=False)
financials_a = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_a.csv"), low_memory=False)
financials_q = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_q.csv"), low_memory=False)
other_table = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_other.csv"), low_memory=False)

# select only latest year and last X years
financials_a_latest = financials_a.sort_values(['symbol','date'], ascending=False).groupby('symbol').head(1)
financials_a_X = financials_a.sort_values(['symbol','date'], ascending=False).groupby('symbol').head(5)

# historical calc
financials_mean = financials_a_X.groupby(['symbol'])[['revenue'
                        , 'capitalExpenditure', 'costOfRevenue'
                        , 'propertyPlantEquipmentNet']].mean()
financials_mean.rename(columns={'revenue': 'mean_revenue'
                       , 'capitalExpenditures': 'mean_capex'
                       , 'costOfRevenue': 'mean_costOfRevenue'
                       , 'propertyPlantEquipmentNet': 'mean_PPEnet'}
                       , inplace=True)

# merge annual latest and mean
df_merged = pd.merge(financials_a_latest, financials_mean
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_annual_current_mean = df_merged

# merge prices
df_merged = pd.merge(df_annual_current_mean, prices_table
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged.rename(columns={'yearHigh': '52h'
    , 'yearLow': '52l'
    , 'price': 'p'}, inplace=True)
df_annual_current_mean_prices = df_merged

# calculate annual minus one
financials_a_minus_one = financials_a.sort_values(['symbol','date']
                        , ascending=False).groupby('symbol').head(2).drop_duplicates(['symbol'], keep='last')
financials_a_minus_one.rename(columns={'revenue': 'revenue_minus_one_y'
                        , 'cashAndCashEquivalents': 'cashAndCashEquivalents_minus_one_y'
                        , 'deferredRevenue':'deferredRevenue_minus_one_y'
                        , 'operatingExpenses':'operatingExpenses_minus_one_y'
                        , 'totalStockholdersEquity' : 'totalStockholdersEquity_minus_one_y'
                        , 'totalCurrentAssets':'totalCurrentAssets_minus_one_y'
                        , 'totalCurrentLiabilities':'totalCurrentLiabilities_minus_one_y'
                        , 'netDebt':'netDebt_minus_one_y'
                        , 'netCashProvidedByOperatingActivites': 'ncfo_minus_one_y'
                        , 'totalLiabilities': 'totalLiabilities_minus_one_y'
                                  }
                        , inplace=True)
# merge annual minus one
df_merged = pd.merge(df_annual_current_mean_prices, financials_a_minus_one
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_annual_current_mean_prices_minus_one = df_merged

# calculate 2 years ago YoY
financials_a_minus_two = financials_a.sort_values(['symbol','date']
                        , ascending=False).groupby('symbol').head(3).drop_duplicates(['symbol'], keep='last')
financials_a_minus_two.rename(columns={'revenue': 'revenue_minus_two_y'
                        , 'cashAndCashEquivalents':'cashAndCashEquivalents_minus_two_y'
                        , 'deferredRevenue':'deferredRevenue_minus_two_y'
                        , 'operatingExpenses':'operatingExpenses_minus_two_y'
                        , 'totalStockholdersEquity' : 'totalStockholdersEquity_minus_two_y'
                        , 'totalCurrentAssets':'totalCurrentAssets_minus_two_y'
                        , 'totalCurrentLiabilities':'totalCurrentLiabilities_minus_two_y'
                        , 'netDebt':'netDebt_minus_one_y'
                        , 'netCashProvidedByOperatingActivites': 'ncfo_minus_two_y'
                        , 'totalLiabilities': 'totalLiabilities_minus_two_y'
                                  }
                        , inplace=True)
# merge annual minus two
df_merged = pd.merge(df_annual_current_mean_prices_minus_one, financials_a_minus_two
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_annual_current_mean_prices_minus_one_two = df_merged

# prepare last quarter
financials_q_last = financials_q.sort_values(['symbol','date'], ascending=False).groupby('symbol').head(1)
financials_q_last.rename(columns={'revenue': 'revenue_last_q'
                        , 'cashAndCashEquivalents':'cashAndCashEquivalents_last_q'
                        , 'deferredRevenue':'deferredRevenue_last_q'
                        , 'operatingExpenses':'operatingExpenses_last_q'
                        , 'totalStockholdersEquity' : 'totalStockholdersEquity_last_q'
                        , 'totalCurrentAssets':'totalCurrentAssets_last_q'
                        , 'totalCurrentLiabilities':'totalCurrentLiabilities_last_q'
                        , 'totalDebt':'totalDebt_last_q'
                        , 'netDebt':'netDebt_last_q'
                        , 'netCashProvidedByOperatingActivites': 'netCashProvidedByOperatingActivites_last_q'
                        , 'totalLiabilities': 'totalLiabilities_last_q'
                                  }
                        , inplace=True)

# prepare last minus one quarter
financials_q_minus_one = financials_q.sort_values(['symbol','date']
                        , ascending=False).groupby('symbol').head(2).drop_duplicates(['symbol'], keep='last')
financials_q_minus_one.rename(columns={'revenue': 'revenue_minus_one_q'
                        , 'cashAndCashEquivalents':'cashAndCashEquivalents_minus_one_q'
                        , 'deferredRevenue':'deferredRevenue_minus_one_q'
                        , 'operatingExpenses':'operatingExpenses_minus_one_q'
                        , 'totalStockholdersEquity' : 'totalStockholdersEquity_minus_one_q'
                        , 'totalCurrentAssets':'totalCurrentAssets_minus_one_q'
                        , 'totalCurrentLiabilities':'totalCurrentLiabilities_minus_one_q'
                        , 'totalDebt':'totalDebt_minus_one_q'
                        , 'netDebt':'netDebt_minus_one_q'
                        , 'netCashProvidedByOperatingActivites': 'ncfo_minus_one_q'
                        , 'totalLiabilities': 'totalLiabilities_minus_one_q'
                                       }
                        , inplace=True)

# merg current quarter to previous quarter
df_merged = pd.merge(financials_q_last, financials_q_minus_one
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_q_last_and_minus_one = df_merged

# prepare last minus two quarter
financials_q_minus_two = financials_q.sort_values(['symbol','date']
                        , ascending=False).groupby('symbol').head(3).drop_duplicates(['symbol'], keep='last')
financials_q_minus_two.rename(columns={'revenue': 'revenue_minus_two_q'
                        , 'deferredRevenue':'deferredRevenue_minus_two_q'
                        , 'operatingExpenses':'operatingExpenses_minus_two_q'
                        , 'totalStockholdersEquity' : 'totalStockholdersEquity_minus_two_q'
                        , 'totalCurrentAssets':'totalCurrentAssets_minus_two_q'
                        , 'totalCurrentLiabilities':'totalCurrentLiabilities_minus_two_q'
                        , 'netDebt':'netDebt_minus_two_q'
                        , 'netCashProvidedByOperatingActivites': 'ncfo_minus_two_q'
                        , 'totalLiabilities': 'totalLiabilities_minus_two_q'
                                       }
                        , inplace=True)

# merge current, previous, and minus two quarters
df_merged = pd.merge(df_q_last_and_minus_one, financials_q_minus_two
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_quarters = df_merged

# merge annual, mean and quarters
df_merged = pd.merge(df_annual_current_mean_prices_minus_one_two, df_quarters
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_annual_quarters_mean_prices = df_merged

# calculate TTM
financials_TTM = financials_q.sort_values(['symbol','date'], ascending=False).groupby('symbol').head(4)
financials_TTM_sum = financials_TTM.groupby(['symbol']).sum()
financials_TTM_sum.rename(columns={'revenue': 'revenue_TTM'
                        , 'netCashProvidedByOperatingActivites': 'ncfo_TTM'
                        , 'capitalExpenditure': 'capex_TTM'}
                        , inplace=True)

# merge all with TTM
df_merged = pd.merge(df_annual_quarters_mean_prices, financials_TTM_sum
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_annual_quarters_mean_prices_TTM = df_merged

# merge all with other
df_merged = pd.merge(df_annual_quarters_mean_prices_TTM, other_table
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_annual_quarters_mean_prices_TTM_other = df_merged

#
#
#
df = df_annual_quarters_mean_prices_TTM_other
#
#
#

# adding variables

# deferred revenues
df['booking_y'] = df['deferredRevenue'] - df['deferredRevenue_minus_one_y']
df['booking_minus_one_y'] = df['deferredRevenue_minus_one_y'] - df['deferredRevenue_minus_two_y']
df['rev_plus_booking_y'] = df['revenue'] + df['booking_y']
df['rev_plus_booking_minus_one_y'] = df['revenue_minus_one_y'] + df['booking_minus_one_y']
df['booking_q'] = df['deferredRevenue_last_q'] - df['deferredRevenue_minus_one_q']
df['booking_minus_one_q'] = df['deferredRevenue_minus_one_q'] - df['deferredRevenue_minus_two_q']
df['rev_plus_booking_q'] = df['revenue_last_q'] + df['booking_q']
df['rev_plus_booking_minus_one_q'] = df['revenue_minus_one_q'] + df['booking_minus_one_q']

# growth
df['ImplYoYRev'] = ((df['revenue'] - df['revenue_minus_one_y']) / df['revenue_minus_one_y'].abs() - 1 )* 100
df['ImplYoYncfo'] = ((df['netCashProvidedByOperatingActivites'] - df['ncfo_minus_one_y']) / df['ncfo_minus_one_y'].abs() -1 )* 100
df['ImplYoYRevBooking'] = ((df['rev_plus_booking_y'] - df['rev_plus_booking_minus_one_y']) / df['rev_plus_booking_minus_one_y'].abs() - 1 )* 100
df['ImplQoQRev'] = ((df['revenue_last_q'] - df['revenue_minus_one_q']) / df['revenue_minus_one_q'].abs() - 1 )* 100
df['ImplQoQncfo'] = ((df['netCashProvidedByOperatingActivites_last_q'] - df['ncfo_minus_one_q']) / df['ncfo_minus_one_q'].abs() - 1 )* 100
df['ImplQoQRevBooking'] = ((df['rev_plus_booking_q'] - df['rev_plus_booking_minus_one_q']) / df['rev_plus_booking_minus_one_q'].abs() - 1 )* 100
# growth fix
df['ImplQoQRev'] = df['ImplQoQRev'].fillna(df['ImplYoYRev'] / 4)
df['ImplQoQRevBooking'] = df['ImplQoQRevBooking'].fillna(df['ImplYoYRevBooking'] / 4)
df['ImplQoQncfo'] = df['ImplQoQncfo'].fillna(df['ImplYoYncfo'] / 4)

# price
df['from_low'] = (df_merged['p'] - df_merged['52l']) / df_merged['52l'] * 100
df.loc[(df['from_low'] < 0), 'from_low'] = 0
df['from_high'] = (df_merged['p'] - df_merged['52h']) / df_merged['52h'] * 100

# margins
df['mean_OpMarg'] = ((df['mean_revenue'] - df['mean_costOfRevenue']) / df['mean_revenue'].abs() -1) * 100
df['marg_TTM'] = ((df['revenue_TTM'] - df['operatingExpenses_last_q']) / df['revenue_TTM'].abs() -1)  * 100

# capex
df['Sales_absolute_increase'] = df['revenue_TTM'] - df['revenue']
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

# Net Current Asset Value (NCAV) = Total Current Assets - Total Liabilities
df['NCAV'] = df['totalCurrentAssets_last_q'] - df['totalLiabilities_last_q']
df['NCAV/S/p'] = df['NCAV'] / df['sharesOutstanding'] / df['p']

# Enterprise value
df['EV_last_q'] = df['marketCap'] + df['totalDebt_last_q'] - df['cashAndCashEquivalents_last_q']
df['EV_last_q'] = df['EV_last_q'].fillna(df['marketCap'] + df['totalDebt'] - df['cashAndCashEquivalents'])
df['EV/S/p'] = df['EV_last_q'] / df['sharesOutstanding'] / df['p']

print('variables calculated')

# fixing
cols_to_fillna = [i for i in df.columns]
for col in cols_to_fillna:
    try:
        df[col] = df[col].fillna(0)
        '''
        if col in ['p', 'from_low', 'from_high', 'OpMarg', 'B/S/p', 'marg', 'marCap'
            , 'B/S/p', '52l', '52h', 'ImplYoYRev', 'ImplQoQRev', 'ImplYoYncfo', 'ImplQoQncfo'
            , 'marg_TTM', 'OwnEa/S/p', 'Rev/S/p', 'Eq/D'
            , 'WC/D', 'Eq/D', 'cik']:
            df[col]=df[col].fillna(0)
        else:
            pass
        '''
    except:
        pass

# format
cols_to_format = [i for i in df.columns]
for col in cols_to_format:
    try:
        if col in [
            'p', 'B/S/p', '52l', '52h'
            , 'Eq/D', 'WC/S/p'
            , 'ImplYoYRev', 'ImplQoQRev', 'ImplYoYncfo', 'ImplQoQncfo'
            , 'ImplQoQRevBooking', 'ImplYoYRevBooking'
            , 'EV/S/p', 'NCAV/S/p', 'OwnEa/S/p']:
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

'''
# debug
df.reset_index(drop=False, inplace=True)
df.to_csv(os.path.join(cwd,input_folder,"df.csv"), index = False)
'''