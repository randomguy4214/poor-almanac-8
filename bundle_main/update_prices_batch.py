#!/usr/bin/python
print('update_prices - initiating.')

import os
import pandas as pd
import datetime
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"
prices_temp = "prices"

#setting up fmpcloud
#https://fmpcloud.io/api/v3/quote/AAPL,FB,MSFT?datatype=csv&apikey=0e983500cc3b679486c5fff4119a236d
token_df = pd.read_csv(os.path.join(cwd,"0_api_token.csv"))
token = token_df.iloc[0,1]
url1 = "https://fmpcloud.io/api/v3/quote/"
apikey = "apikey="
amp = "&"
csv = "?datatype=csv"

# prepare tickers list
tickers_narrowed = pd.read_csv(os.path.join(cwd,"0_symbols.csv"))
ticker_narrowed = tickers_narrowed.values.tolist()
tickers = ','.join(tickers_narrowed["symbol"].astype(str)).strip()

final_url = url1 + tickers + csv + amp + apikey + token
df = pd.read_csv(final_url)
name = "prices" + ".csv"
df.to_csv(os.path.join(cwd, input_folder, temp_folder, prices_temp, name))


print('update_prices - done')
