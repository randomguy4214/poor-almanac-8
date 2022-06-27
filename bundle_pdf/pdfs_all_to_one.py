#!/usr/bin/python
print('merging pdfs for all companies')

import os
import pandas as pd
import sys
from PyPDF2 import PdfFileMerger, PdfFileReader
from pathlib import Path

pd.options.mode.chained_assignment = None  # default='warn'
pd.options.mode.use_inf_as_na = True

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts_all"

# tickers processed - 5_df_output_unflitered.xlsx, properly sorting them
five_df_output_unflitered = pd.read_excel(os.path.join(cwd,"5_df_output_unflitered.xlsx"), index_col=None)
five_df_output_unflitered = five_df_output_unflitered.sort_values(['country','industry','EV'], ascending=[True, True, False])
df_symbols = five_df_output_unflitered['symbol'].drop_duplicates().reset_index(drop=False).drop(columns='index')

# Create a new PdfFileWriter object which represents a blank PDF document
merger = PdfFileMerger()

# https://stackoverflow.com/questions/17104926/pypdf-merging-multiple-pdf-files-into-one-pdf
# Loop through pdfs and append them to each other
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
        if pdf_name not in df_symbols.values:
            try:
                merger.append(PdfFileReader(open(path_in_str, 'rb')))
                print(path_in_str)
            except:
                pass
    except:
        pass

# now loop only through stock pdf and in a very specific order
for i in range(0, df_symbols.index[-1]+1):
    ticker_str = str(df_symbols['symbol'][i])
    ticker_str_pdf = ticker_str + '.pdf'
    path = Path(os.path.join(cwd,input_folder,charts_folder,ticker_str_pdf))
    path_in_str = str(path)

    if os.path.isfile(path):
        merger.append(PdfFileReader(open(path_in_str, 'rb')))
        print(ticker_str + ' pdf added' + '  ' + df_symbols.index[i] + '/' + df_symbols.index[-1])
        #print(path_in_str)


#save to one large pdf
print('merging...will take a while...')
Charts = '5_Charts_unfiltered.pdf'
merger.write(os.path.join(cwd,Charts))
