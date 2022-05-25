#!/usr/bin/python
print('commodities plots - initiating')

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
commodities_df = pd.read_csv(os.path.join(cwd,input_folder,"2_processed_commodities.csv")
                             , low_memory=False
                             , index_col='Date')

### prepare sub dataframes
a_crude_oil = commodities_df.iloc[:,[0,1,2,3]]
b_coal = commodities_df.iloc[:,[4,5]]
c_gas = commodities_df.iloc[:,[6,7,8]]
cc_gas_index = commodities_df.iloc[:,[9]]
d_cocoa_coffee = commodities_df.iloc[:,[10,11,12]]
d_tobacco = commodities_df.iloc[:,[47]]
d_tea = commodities_df.iloc[:,[13,14,15,16]]
e_oils = commodities_df.iloc[:,[17,21,22,24,20]]
e_beans = commodities_df.iloc[:,[18,23,25,27]]
e_plants = commodities_df.iloc[:,[19,26,28,29,30]]
e_rice = commodities_df.iloc[:,[31,32,33,34]]
e_wheat = commodities_df.iloc[:,[35,36]]
e_fruits = commodities_df.iloc[:,[37,38,39]]
f_meat = commodities_df.iloc[:,[40,41,42,43]]
e_sugar = commodities_df.iloc[:,[44,45,46]]
f_wood = commodities_df.iloc[:,[48,49,50,51,52]]
f_materials_one = commodities_df.iloc[:,[53,54,55]]
e_fertilizers = commodities_df.iloc[:,[56,57,58,59,60]]
g_metals_1 = commodities_df.iloc[:,[63,65,66,67]]
g_metals_2 = commodities_df.iloc[:,[61,64,68,69,70]]
g_metals_3 = commodities_df.iloc[:,[62,70]]

# create a list of dataframes and loop through them to create separate charts
alldfs = [var for var in dir() if isinstance(eval(var), pd.core.frame.DataFrame)]
for df_name in alldfs:
    if df_name != 'commodities_df':
        print(df_name + ' plot')
        comm_df = eval(df_name) # searches for name of dataframe and activates it
        comm_df.reset_index(drop=False, inplace=True)
        #df_name_csv = df_name + '.csv'
        #comm_df.to_csv(os.path.join(cwd, input_folder, charts_folder, df_name_csv))
        #print(comm_df)

        #### start plotting
        g = comm_df.plot(
            alpha=1
            , linewidth=0.6
            , kind='line'
        )
        g.set_facecolor('black')
        g.set_xticks(range(0, len(comm_df.index)), comm_df['Date'])
        g.set_xticklabels(comm_df['Date'], rotation=90, fontsize=3, color='gray')
        every_nth = 4
        for n, label in enumerate(g.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)


        g.set_yticks(g.get_yticks())
        g_ylabels = ['{:,}'.format(y) for y in (g.get_yticks()).round(2)]
        g.set_yticklabels(g_ylabels, size=5, color='gray')
        g.set_ylim(0, max(g.get_yticks()))
        g.legend(loc='upper left', frameon=False, ncol=1, fontsize=5, labelcolor='gray')

        ###############################
        #plt.tight_layout()
        zeros_commod = '000_commodity_'
        output_raw = zeros_commod + df_name + '.pdf'
        plt.savefig(os.path.join(cwd, input_folder, charts_folder, output_raw), dpi=100, facecolor='black')
        plt.close('all')
        #plt.show()
        #sys.exit()
    else:
        pass
