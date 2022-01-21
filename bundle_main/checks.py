#!/usr/bin/python

print('0 checks - initiated')

import os
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
temp_folder = "temp"
prices_temp = "prices"
financials_temp = "financials"


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

# check temp prices folders
if not os.path.exists(os.path.join(cwd,input_folder,temp_folder, prices_temp)):
    os.mkdir(os.path.join(cwd,input_folder,temp_folder, prices_temp))
    print("temp prices csv folder created")
else:
    print("temp prices csv folder exists")

# check prices and financials folders
if not os.path.exists(os.path.join(cwd, input_folder, temp_folder, financials_temp)):
    os.mkdir(os.path.join(cwd, input_folder, temp_folder, financials_temp))
    print("temp financials csv folder created")
else:
    print("temp financials csv exists")

# check drop list tickers
if not os.path.exists(os.path.join(cwd,"0_drop_list.xlsx")):
    drop_list = pd.DataFrame({
        'symbol': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        'industry': ['Biotechnology', 'Shell Companies', 'Banks—Regional', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        'country': ['United States', 'Germany', 'France', 'United Kingdom', 'Belgium', 'Netherlands Antilles'
            , 'South Korea', 'Switzerland', 'Taiwan', 'Austria', 'Netherlands', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                             })

    drop_list.to_excel(os.path.join(cwd,"0_drop_list.xlsx"))
    print("drop_list created")
else:
    print("good! drop_list already exists")

# check prices_last_ticker
if not os.path.exists(os.path.join(cwd,input_folder,temp_folder,"prices_last_ticker.csv")):
    prices_last_ticker = pd.DataFrame({'number': [0] })
    prices_last_ticker.to_csv(os.path.join(cwd,input_folder,temp_folder,"prices_last_ticker.csv"))
    print("prices_last_ticker created")
else:
    print("good! prices_last_ticker already exists")

# check prices_last_ticker_filtered
if not os.path.exists(os.path.join(cwd,input_folder,temp_folder,"prices_last_ticker_filtered.csv")):
    prices_last_ticker = pd.DataFrame({'number': [0] })
    prices_last_ticker.to_csv(os.path.join(cwd,input_folder,temp_folder,"prices_last_ticker_filtered.csv"))
    print("prices_last_ticker_filtered created")
else:
    print("good! prices_last_ticker_filtered already exists")

# check financials_last_ticker
if not os.path.exists(os.path.join(cwd,input_folder,temp_folder,"financials_last_ticker.csv")):
    financials_quarterly_last_ticker = pd.DataFrame({'number': [0] })
    financials_quarterly_last_ticker.to_csv(os.path.join(cwd,input_folder,temp_folder,"financials_last_ticker.csv"))
    print("financials_last_ticker created")
else:
    print("good! financials_last_ticker already exists")

# check api_token
if not os.path.exists(os.path.join(cwd,"0_api_token.csv")):
    api_token = pd.DataFrame({'api_token': [0] })
    api_token.to_csv(os.path.join(cwd,"0_api_token.csv"))
    print("api_token created - please fill in real api")
else:
    print("good! api_token already exists")

# check meta file
if not os.path.exists(os.path.join(cwd,"0_meta.csv")):
    print("meta not created, please upload")
else:
    print("good! meta data already exists")

print(cwd, '<<< working directory')
print('0 checks - done')
