#!/usr/bin/python
print('copying updated plots to all plots')

import os
import shutil
from pathlib import Path

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
plots_folder = "5_charts"
plots_folder_all = "5_charts_all"

# check charts_folder
if not os.path.exists(os.path.join(cwd,input_folder, plots_folder)):
    pass # check if plots folder exists
else:
    if not os.path.exists(os.path.join(cwd,input_folder, plots_folder_all)):
        pass # check if plots_all folder exists
    else:
        paths = Path(os.path.join(cwd, input_folder, plots_folder)).glob('**/*.pdf')
        for path in paths:
            try:
                # https://towardsdatascience.com/copy-files-python-ad17998264db
                target_folder = os.path.join(cwd, input_folder, plots_folder_all)
                shutil.copy2(path, target_folder)
            except:
                pass
