#!/usr/bin/python

import os
import pandas as pd
import datetime
cwd = os.getcwd()
input_folder = "0_input"
temp_folder = 'temp'

token_df = pd.read_csv(os.path.join(cwd,"0_api_token.csv"), low_memory=False)
token = token_df.iloc[0,1]
url1 = "https://financialmodelingprep.com/api/v4/"
earn_cal = "earning-calendar-confirmed?"
earn_from = "from="

first_date_df = pd.read_csv(os.path.join(cwd,input_folder,temp_folder,"latest_date_updated.csv"))
#first_date = (datetime.datetime.now() - pd.DateOffset(weeks=1)).date().strftime("%Y-%m-%d")
first_date = first_date_df['date'][0]

print('latest update was on ' + first_date)
earn_to = "to="
today_date = datetime.datetime.now().date().strftime("%Y-%m-%d")
apikey = "apikey="
amp = "&"
csv = "?datatype=csv"

earn_url = url1 + earn_cal + earn_from + first_date + amp + earn_to + today_date + amp + apikey + token
print(earn_url)
#print(earn_url)
df_earn = pd.read_json(earn_url)
symbol_list = df_earn['symbol']
symbol_list.reset_index(drop=True, inplace=True)
symbol_list.to_csv(os.path.join(cwd,"0_symbols.csv"))

