#!/usr/bin/python
import os
from pathlib import Path
import sys
import subprocess

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts_all"
charts_folder_compr = '5_charts_compr'

# first loop through non-stock pdfs
paths = Path(os.path.join(cwd,input_folder,charts_folder)).glob('**/*.pdf')
for path in paths:
        try:
                path_in_str = str(path)
                path_to_folder_only = os.path.join(cwd, input_folder, charts_folder)
                name_path_reduced_one = path_in_str.replace(path_to_folder_only, '')
                name_path_reduced_two = name_path_reduced_one.replace('_compr', '')
                name_path_reduced_three = name_path_reduced_two.replace('.pdf', '')
                name_df = name_path_reduced_three.split('\\')
                pdf_name = name_df[1] + '.pdf'
                wrong_name = name_df[1] + '_compr.pdf'
                wrong_path = Path(os.path.join(cwd, input_folder, charts_folder, wrong_name))
                correct_path = Path(os.path.join(cwd, input_folder, charts_folder, pdf_name))
                if os.path.isfile(path):
                        os.rename(wrong_path, correct_path)
                else:
                        print(wrong_path)
        except:
                pass