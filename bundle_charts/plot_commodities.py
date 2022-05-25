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
crude_oil = commodities_df.iloc[:,[0,1,2,3]]
coal = commodities_df.iloc[:,[4,5]]
gas = commodities_df.iloc[:,[6,7,8]]
gas_index = commodities_df.iloc[:,[9]]
cocoa_coffee = commodities_df.iloc[:,[10,11,12]]
tea = commodities_df.iloc[:,[13,14,15,16]]
oils = commodities_df.iloc[:,[17,21,22]]
beans = commodities_df.iloc[:,[18,23,25,27]]
plants = commodities_df.iloc[:,[19,20,24,26,28,29,30,31,32,33,34,35]]
rice = commodities_df.iloc[:,[32,33,34,35]]
wheat = commodities_df.iloc[:,[36,37]]
fruits = commodities_df.iloc[:,[38,39,40]]
meat = commodities_df.iloc[:,[41,42,43,44]]
sugar = commodities_df.iloc[:,[45,46]]
wood = commodities_df.iloc[:,[49,50,51,52,53]]
materials_one = commodities_df.iloc[:,[48,54,55,56]]
fertilizers = commodities_df.iloc[:,[58,59,60,61]]
#metals = commodities_df.iloc[:,[62,63,64,65,66,67,68,69,70,71]]

# create a list of dataframes and loop through them to create separate charts
alldfs = [var for var in dir() if isinstance(eval(var), pd.core.frame.DataFrame)]
for df_name in alldfs:
    if df_name != 'commodities_df':
        print(df_name)
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
        g.set_xticklabels(comm_df['Date'], rotation=90, fontsize=3, color='white')
        every_nth = 4
        for n, label in enumerate(g.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)


        g.set_yticks(g.get_yticks())
        g.set_yticklabels(g.get_yticks(), size=5, color='white')
        g.legend(loc='upper left', frameon=False, ncol=1, fontsize=5, labelcolor='white')

        ###############################
        #plt.tight_layout()
        zeros_commod = '000_commodity_'
        output_raw = zeros_commod + df_name + '.pdf'
        plt.savefig(os.path.join(cwd, input_folder, charts_folder, output_raw), dpi=100, facecolor='black')
        #plt.show()
        #sys.exit()
    else:
        pass
