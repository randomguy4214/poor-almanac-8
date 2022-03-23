#!/usr/bin/python

print('OwnEa - initiating.')

import os
import pandas as pd

pd.options.mode.chained_assignment = None
pd.set_option('use_inf_as_na', True)

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"

# import
recent_OwnEa_a = pd.read_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa_a.csv"), usecols=['symbol','OwnEa'], low_memory=False)
recent_OwnEa_q = pd.read_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa_q.csv"), usecols=['symbol','OwnEa'], low_memory=False)

recent_OwnEa = recent_OwnEa_a.append(recent_OwnEa_q)
recent_OwnEa = recent_OwnEa.groupby('symbol').sum().reset_index()

recent_OwnEa.to_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa.csv"), index = False)
print('4_recent_OwnEa created')