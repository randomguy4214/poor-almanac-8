import os
from pathlib import Path

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts_all"

paths = Path(os.path.join(cwd,input_folder,charts_folder)).glob('**/*.pdf')
for path in paths:
    try:
        path_in_str = str(path)
        name_path_reduced_one = path_in_str.replace('0_input','')
        name_path_reduced_two = name_path_reduced_one.replace('5_charts_all','')
        name_df = name_path_reduced_two.split('_')
        #print(name_df[1])
        #print(path_in_str)
        new_path = os.path.join(cwd,input_folder,charts_folder, name_df[1])
        #print(new_path)
        os.rename(path_in_str, new_path)
    except:
        pass