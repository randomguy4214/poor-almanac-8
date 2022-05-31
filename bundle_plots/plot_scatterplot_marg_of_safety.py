#!/usr/bin/python
print('scatterplot - plotting')

import warnings
warnings.filterwarnings("ignore")
import os
import pandas as pd
import numpy as np
import seaborn as sns
sns.set_theme(style='darkgrid')
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys

pd.options.mode.chained_assignment = None  # default='warn'
pd.options.mode.use_inf_as_na = True

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts"


# import files
df_import = pd.read_excel(os.path.join(cwd,"5_df_output_unflitered.xlsx"))
df = df_import[['symbol', 'from_low', 'marg_of_saf_perp', 'marg_of_saf_5y_perp','marketCap_q', 'industry', 'country']]
df_drop_list = pd.read_excel(os.path.join(cwd,"0_drop_list.xlsx"))

# filter the data
df = df[df['country'].isin(df_drop_list['country'])]
df = df[~df['industry'].isin(df_drop_list['industry'])]
df = df[~df['symbol'].isin(df_drop_list['symbol'])]
df = df[df['symbol'].str.contains('.TW')==False]

df = df[df['marg_of_saf_perp'].notna()]
df = df[df['from_low'].notna()]
df = df[df['symbol'].notna()]
#df = df[df['marg_of_saf_perp'] >= 20]
#df = df[df['marg_of_saf_perp'] <= 1000]
#df = df[df['from_low'] <= 50]
#df = df[df['from_low'] >= 0]

# quantiles
df['marg_of_saf_perp_quantile'] = pd.qcut(df['marg_of_saf_perp'], 50, labels=False, duplicates='drop')
df['marg_of_saf_perp_q'] = 50 - df['marg_of_saf_perp_quantile']
df['marg_of_saf_5y_perp_quantile'] = pd.qcut(df['marg_of_saf_5y_perp'], 50, labels=False, duplicates='drop')
df['marg_of_saf_5y_perp_q'] = 50 - df['marg_of_saf_5y_perp_quantile']

# filter on quantile
#df = df[df['marg_of_saf_perp_q'] >= 2] # exclude outliers

# sort data
df = df.sort_values(['country','industry','marg_of_saf_perp'], ascending=[True, True, False])

# export symbols
df_exp = df[['symbol','marg_of_saf_perp']]
df_exp.to_csv(os.path.join(cwd,input_folder,"5_symbols_marg_of_safety.csv"), index = False)

# plot
sns.set(style='darkgrid', color_codes=True,rc = {'figure.figsize':(14, 8.5)})
splot_func = sns.scatterplot(data = df, x = df['marg_of_saf_perp'], y = df['from_low']
                , size = df['marketCap_q']
                , hue = "industry"
                , alpha = 0.4 # transparency
                , legend=False
                #, colorfont = 'gray'
                ) # make scatterplot as variable
splot_func.set(xscale='log', yscale='log')
splot_func.set_yticklabels(splot_func.get_yticks().astype('int64'), size=5, color='gray')
splot_func.set_xticklabels(splot_func.get_xticks().astype('int64'), size=5, color='gray')
splot_func.set_facecolor('black')
splot_func.grid(color='gray', linestyle='--', linewidth=0.7)

# Label data points with a loop
for i in range(df.shape[0]):
        #print(df['symbol'].iloc[i])
        plt.text(x = df['marg_of_saf_perp'].iloc[i]+0.3
                 , y = df['from_low'].iloc[i]+0.3
                 , s = df['symbol'].iloc[i]
                 , fontdict=dict(size=5, color='gray'))
        #fck me that took too long to figure out. iloc is important.

# limits
#plt.xlim(100, )
#plt.ylim(0, 10)
# axes
plt.xlabel('margin of safety', fontsize=8, color='gray')
plt.ylabel('from low', fontsize=8, color='gray')


plt.tight_layout()
output_raw = '010_scatterplot.pdf'
plt.savefig(os.path.join(cwd,input_folder,charts_folder,output_raw), dpi=30, facecolor='black')
plt.close('all')
#sns.set(style='white')
mpl.rc_file_defaults()
#plt.show()
