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
#https://fmpcloud.io/api/v3/quote/AAPL?datatype=csv&timeseries=255&apikey=
token_df = pd.read_csv(os.path.join(cwd,"0_api_token.csv"))
token = token_df.iloc[0,1]
url1 = "https://fmpcloud.io/api/v3/quote/"
apikey = "apikey="
amp = "&"
csv = "?datatype=csv"

# prepare tickers list
df_tickers = pd.read_csv(os.path.join(cwd,"0_symbols.csv"), index_col=0)
df_tickers.drop_duplicates(inplace=True)

# find last updated ticker (this is necessary if you lose internet connection, etc)
prices_last_ticker = pd.read_csv(os.path.join(cwd,input_folder,temp_folder,"prices_last_ticker.csv"),index_col=0)
last_ticker = prices_last_ticker.values[0]
last_ticker_n = last_ticker[0]
print("last batch in prices was", last_ticker_n)

# start importing
index_max = pd.to_numeric(df_tickers.index.values.max())
chunk_size = 50
for i in range(last_ticker_n, len(df_tickers), chunk_size):
    try:
        df_chunk = df_tickers[i:i + chunk_size]
        index_last = pd.to_numeric(df_chunk.index.values.max())
        tickers_narrowed = df_chunk.values.tolist()
        tickers = ','.join(df_chunk["symbol"].astype(str)).strip()
        final_url = url1 + tickers + csv + amp + apikey + token
        df = pd.read_csv(final_url)
        df.set_index('symbol', drop=True, inplace=True)
        output_string = 'df_quotes_' + str(index_last) + '.csv'
        df.to_csv(os.path.join(cwd,input_folder,temp_folder,prices_temp,output_string))
        # print & export last_n
        nnn = int(index_last/index_max*100)
        print("prices:", index_last, "from", index_max, "/", nnn, "%")
        last_ticker = pd.DataFrame([{'number':index_last}])
        last_ticker.to_csv(os.path.join(cwd, input_folder, temp_folder, "prices_last_ticker.csv"))
        time.sleep(5)
    except:
        pass

last_ticker = pd.DataFrame({'number':[0]})
last_ticker.to_csv(os.path.join(cwd,input_folder,temp_folder,"prices_last_ticker.csv"))
print('update_prices - done')