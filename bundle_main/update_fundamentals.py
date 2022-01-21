#!/usr/bin/python
print('financials - initiating')

import os
import pandas as pd
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:20,.2f}'.format
pd.options.mode.use_inf_as_na = True
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"
prices_temp = "prices"
financials_temp = "financials"

#setting up tiingo
api_token_df = pd.read_csv(os.path.join(cwd,"0_api_token.csv"))
api_token = api_token_df.iloc[0,1]
url1 = "https://api.tiingo.com/tiingo/fundamentals/"
url2 = "/statements"
token = "?token="
amp = "&"
csv = "format=csv"

# prepare tickers list
tickers_narrowed = pd.read_csv(os.path.join(cwd,"0_symbols.csv"))
ticker_narrowed = tickers_narrowed.values.tolist()
tickers = ' '.join(tickers_narrowed["symbol"].astype(str)).strip()

# find last updated ticker (this is necessary if you lose internet connection, etc)
last_ticker = pd.read_csv(os.path.join(cwd,input_folder,temp_folder,"financials_last_ticker.csv"),index_col=0)
last_ticker_n = last_ticker.values[0]
last_ticker_nn = last_ticker_n[0]
print("last ticker in financials was number ", last_ticker_nn)

# start importing
index_max = pd.to_numeric(tickers_narrowed.index.values.max())
for t in tickers.split(' '):
    try:
        n = pd.to_numeric(tickers_narrowed["symbol"][tickers_narrowed["symbol"] == t].index).values
        if n > last_ticker_n:
            final_url = url1 + t + url2 + token + api_token + amp + csv
            # https://api.tiingo.com/tiingo/fundamentals/HDALF/statements?token=&format=csv
            df = pd.read_csv(final_url, index_col=['date', 'year', 'quarter'])
            df = df.pivot(columns=['statementType', 'dataCode'])
            df.columns = [' '.join(col).strip() for col in df.columns.values]  # fix column names
            df.columns = df.columns.str.replace("value ", "")
            df['symbol'] = t
            name = t + ".csv"
            df.to_csv(os.path.join(cwd, input_folder, temp_folder, financials_temp, name))
            # print & export last_n
            nn = n[0] # get number out of numpy.array
            nnn = round(nn/index_max*100,1)
            print("fundamentals:", t, "/" ,nn, "from", index_max, "/", nnn, "%")
            financials_last_ticker = pd.DataFrame({'number': n})
            financials_last_ticker.to_csv(os.path.join(cwd, input_folder, temp_folder, "financials_last_ticker.csv"))
    except:
        pass

financials_last_ticker = pd.DataFrame({'number': [0]})
financials_last_ticker.to_csv(os.path.join(cwd, input_folder, temp_folder, "financials_last_ticker.csv"))

print('financials - done')
