#!/usr/bin/python
print('drawing scatter plot')

import warnings
warnings.filterwarnings("ignore")
import os
import shutil

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts"

# check charts_folder
if not os.path.exists(os.path.join(cwd,input_folder, charts_folder)):
    os.mkdir(os.path.join(cwd,input_folder, charts_folder))
else:
    shutil.rmtree(os.path.join(cwd,input_folder, charts_folder))
    os.mkdir(os.path.join(cwd,input_folder, charts_folder))

# copy 00_Research_Description.pdf
try:
    research_pdf = '00_Research_description.pdf'
    shutil.copy(os.path.join(cwd,research_pdf),os.path.join(cwd,input_folder,charts_folder))
except:
    pass