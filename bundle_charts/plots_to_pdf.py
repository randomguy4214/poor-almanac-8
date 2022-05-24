#!/usr/bin/python
print('merging pdfs')

import os
import pandas as pd
import PyPDF2
import sys
from pathlib import Path

pd.options.mode.chained_assignment = None  # default='warn'
pd.options.mode.use_inf_as_na = True

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts"

# Create a new PdfFileWriter object which represents a blank PDF document
pdf_write_object = PyPDF2.PdfFileWriter()

#https://stackoverflow.com/questions/48732680/merge-multiple-pdfs-using-pypdf2-module-using-for-loop
# Loop-open pdfs
paths = Path(os.path.join(cwd,input_folder,charts_folder)).glob('**/*.pdf')
for path in paths:
    path_in_str = str(path)
    try:
        pdf_read_object = PyPDF2.PdfFileReader(open(path, 'rb'))
        for page in range(pdf_read_object.numPages):
            pdf_write_object.addPage(pdf_read_object.getPage(page))
            #print('processing file : ' + 'number of pages : ' + str(pdf_read_object.numPages))
    except:
        pass

#sys.exit()

# Now that you have copied all the pages in both the documents, write them into a new document
Charts = '5_Charts.pdf'
pdfOutputFile = open(os.path.join(cwd,Charts), 'wb')
pdf_write_object.write(pdfOutputFile)
pdfOutputFile.close()
