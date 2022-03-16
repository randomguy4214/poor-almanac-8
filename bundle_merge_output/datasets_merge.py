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
EV_table = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_EV.csv"), low_memory=False)

#



# df.reset_index(drop=False, inplace=True)
df.to_csv(os.path.join(cwd,input_folder,"df.csv"), index = False)




'''



# price
df['from_low'] = (df_merged['p'] - df_merged['52l']) / df_merged['52l'] * 100
df.loc[(df['from_low'] < 0), 'from_low'] = 0
df['from_high'] = (df_merged['p'] - df_merged['52h']) / df_merged['52h'] * 100



print('variables calculated')

# fixing
cols_to_fillna = [i for i in df.columns]
for col in cols_to_fillna:
    try:
        df[col] = df[col].fillna(0)
        '''
        if col in ['p', 'from_low', 'from_high', 'OpMarg', 'B/S/p', 'marg', 'marCap'
            , 'B/S/p', '52l', '52h', 'ImplYoYRev', 'ImplQoQRev', 'ImplYoYncfo', 'ImplQoQncfo'
            , 'marg_TTM', 'OwnEa_TTM/S/p', 'Rev/S/p', 'Eq/D'
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
            , 'EV/S/p', 'NCAV/S/p', 'OwnEa_TTM/S/p', 'OwnEa_TTM/EV'
            ,]:
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
df_merged.to_csv(os.path.join(cwd,input_folder,"4_merged.csv"))
#df_merged.to_excel(os.path.join(cwd,input_folder,"4_merged.xlsx"))
# export tickers again. just to have more narrowed result
stocks = df_merged[['symbol']].sort_values(by=['symbol'], ascending= True).drop_duplicates()
stocks.to_csv(os.path.join(cwd,input_folder,"4_tickers_narrowed.csv"), index = False)
print("datasets are merged and exported")

# export column
df_columns=pd.DataFrame(df_merged.columns.T)
df_columns.to_excel(os.path.join(cwd,input_folder,'4_merged_columns.xlsx'))


# debug
df.reset_index(drop=False, inplace=True)
df.to_csv(os.path.join(cwd,input_folder,"df.csv"), index = False)
'''