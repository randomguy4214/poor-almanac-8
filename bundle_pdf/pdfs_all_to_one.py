#!/usr/bin/python
print('merging all pdfs by category')

import os
import pandas as pd
import sys
from PyPDF2 import PdfFileMerger, PdfFileReader
from pathlib import Path
import subprocess

pd.options.mode.chained_assignment = None  # default='warn'
pd.options.mode.use_inf_as_na = True

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts_all"
plots_final_folder = "5_plots_final"

df_other = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_other.csv"), usecols = ['symbol','description', 'country', 'industry'], low_memory=False)
df_other.fillna('nan', inplace=True)
tickers_narrowed = pd.read_csv(os.path.join(cwd,"0_symbols_original.csv"))
df_merged = pd.merge(tickers_narrowed, df_other, how='left', left_on=['symbol'], right_on=['symbol'],suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
useless_industries = 'asset management|shell|biotechnology|banks|capital markets|credit|REIT'
df_merged_reduced = df_merged[~df_merged['industry'].str.contains(useless_industries, case=False, na=False)]
#df_merged_reduced.to_csv(os.path.join(cwd, 'test_df_merged_reduced.csv'), index=False)
#df_symbols = df_merged.reset_index(drop=True)
df_symbols = df_merged_reduced[['symbol','industry']]
df_symbols = df_symbols.reset_index(drop=False)
df_industries = df_merged_reduced['industry']
df_industries = df_industries.fillna('nan').sort_values().drop_duplicates().reset_index(drop=True)
#df_industries.rename(columns={df_industries.columns[0]: 'industry'},inplace=True)
#print(df_industries)
#df_industries.to_csv(os.path.join(cwd, 'test_df_industries_redu.csv'))
#sys.exit()

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
        if pdf_name not in df_symbols['symbol'].values:
            #print(pdf_name)
            #print(df_symbols['symbol'].values)
            try:
                merger.append(PdfFileReader(open(path_in_str, 'rb')))
                #print(path_in_str)
            except:
                pass
    except:
        pass

#save to one large pdf
pdf_batch = '0_non_stock.pdf'
merger.write(os.path.join(cwd,plots_final_folder,pdf_batch))
merger.close()

#compress
path_in_str = str(os.path.join(cwd,plots_final_folder,pdf_batch))
path_to_compressor = Path(os.path.join('C:\\Program Files (x86)\\4dots Software\\4dots Free PDF Compress'))
cmd = [
    '4dotsFreePDFCompress.exe'
    , path_in_str
    , '/quality:15'
    , '/overwrite'
]
p = subprocess.run(cmd, cwd=path_to_compressor, shell=True)
#print(pdf_batch + ' compressed')
print('non-stock added')


# 1 take all asset industries
# 2 take all stocks within that industry
# 3 for each stock add to pdf
# 4 save each industry pdf separately

for j in range(0, df_industries.index[-1]+1):
    merger = PdfFileMerger()
    industry_str = str(df_industries[j])
    industry_str_pdf = industry_str + '.pdf'
    for i in range(0, df_symbols.index[-1]+1):
        # if symbol has same industry
        ticker_str = str(df_symbols['symbol'][i])
        industry_str_internal = str(df_symbols['industry'][i])
        if industry_str == industry_str_internal:
            ticker_str_pdf = ticker_str + '.pdf'
            path = Path(os.path.join(cwd,input_folder,charts_folder,ticker_str_pdf))
            path_in_str = str(path)
            if os.path.isfile(path):
                merger.append(PdfFileReader(open(path_in_str, 'rb')))
        else:
            pass
    #save to one large pdf
    merger.write(os.path.join(cwd,plots_final_folder,industry_str_pdf))
    merger.close()

    # compress
    path_in_str = str(os.path.join(cwd, plots_final_folder, industry_str_pdf))
    path_to_compressor = Path(os.path.join('C:\\Program Files (x86)\\4dots Software\\4dots Free PDF Compress'))
    cmd = [
        '4dotsFreePDFCompress.exe'
        , path_in_str
        , '/quality:15'
        , '/overwrite'
    ]
    p = subprocess.run(cmd, cwd=path_to_compressor, shell=True)
    #print(industry_str_pdf + ' compressed')
    print(industry_str + ' added')

