#!/usr/bin/python
print('reducing pdf size for all tickers')

import os
from pathlib import Path
import sys
import subprocess

# set directories and files
cwd = os.getcwd()
charts_folder = "5_plots_final"

# first loop through non-stock pdfs
paths = Path(os.path.join(cwd,charts_folder)).glob('**/*.pdf')
for path in paths:
    try:
        path_in_str = str(path)
        path_to_folder_only = os.path.join(cwd,charts_folder)
        name_path_reduced_one = path_in_str.replace(path_to_folder_only, '')
        name_path_reduced_two = name_path_reduced_one.replace('.pdf', '')
        name_df = name_path_reduced_two.split('\\')
        pdf_name = str(name_df[1])
        pdf_name_pdf = pdf_name + '.pdf'
        #path to 4dots software = 'C:\Program Files (x86)\4dots Software\4dots Free PDF Compress\4dotsFreePDFCompress.exe'
        path_to_compressor = Path(os.path.join('C:\\Program Files (x86)\\4dots Software\\4dots Free PDF Compress'))
        cmd = [
            '4dotsFreePDFCompress.exe'
            , path_in_str
            ,'/quality:15'
            ,'/overwrite'
        ]
        p = subprocess.run(cmd, cwd=path_to_compressor, shell=True)
        print(pdf_name + ' compressed')
    except:
        print('error with ticker in path ' + str(path))