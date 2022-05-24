#!/usr/bin/python
print('commodities - initiating')

import os
import pandas as pd
import sys

cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"

# https://financialmodelingprep.com/api/v3/symbol/available-commodities?datatype=csv&apikey=24396e170b4c9805ada69a4770ce52b0