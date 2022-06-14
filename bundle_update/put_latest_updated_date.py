#!/usr/bin/python

import os
import pandas as pd
import datetime
cwd = os.getcwd()
input_folder = "0_input"
temp_folder = 'temp'

today_date = datetime.datetime.now().date().strftime("%Y-%m-%d")

df = pd.DataFrame({'date': [today_date] })
df.to_csv(os.path.join(cwd,input_folder,temp_folder,"latest_date_updated.csv"))