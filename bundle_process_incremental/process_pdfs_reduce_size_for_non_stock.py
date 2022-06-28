#!/usr/bin/python
print('reducing pdf size for non-stock')

import os
import pandas as pd
from pathlib import Path
import sys
import subprocess


pd.options.mode.chained_assignment = None  # default='warn'
pd.options.mode.use_inf_as_na = True

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts"

# loop through non-stock pdfs
paths = Path(os.path.join(cwd,input_folder,charts_folder)).glob('**/*.pdf')
non_stocks_list = ['commodity','BS_FED','002_SCFI','003_SCFI', '002_WCI', 'scatterplot']
for path in paths:
    path_in_str = str(path)
    if any(item in path_in_str for item in non_stocks_list):
        try:
            # path to 4dots software = 'C:\Program Files (x86)\4dots Software\4dots Free PDF Compress\4dotsFreePDFCompress.exe'
            path_to_compressor = Path(
                os.path.join('C:\\Program Files (x86)\\4dots Software\\4dots Free PDF Compress'))
            cmd = [
                '4dotsFreePDFCompress.exe'
                , path_in_str
                , '/quality:15'
                , '/overwrite'
            ]
            if os.path.isfile(path_in_str):
                p = subprocess.run(cmd, cwd=path_to_compressor, shell=True)
            else:
                pass
        except:
            print('error with ticker in path ' + str(path))
    else:
        pass