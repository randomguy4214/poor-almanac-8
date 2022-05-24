#!/usr/bin/python
print('commodities - initiating')

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
oils = commodities_df.iloc[:,[17,18,21,22,23,25,27]]
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

############################################################################################
# START PLOTTING ###########################################################################
### overall template for subplots
fig, grid = plt.subplots(
    figsize=(14, 8.5)  # pdf dimensions
    , sharey=False, sharex=False  # do not sync axes
    , tight_layout=True
    , subplot_kw=dict(frameon=False  # switch off spines
                      , visible=False  # fuck you stupid cunt. literally one week wasted for this shit.
                      )
);
# create a grid for plots
# https://matplotlib.org/3.5.0/gallery/userdemo/demo_gridspec03.html#sphx-glr-gallery-userdemo-demo-gridspec03-py
grid = GridSpec(3  # rows
                , 5  # columns
                , width_ratios=[1, 1, 1, 1, 1]
                , height_ratios=[1, 1, 1])
# 1st row
ax1 = fig.add_subplot(grid[0])  # oil
ax2 = fig.add_subplot(grid[1])  # coal
ax3 = fig.add_subplot(grid[2])  # gas
ax4 = fig.add_subplot(grid[3])  # gas_index
ax5 = fig.add_subplot(grid[4])  # cocoa & coffee
# 2nd row
ax6 = fig.add_subplot(grid[5])  # tea
ax7 = fig.add_subplot(grid[6])  #
ax8 = fig.add_subplot(grid[7])  #
ax9 = fig.add_subplot(grid[8])  #
ax10 = fig.add_subplot(grid[9])  #
# 3rd row
ax11 = fig.add_subplot(grid[10])  #
ax12 = fig.add_subplot(grid[11])  #
ax13 = fig.add_subplot(grid[12])  #
ax14 = fig.add_subplot(grid[13])  #
ax15 = fig.add_subplot(grid[14])  #

# 1
g_crude_oil = crude_oil.plot(
    use_index=True
    , alpha=1
    , linewidth=0.5
    , kind='line'
    , ax=ax1
)
g_crude_oil.set_facecolor('black')
g_crude_oil.set_xticks(g_crude_oil.get_xticks())
g_crude_oil.set_yticks(g_crude_oil.get_yticks())
g_crude_oil.set_yticklabels(g_crude_oil.get_yticks(), size=5, color='white')
g_crude_oil.legend(loc='upper left', frameon=False, ncol=1, fontsize=5, labelcolor='white')
g_crude_oil.axes.get_xaxis().set_visible(False)

# 2
g_coal = coal.plot(
    use_index=True
    , alpha=1
    , linewidth=0.5
    , kind='line'
    , ax=ax2
)
g_coal.set_facecolor('black')
g_coal.set_xticks(g_coal.get_xticks())
g_coal.set_yticks(g_coal.get_yticks())
g_coal.set_yticklabels(g_coal.get_yticks(), size=5, color='white')
g_coal.legend(loc='upper left', frameon=False, ncol=1, fontsize=5, labelcolor='white')
g_coal.axes.get_xaxis().set_visible(False)

# 3
g_gas = gas.plot(
    use_index=True
    , alpha=1
    , linewidth=0.5
    , kind='line'
    , ax=ax3
)
g_gas.set_facecolor('black')
g_gas.set_xticks(g_gas.get_xticks())
g_gas.set_yticks(g_gas.get_yticks())
g_gas.set_yticklabels(g_gas.get_yticks(), size=5, color='white')
g_gas.legend(loc='upper left', frameon=False, ncol=1, fontsize=5, labelcolor='white')
g_gas.axes.get_xaxis().set_visible(False)

# 4
g_gas_index = gas_index.plot(
    use_index=True
    , alpha=1
    , linewidth=0.5
    , kind='line'
    , ax=ax4
)
g_gas_index.set_facecolor('black')
g_gas_index.set_xticks(g_gas_index.get_xticks())
g_gas_index.set_yticks(g_gas_index.get_yticks())
g_gas_index.set_yticklabels(g_gas_index.get_yticks(), size=5, color='white')
g_gas_index.legend(loc='upper left', frameon=False, ncol=1, fontsize=5, labelcolor='white')
g_gas_index.axes.get_xaxis().set_visible(False)

# 5
g_cocoa_coffee = cocoa_coffee.plot(
    use_index=True
    , alpha=1
    , linewidth=0.5
    , kind='line'
    , ax=ax5
)
g_cocoa_coffee.set_facecolor('black')
g_cocoa_coffee.set_xticks(g_cocoa_coffee.get_xticks())
g_cocoa_coffee.set_yticks(g_cocoa_coffee.get_yticks())
g_cocoa_coffee.set_yticklabels(g_cocoa_coffee.get_yticks(), size=5, color='white')
g_cocoa_coffee.legend(loc='upper left', frameon=False, ncol=1, fontsize=5, labelcolor='white')
g_cocoa_coffee.axes.get_xaxis().set_visible(False)


###############################
plt.tight_layout()
output_raw = '000_commodities.pdf'
plt.savefig(os.path.join(cwd, input_folder, charts_folder, output_raw), dpi=100, facecolor='black')
plt.show()