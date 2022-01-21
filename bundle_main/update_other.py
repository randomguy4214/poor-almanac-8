#!/usr/bin/python
print('other - initiating.')

import os
import pandas as pd
import datetime
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"
temp_other = "other"

#setting up fmpcloud
#https://fmpcloud.io/api/v3/profile/AAPL?datatype=csv&apikey=
token_df = pd.read_csv(os.path.join(cwd,"0_api_token.csv"))
token = token_df.iloc[0,1]
url1 = "https://fmpcloud.io/api/v3/profile/"
apikey = "apikey="
amp = "&"
csv = "?datatype=csv"

# prepare tickers list
tickers_narrowed = pd.read_csv(os.path.join(cwd,"0_symbols.csv"))
ticker_narrowed = tickers_narrowed.values.tolist()
tickers = ' '.join(tickers_narrowed["symbol"].astype(str)).strip()

# find last updated ticker (this is necessary if you lose internet connection, etc)
last_ticker = pd.read_csv(os.path.join(cwd,input_folder,temp_folder,"other_last_ticker.csv"),index_col=0)
last_ticker_n = last_ticker.values[0]
last_ticker_nn = last_ticker_n[0]
print("last ticker in other was number", last_ticker_nn)

# start importing
index_max = pd.to_numeric(tickers_narrowed.index.values.max())
for t in tickers.split(' '):
    try:
        n = pd.to_numeric(tickers_narrowed["symbol"][tickers_narrowed["symbol"] == t].index).values
        if n > last_ticker_nn:
            final_url = url1 + t + csv + amp + apikey + token
            df = pd.read_csv(final_url)
            df['symbol'] = t
            name = t + ".csv"
            df.to_csv(os.path.join(cwd, input_folder, temp_folder, temp_other, name))
            # print & export last_n
            nn = n[0] # get number out of numpy.array
            nnn = round(nn/index_max*100,1)
            print("prices:", t, "/" ,nn, "from", index_max, "/", nnn, "%")
            last_ticker = pd.DataFrame({'number':n})
            last_ticker.to_csv(os.path.join(cwd, input_folder, temp_folder, "other_last_ticker.csv"))
    except:
        pass

prices_last_ticker = pd.DataFrame({'number': [0] })
prices_last_ticker.to_csv(os.path.join(cwd,input_folder,temp_folder,"other_last_ticker.csv"))

print('other - done')
