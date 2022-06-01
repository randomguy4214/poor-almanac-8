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

# Create a new PdfFileWriter object which represents a blank PDF document
merger = PdfFileMerger()

# https://stackoverflow.com/questions/17104926/pypdf-merging-multiple-pdf-files-into-one-pdf
# Loop through pdfs and append them to each other
paths = Path(os.path.join(cwd,input_folder,charts_folder)).glob('**/*.pdf')
for path in paths:
    try:
        path_in_str = str(path)
        merger.append(PdfFileReader(open(path_in_str, 'rb')))
        print(path_in_str)
    except:
        pass

#save to one large pdf
Charts = '5_Charts_unfiltered.pdf'
merger.write(os.path.join(cwd,Charts))
