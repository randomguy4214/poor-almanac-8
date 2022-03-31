#!/usr/bin/python

import os
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
pd.options.mode.use_inf_as_na = True


# set directories and files
cwd = os.getcwd()
input_folder = "0_input"

# import files
df_other = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_other.csv"), low_memory=False)
df_prices_EV = pd.read_csv(os.path.join(cwd,input_folder,"4_recent_EV_prices_diff.csv"), low_memory=False)
df_OwnEa = pd.read_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa_all.csv"), low_memory=False)
df_Net_Debt_To_Equity = pd.read_csv(os.path.join(cwd,input_folder,"4_net_debt_to_equity.csv"), low_memory=False)

df_merged = pd.merge(df_prices_EV, df_OwnEa
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_to_merge = df_merged
df_merged = pd.merge(df_to_merge, df_other
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_to_merge = df_merged
df_merged = pd.merge(df_to_merge, df_Net_Debt_To_Equity
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged.reset_index(inplace=True)
#
df = df_merged[['symbol','price','EV'
    ,'from_low','from_high','OwnEa', 'OwnEa_eight_q_avg'
    ,'name','industry','description'
    ,'country','isFund','isEtf', 'marketCap', 'netDebtToEquity']]
df['SO'] = df['marketCap'] / df['price']
df['EV/OwnEa_c'] = df['EV'] / df['OwnEa']
#df.dropna(subset=['EV/OwnEa'], inplace=True)
#df = df[(df['symbol'].str.contains('AGRX'))] # for testing |

# simple model
df['dcf_perp'] = df['OwnEa_eight_q_avg'] * 4 / 0.1 / df['SO']

# advanced model
df['5y_g'] = 1.1
df['FV_1'] = df['OwnEa_eight_q_avg'] * 4
df['FV_2'] = df['FV_1'] * np.power((df['5y_g']),2)
df['FV_3'] = df['FV_1'] * np.power((df['5y_g']),3)
df['FV_4'] = df['FV_1'] * np.power((df['5y_g']),4)
df['FV_5'] = df['FV_1'] * np.power((df['5y_g']),5)

df['TV_g'] = 0.036 #on 2022 march
df['TV'] = (df['FV_5'] * df['5y_g']) / (df['5y_g'] -df['TV_g'])

df['disc'] = 1.1
df['PV'] = (df['FV_1'] / df['disc'] + df['FV_2'] / np.power(df['disc'],2) \
       + df['FV_3'] / np.power(df['disc'],3) + df['FV_4'] / np.power(df['disc'],4) \
       + df['FV_5'] / np.power(df['disc'],5) + df['TV'] / np.power(df['disc'],5)).round(0)
df['dcf_5y_perp'] = (df['PV'] / df['SO']).round(0)

# diff to price
df['marg_of_saf_perp'] = ((df['dcf_perp']- df['price']) / df['price'] * 100).round(0)
df['marg_of_saf_5y_perp'] = ((df['dcf_5y_perp'] - df['price']) / df['price'] * 100).round(0)

# clean
df.drop(['disc', '5y_g', 'FV_1', 'FV_2', 'FV_3', 'FV_4', 'FV_5', 'TV_g', 'TV'], axis=1, inplace=True)

# sort and export unfiltered
output_raw = '5_df_output_unflitered.xlsx'
df.to_excel(os.path.join(cwd,output_raw), index=False)

print('please check the results')