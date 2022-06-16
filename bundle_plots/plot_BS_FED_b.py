#!/usr/bin/python
print('FED balance sheet 100 weeks - plotting')

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
from datetime import date
from matplotlib.gridspec import GridSpec

cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"
charts_folder = "5_charts"

### prepare dataframe
df_BS_FED = pd.read_csv(os.path.join(cwd,input_folder,"2_processed_BS_FED.csv")
                             , low_memory=False
                             , index_col='Date')
df_BS_FED_b = df_BS_FED.iloc[-100:].copy() # last 100 weeks
#print(df_BS_FED_b)
color_palette = [
'#a02dbc'
, '#9940af'
, '#9252a2'
, '#8e5b9b'
, '#8b6494'
, '#876e8d'
, '#00ffff'
, '#05ebf5'
, '#0ad6eb'
, '#0fc2e0'
, '#14add6'
, '#1a99cc'
, '#F0FF00' # reverse repo
, '#c0cc00' # reverse repo
, '#244a92'
, '#1a5a8d'
, '#0f6988'
, '#00ff00'
, '#05eb0f'
, '#0ad61f'
, '#0fc22e'
, '#14ad3d'
, '#1a994d'
, '#61143d'
, '#690f2e'
, '#710a1f'
, '#78050f'
, '#800000'
    ]


#sys.exit()


#### start plotting
plt.rcParams["figure.figsize"] = (11.69, 8.27) # pdf dimensions
g = df_BS_FED_b.plot(
    alpha=1
    , stacked=True
    , kind='area'
    , color = color_palette
    , rasterized=True
)
g.set_facecolor('black')
g.set_xticks(range(0, len(df_BS_FED_b.index)), df_BS_FED_b.index.values)
g.set_xticklabels(df_BS_FED_b.index.values, rotation=90, fontsize=5, color='white')
every_nth = 4
for n, label in enumerate(g.xaxis.get_ticklabels()):
    if n % every_nth != 0:
        label.set_visible(False)
g.set_yticks(g.get_yticks())
Trillion = 1000000000000 / 1000000 # the data is in millions
g_ylabels = ['{:,}'.format(y) + ' T' for y in ((g.get_yticks()) / Trillion).astype('int64')]
g.set_yticklabels(g_ylabels, size=8, color='white')
g.legend(loc='upper left', frameon=False, ncol=1, fontsize=5, labelcolor='gray')
g.set_title('Weekly FED balance sheet by type, last 100 weeks', fontsize=8, color='white', loc='center')

###############################
plt.tight_layout()
BS_FED = '001_BS_FED_b'
output_raw = BS_FED + '.pdf'

plt.savefig(os.path.join(cwd, input_folder, charts_folder, output_raw)
                    , facecolor='#00224B'
            )
#plt.show()
plt.close('all')
#sys.exit()
