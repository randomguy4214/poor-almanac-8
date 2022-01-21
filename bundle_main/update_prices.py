#!/usr/bin/python
import sys

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
financials_temp = "financials"

#check year
todays_date = datetime.date.today()
curr_year = todays_date.year
full_year = datetime.timedelta(days = 365)
year_ago = todays_date - full_year
year_ago_str = str(year_ago)

#setting up tiingo
api_token_df = pd.read_csv(os.path.join(cwd,"0_api_token.csv"))
api_token = api_token_df.iloc[0,1]
url1 = "https://api.tiingo.com/tiingo/"
daily_str = "daily/"
prices_str = "/prices"
start_date = "?startDate="
token = "token="
amp = "&"
csv = "format=csv"
fund_str = "fundamentals/"
daily_2_str = "/daily?"
# https://api.tiingo.com/tiingo/fundamentals/aapl/daily?token=&format=csv

# prepare tickers list
tickers_narrowed = pd.read_csv(os.path.join(cwd,"0_symbols.csv"))
ticker_narrowed = tickers_narrowed.values.tolist()
tickers = ' '.join(tickers_narrowed["symbol"].astype(str)).strip()

# find last updated ticker (this is necessary if you lose internet connection, etc)
last_ticker = pd.read_csv(os.path.join(cwd,input_folder,temp_folder,"prices_last_ticker.csv"),index_col=0)
last_ticker_n = last_ticker.values[0]
last_ticker_nn = last_ticker_n[0]
print("last ticker in prices was number", last_ticker_nn)

# start importing
index_max = pd.to_numeric(tickers_narrowed.index.values.max())
for t in tickers.split(' '):
    try:
        n = pd.to_numeric(tickers_narrowed["symbol"][tickers_narrowed["symbol"] == t].index).values
        if n > last_ticker_nn:
            # download marcap
            final_url_2 = url1 + fund_str + t + daily_2_str + token + api_token + amp + csv
            df2 = pd.read_csv(final_url_2)
            # download prices
            final_url = url1 + daily_str + t + prices_str + start_date + year_ago_str + amp + token + api_token + amp + csv
            df = pd.read_csv(final_url)
            # merge & export
            df_merged = pd.merge(df,df2, how='left', left_on=['date'], right_on=['date'], suffixes=('', '_drop'))
            df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
            df_merged['symbol'] = t
            name = t + ".csv"
            df_merged.to_csv(os.path.join(cwd, input_folder, temp_folder, prices_temp, name))
            # print & export last_n
            nn = n[0] # get number out of numpy.array
            nnn = round(nn/index_max*100,1)
            print("prices:", t, "/" ,nn, "from", index_max, "/", nnn, "%")
            last_ticker = pd.DataFrame({'number':n})
            last_ticker.to_csv(os.path.join(cwd, input_folder, temp_folder, "prices_last_ticker.csv"))
    except:
        pass

prices_last_ticker = pd.DataFrame({'number': [0] })
prices_last_ticker.to_csv(os.path.join(cwd,input_folder,temp_folder,"prices_last_ticker.csv"))

print('update_prices - done')
