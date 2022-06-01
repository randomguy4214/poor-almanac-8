#!/usr/bin/python
print('creating folder for all plots')

import os
import shutil

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts"
charts_folder_all = "5_charts_all"

# check charts_folder
if not os.path.exists(os.path.join(cwd,input_folder, charts_folder)):
    pass
else:
    if not os.path.exists(os.path.join(cwd,input_folder, charts_folder_all)):
        shutil.copytree(os.path.join(cwd,input_folder, charts_folder), os.path.join(cwd,input_folder, charts_folder_all))
    else:
        pass
