#!/usr/bin/python
print('0 checks - initiated')

import os
import pandas as pd

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
temp_folder = "temp"
prices_temp = "prices"
financials_a_temp = "financials_a"
financials_q_temp = "financials_q"
other_temp = "other"

# check folder 0_input
if not os.path.exists(os.path.join(cwd,input_folder)):
    os.mkdir(os.path.join(cwd,input_folder))
    print("folder 0_input created")
else:
    print("good! folder 0_input already exists")

# check temp folder
if not os.path.exists(os.path.join(cwd,input_folder,temp_folder)):
    os.mkdir(os.path.join(cwd,input_folder,temp_folder))
    print("temp folder created")
else:
    print("temp folder exists")

# check temp subfolders
if not os.path.exists(os.path.join(cwd,input_folder,temp_folder, prices_temp)):
    os.mkdir(os.path.join(cwd,input_folder,temp_folder, prices_temp))
    os.mkdir(os.path.join(cwd, input_folder, temp_folder, financials_a_temp))
    os.mkdir(os.path.join(cwd, input_folder, temp_folder, financials_q_temp))
    os.mkdir(os.path.join(cwd, input_folder, temp_folder, other_temp))
    print("temp subfolders created")
else:
    print("temp subfolders exist")

# check drop list tickers
if not os.path.exists(os.path.join(cwd,"0_drop_list.xlsx")):
    drop_list = pd.DataFrame({
        'symbol': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'industry': ['Biotechnology', 'Shell Companies', 'Banks—Regional', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'country': ['US', 'DE', 'GB', 'FR', 0, 0
            , 0, 'CH', 'TW', 'AT', 'NL', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                             })
    drop_list.to_excel(os.path.join(cwd,"0_drop_list.xlsx"))
    print("drop_list created")
else:
    print("good! drop_list already exists")

# check last_ticker
if not os.path.exists(os.path.join(cwd,input_folder,temp_folder,"prices_last_ticker.csv")):
    prices_last_ticker = pd.DataFrame({'number': [0] })
    prices_last_ticker.to_csv(os.path.join(cwd,input_folder,temp_folder,"prices_last_ticker.csv"))
    print("prices_last_ticker created")

    prices_last_ticker = pd.DataFrame({'number': [0] })
    prices_last_ticker.to_csv(os.path.join(cwd,input_folder,temp_folder,"prices_last_ticker_filtered.csv"))
    print("prices_last_ticker_filtered created")

    financials_a_last_ticker = pd.DataFrame({'number': [0] })
    financials_a_last_ticker.to_csv(os.path.join(cwd,input_folder,temp_folder,"financials_a_last_ticker.csv"))
    print("financials_a_last_ticker created")

    financials_q_last_ticker = pd.DataFrame({'number': [0] })
    financials_q_last_ticker.to_csv(os.path.join(cwd,input_folder,temp_folder,"financials_q_last_ticker.csv"))
    print("financials_q_last_ticker created")

    financials_q_last_ticker = pd.DataFrame({'number': [0] })
    financials_q_last_ticker.to_csv(os.path.join(cwd,input_folder,temp_folder,"other_last_ticker.csv"))
    print("other_last_ticker created")
else:
    print("good! last_ticker already exists")

# check api_token
if not os.path.exists(os.path.join(cwd,"0_api_token.csv")):
    api_token = pd.DataFrame({'api_token': [0] })
    api_token.to_csv(os.path.join(cwd,"0_api_token.csv"))
    print("api_token created - please fill in real api token")
else:
    print("good! api token already exists")

# check meta file
if not os.path.exists(os.path.join(cwd,"0_symbols.csv")):
    api_token_df = pd.read_csv(os.path.join(cwd,"0_api_token.csv"))
    api_token = api_token_df.iloc[0,1]
    url1 = "https://fmpcloud.io/api/v3/financial-statement-symbol-lists?datatype=csv&apikey="
    url_symbols = url1 + api_token
    df = pd.read_csv(url_symbols)
    df.to_csv(os.path.join(cwd, "0_symbols.csv"))
    print("symbols downloaded if you put your api token")
else:
    print("good! symbols already exist")

print(cwd, '<<< working directory')
print('0 checks - done')
