#!/usr/bin/python
print('creating folder for plots')

import os
import shutil

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts"
plots_final_folder = "5_plots_final"

# check charts_folder
if not os.path.exists(os.path.join(cwd,input_folder, charts_folder)):
    os.mkdir(os.path.join(cwd,input_folder, charts_folder))
else:
    shutil.rmtree(os.path.join(cwd,input_folder, charts_folder))
    os.mkdir(os.path.join(cwd,input_folder, charts_folder))

# check charts_folder_final
if not os.path.exists(os.path.join(cwd, plots_final_folder)):
    os.mkdir(os.path.join(cwd, plots_final_folder))
else:
    shutil.rmtree(os.path.join(cwd, plots_final_folder))
    os.mkdir(os.path.join(cwd, plots_final_folder))


# copy 00_Research_Description.pdf
#try:
#    research_pdf = '00_Research_description.pdf'
#    shutil.copy(os.path.join(cwd,research_pdf),os.path.join(cwd,input_folder,charts_folder))
#except:
#    pass