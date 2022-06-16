#!/usr/bin/python
print('reducing pdf size for recently updated tickers')

import os
import pandas as pd
from pathlib import Path
import pdfminify
import sys
import subprocess


pd.options.mode.chained_assignment = None  # default='warn'
pd.options.mode.use_inf_as_na = True

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts"

# first loop through non-stock pdfs
paths = Path(os.path.join(cwd,input_folder,charts_folder)).glob('**/*.pdf')
for path in paths:
    path_in_str = str(path)
    path_to_folder_only = os.path.join(cwd,input_folder,charts_folder)
    name_path_reduced_one = path_in_str.replace(path_to_folder_only, '')
    name_path_reduced_two = name_path_reduced_one.replace('.pdf', '')
    name_df = name_path_reduced_two.split('\\')
    pdf_name = name_df[1]
    #print(path_in_str)
    #p = subprocess.run('pdfminify path_in_str path_in_str', shell=True)
    p = subprocess.run('$path', shell=True)


    sys.exit()

    #pdfminify(path)