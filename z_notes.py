import os
import pandas as pd
cwd = os.getcwd()
input_folder = "0_input"
notes = pd.read_excel(os.path.join(cwd, "z_notes.xlsx"), index_col="symbol")
notes.reset_index(drop=False, inplace=True)
symbols = notes['symbol'].drop_duplicates()
print(symbols)
output_unfiltered = pd.read_excel(os.path.join(cwd,"5_df_output_unflitered.xlsx"))
df_merged = pd.merge(symbols, output_unfiltered
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_to_merge = df_merged
dataset_merged = pd.read_csv(os.path.join(cwd,input_folder,"4_merged.csv"), low_memory=False)
df_merged = pd.merge(df_to_merge, dataset_merged
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged.to_excel(os.path.join(cwd, 'z_notes.xlsx'), index=False)

