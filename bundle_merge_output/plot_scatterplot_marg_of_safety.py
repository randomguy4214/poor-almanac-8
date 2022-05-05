#!/usr/bin/python
print('drawing scatter plot')

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import shutil

pd.options.mode.chained_assignment = None  # default='warn'
pd.options.mode.use_inf_as_na = True


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

# import files
df_import = pd.read_excel(os.path.join(cwd,"5_df_output_unflitered.xlsx"))
df = df_import[['symbol', 'from_low', 'marg_of_saf_perp', 'marg_of_saf_5y_perp','marketCap_q', 'industry']]

# filter the data
df = df[df['marg_of_saf_perp'].notna()]
df = df[df['from_low'].notna()]
df = df[df['symbol'].notna()]
df = df[df['marg_of_saf_perp'] >= 100]
df = df[df['from_low'] <= 10]
df = df[df['from_low'] >= 0]

# quantiles
df['marg_of_saf_perp_quantile'] = pd.qcut(df['marg_of_saf_perp'], 50, labels=False, duplicates='drop')
df['marg_of_saf_perp_q'] = 50 - df['marg_of_saf_perp_quantile']
df['marg_of_saf_5y_perp_quantile'] = pd.qcut(df['marg_of_saf_5y_perp'], 50, labels=False, duplicates='drop')
df['marg_of_saf_5y_perp_q'] = 50 - df['marg_of_saf_5y_perp_quantile']

# filter on quantile
df = df[df['marg_of_saf_perp_q'] >= 2] # exclude outliers

# export symbols
df_exp = df[['symbol','marg_of_saf_perp']]
df_exp.to_csv(os.path.join(cwd,input_folder,"5_symbols_marg_of_safety.csv"), index = False)

# plot
sns.set(style='darkgrid', color_codes=True,rc = {'figure.figsize':(15,8)})
splot_func = sns.scatterplot(data = df, x = df['marg_of_saf_perp'], y = df['from_low'] \
                , size = df['marketCap_q'] \
                , hue = "industry" \
                , alpha = 0.4 # transparency
                , legend=False
                ) # make scatterplot as variable
splot_func.set(xscale='log')

# Label data points with a loop
for i in range(df.shape[0]):
        #print(df['symbol'].iloc[i])
        plt.text(x = df['marg_of_saf_perp'].iloc[i]+0.3, y = df['from_low'].iloc[i]+0.3, s = df['symbol'].iloc[i]
                , fontdict=dict(size=5))
        #fck me that took too long to figure out. iloc is important.

# limits
#plt.xlim(100, )
#plt.ylim(0, 10)
# axes
plt.xlabel('margin of safety')
plt.ylabel('from low')
# size

output_raw = '0_scatterplot.pdf'
plt.savefig(os.path.join(cwd,input_folder,charts_folder,output_raw), dpi=300)
plt.close('all')
#plt.show()
