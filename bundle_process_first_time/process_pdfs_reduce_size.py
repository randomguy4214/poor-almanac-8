#!/usr/bin/python
print('reducing pdf size for all tickers')

import os
from pathlib import Path
import sys
import subprocess

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts_all"

# first loop through non-stock pdfs
paths = Path(os.path.join(cwd,input_folder,charts_folder)).glob('**/*.pdf')
for path in paths:
    try:
        path_in_str = str(path)
        path_to_folder_only = os.path.join(cwd,input_folder,charts_folder)
        name_path_reduced_one = path_in_str.replace(path_to_folder_only, '')
        name_path_reduced_two = name_path_reduced_one.replace('.pdf', '')
        name_df = name_path_reduced_two.split('\\')
        pdf_name = name_df[1]
        compr = 'compr_'
        new_pdf_name = pdf_name + '_compr.pdf'
        new_path = Path(os.path.join(cwd,input_folder,charts_folder, new_pdf_name))
        path_out_str = str(new_path)
        #path to ghostscript = 'C:\Program Files\gs\gs9.56.1\bin'
        path_to_ghostscript = Path(os.path.join('C:\\Program Files\\gs\\gs9.56.1\\bin'))
        cmd = [
            'gswin64c' #no-window mode
            , '-dSAFER'
            , '-dNOPAUSE'
            , '-dBATCH'
            , '-dNoCancel'
            , '-dNOPROMPT'
            , '-q'
            , '-sDEVICE=pdfwrite'
            , '-dPDFSETTINGS=/screen'
            #, '-dNORANGEPAGESIZE'
            #, '-dAutoRotatePages=/All'
            ,'-sOutputFile=' + path_out_str
            ,path_in_str]
        p = subprocess.run(cmd, cwd=path_to_ghostscript, shell=True)
        # delete old file and rename new
        if os.path.isfile(new_path):
            os.remove(path)
            os.rename(new_path, path)
        else:
            print('error on ' + path)
        print(pdf_name + ' compressed')
    except:
        print('error with ticker in path ' + str(path))