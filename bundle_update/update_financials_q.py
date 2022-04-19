#!/usr/bin/python
print('financials_q - initiating')

import os
import pandas as pd
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"
prices_temp = "prices"
financials_temp = "financials_q"

#https://fmpcloud.io/api/v3/balance-sheet-statement-shorten/AAPL?datatype=csv&apikey=
token_df = pd.read_csv(os.path.join(cwd,"0_api_token.csv"))
token = token_df.iloc[0,1]
url1 = "https://financialmodelingprep.com/api/v3/"
inc_st = "income-statement-shorten/"
bs_st = "balance-sheet-statement-shorten/"
cf_st = "cash-flow-statement-shorten/"
apikey = "apikey="
amp = "&"
period_q = "period=quarter"
csv = "?datatype=csv"
timeseries = "timeseries="

# prepare tickers list
tickers_narrowed = pd.read_csv(os.path.join(cwd,"0_symbols.csv"))
ticker_narrowed = tickers_narrowed.values.tolist()
tickers = ' '.join(tickers_narrowed["symbol"].astype(str)).strip()

# find last updated ticker (this is necessary if you lose internet connection, etc)
last_ticker = pd.read_csv(os.path.join(cwd,input_folder,temp_folder,"financials_q_last_ticker.csv"),index_col=0)
last_ticker_n = last_ticker.values[0]
last_ticker_nn = last_ticker_n[0]
print("last ticker in financials_q was number ", last_ticker_nn)

# start importing
index_max = pd.to_numeric(tickers_narrowed.index.values.max())
for t in tickers.split(' '):
    try:
        n = pd.to_numeric(tickers_narrowed["symbol"][tickers_narrowed["symbol"] == t].index).values
        if n >= last_ticker_n:
            inc = url1 + inc_st + t + csv + amp + period_q + amp + apikey + token
            bs = url1 + bs_st + t + csv + amp + period_q + amp + apikey + token
            cf = url1 + cf_st + t + csv + amp + period_q + amp + apikey + token
            #print(inc)
            df_inc = pd.read_csv(inc)
            df_bs = pd.read_csv(bs)
            df_cf = pd.read_csv(cf)

            df_merged = pd.merge(df_inc, df_bs, how='left', left_on=['calendarYear', 'period']
                                 , right_on=['calendarYear', 'period'],
                                 suffixes=('', '_drop'))
            df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
            df_to_merge = df_merged
            df_merged = pd.merge(df_to_merge, df_cf, how='left', left_on=['calendarYear', 'period']
                                 , right_on=['calendarYear', 'period'],
                                 suffixes=('', '_drop'))
            df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
            df = df_merged
            df['symbol'] = t

            name = t + ".csv"
            df.to_csv(os.path.join(cwd, input_folder, temp_folder, financials_temp, name))
            # print & export last_n
            nn = n[0] # get number out of numpy.array
            nnn = round(nn/index_max*100,1)
            print("fundamentals_q:", t, "/" ,nn, "from", index_max, "/", nnn, "%")
            financials_last_ticker = pd.DataFrame({'number': n})
            financials_last_ticker.to_csv(os.path.join(cwd, input_folder, temp_folder, "financials_q_last_ticker.csv"))
    except:
        pass

financials_last_ticker = pd.DataFrame({'number': [0]})
financials_last_ticker.to_csv(os.path.join(cwd, input_folder, temp_folder, "financials_q_last_ticker.csv"))

print('financials_q - done')
