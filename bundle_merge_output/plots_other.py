#!/usr/bin/python
print('drawing charts')
import warnings
warnings.filterwarnings("ignore")
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
from datetime import date
from matplotlib.gridspec import GridSpec


pd.options.mode.chained_assignment = None  # default='warn'
pd.options.mode.use_inf_as_na = True

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts"

# import files
########## margin of safety
df_5_symbols_marg_of_safety = pd.read_csv(os.path.join(cwd,input_folder,"5_symbols_marg_of_safety.csv"), low_memory=False)
########## quarterly
df_q = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_q.csv")
                   , usecols = ['symbol','date', 'grossProfitRatio', 'operatingCashFlow', 'calendarYear'
                                    , 'period', 'shortTermDebt', 'longTermDebt', 'totalStockholdersEquity'
                                , 'inventory']
                   , low_memory=False)
df_merged = pd.merge(df_5_symbols_marg_of_safety, df_q
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
#df_q = df_merged #.head(150)
df_q = df_merged.groupby('symbol').head(80).reset_index(drop=True) # selecting only 20 years per symbol
########## annual
df_a = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_a.csv")
                   , usecols = ['symbol','date', 'grossProfitRatio', 'operatingCashFlow', 'calendarYear'
                                    , 'period', 'shortTermDebt', 'longTermDebt', 'totalStockholdersEquity'
                                , 'inventory', 'revenue']
                   , low_memory=False)
df_a = df_a.groupby('symbol').head(20).reset_index(drop=True) # selecting only 20 years per symbol
########## other
df_other = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_other.csv")
                   , usecols = ['symbol','description', 'country', 'industry'], low_memory=False)
df_other.fillna('N/A')
########## own_ea
df_own_ea = pd.read_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa_a.csv")
                        , usecols = ['symbol', 'maint_capex_ratio'], low_memory=False)

    # QUARTERLY DATAFRAME with margin of safety
#df = df_merged[(df_merged['symbol'].str.contains('SKM|SPWH|RBB'))]
df_q = df_q[df_q['operatingCashFlow'].notna()]
df_q = df_q[df_q['date'].notna()]
df_q = df_q[df_q['calendarYear'].notna()]
df_q['calendarYear'] = df_q['calendarYear'].astype(int)
df_q['marg_of_saf_perp'] = df_q['marg_of_saf_perp'].round(0)
df_q['yearQ_str'] = df_q['calendarYear'].astype(str) + ' ' + df_q['period'].astype(str)
df_q['symbol_marg_of_saf'] = df_q['symbol'].astype(str) + ' / ' + df_q['marg_of_saf_perp'].astype(str) + ' %'
df_q = df_q.sort_values(['symbol','date'], ascending=[True, True])
    # ANNUAL DATAFRAME with Other and OwnEa
df_merged = pd.merge(df_a, df_other
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_to_merge = df_merged
df_merged = pd.merge(df_to_merge, df_own_ea
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_a = df_merged.fillna(0)
df_a['OwnEa'] = df_a['operatingCashFlow'] + (((-1 * df_a['revenue'])) * (df_a['maint_capex_ratio']/100))
df_a['OwnEa'] = df_a['OwnEa'].round(0)
df_a['calendarYear_str'] = df_a['calendarYear'].astype(int).astype(str) + ' ' + df_a['period'].astype(str)

#df_a['OwnEa'] = df_a['OwnEa'].astype(int)

# create symbols from margin of safety file
df_symbols = df_5_symbols_marg_of_safety['symbol'].drop_duplicates().reset_index(drop=False).drop(columns='index')
#df_symbols = df_symbols #.head(5)
#df_symbols = df_symbols.iloc[2: , :]
# loop through each ticker, create charts, and save pdfs
index_max = pd.to_numeric(df_symbols.index.values.max())
for i in range(0, df_symbols.index[-1]):
    try:
        df_narrow = pd.DataFrame(df_symbols.iloc[i]).T              #whythefuck selecting a row is series and not DF???
        df_narrow.reset_index(inplace=True, drop=True)
        # prepare quarterly statements
        df_merged = pd.merge(df_narrow, df_q
                             , how='left', left_on=['symbol']
                             , right_on=['symbol'], suffixes=('', '_drop'))
        df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
        df_temp_q = df_merged
        df_temp_q = df_temp_q.sort_values(['symbol', 'date'], ascending=[False, False])
        df_temp_q['inventory_cf'] = df_temp_q['inventory'] - df_temp_q['inventory'].shift(-1) #get inventory diff
        #print(df_temp_q)
        df_temp_q['inventory_cf'].fillna(0)
        df_temp_q = df_temp_q.sort_values(['symbol', 'date'], ascending=[False, True])
        #df_temp_q.to_csv(os.path.join(cwd, input_folder, "test.csv"), index=False)
        #sys.exit()

        # prepare annual statements
        df_merged = pd.merge(df_narrow, df_a
                             , how='left', left_on=['symbol']
                             , right_on=['symbol'], suffixes=('', '_drop'))
        df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
        df_temp_a = df_merged
        #df_temp_a.to_csv(os.path.join(cwd, input_folder, "test.csv"), index=False)

        ############################################################################################
        # START PLOTTING ###########################################################################
        ### overall template for subplots
        fig, grid = plt.subplots(
            figsize=(14, 8.5)                       # pdf dimensions
            , sharey=False, sharex=False            # do not sync axes
            , tight_layout=True
            , subplot_kw=dict(frameon=False         # switch off spines
                              , visible = False     # fuck you stupid cunt. literally one week wasted for this shit.
                              )
            );
        #plt.style.use('seaborn-paper')
        sns.set(style="darkgrid", palette="muted", color_codes=True)
        # create a grid for plots
        # https://matplotlib.org/3.5.0/gallery/userdemo/demo_gridspec03.html#sphx-glr-gallery-userdemo-demo-gridspec03-py
        grid = GridSpec(2 # rows
                        ,4 # columns
                        , width_ratios=[2, 1, 1, 1]
                        , height_ratios=[1, 1])
            # 1st row
        ax1 = fig.add_subplot(grid[0])  # OpCash q
        ax2 = fig.add_subplot(grid[1])  # OpCash a
        ax3 = fig.add_subplot(grid[2])  # sales (?)
        ax3_secondy = ax3.twinx() # second Y axis for ax3
        ax4 = fig.add_subplot(grid[3])  # capital structure
            # 2nd row
        ax5 = fig.add_subplot(grid[4])  # inventory q
        ax6 = fig.add_subplot(grid[5])  # Owners Earnings a
        #ax7 = fig.add_subplot(grid[6])  # smth else
        #ax8 is where text plot should be, but its fucked up

        ### Cash Op quarterly
        g_OpCash_q = sns.barplot(
            x = 'yearQ_str'
            , y = 'operatingCashFlow'
            , data = df_temp_q
            , palette = sns.color_palette('GnBu_d', 4)
            , alpha=.7
            , ci=None # error bars
            , ax=ax1                                # location on global grid
            )

        # formatting
        #g_OpCash_q.set_ylabel('Operating CF in M, quarterly', fontsize=8, color='gray')
        g_OpCash_q.tick_params(axis='y', which='major', labelsize=5, color='gray')
        g_OpCash_q.yaxis.label.set_visible(False)
        g_OpCash_q.set_title('Operating CF in M, quarterly', fontsize=8, color='gray')
        ylabels = ['{:,}'.format(y) + ' M' for y in (g_OpCash_q.get_yticks() / 1000000).astype('int64')]
        g_OpCash_q.set_yticklabels(ylabels, size=5, color='gray')
        g_OpCash_q.minorticks_off()
        g_OpCash_q.set_xticklabels(g_OpCash_q.get_xticklabels(), rotation=90, fontsize=5, color='gray')
        g_OpCash_q.axes.get_xaxis().set_visible(False)
        g_OpCash_q.spines['left'].set_color('gray')
        g_OpCash_q.spines['bottom'].set_color('gray')
        g_OpCash_q.tick_params(axis='x', colors='gray')
        g_OpCash_q.tick_params(axis='y', colors='gray')

        ### Cash Op annually
        g_OpCash_a = sns.barplot(
            x = 'calendarYear_str'
            , y = 'operatingCashFlow'
            , data = df_temp_a
            , palette = sns.color_palette('GnBu_d', 4)
            , alpha=.7
            , ci = None                               # error bars switched off
            , ax = ax2
            )
        # formatting
        g_OpCash_a.yaxis.label.set_visible(False)
        g_OpCash_a.set_title('Operating CF in M, annually', fontsize=8, color='gray')
        g_OpCash_a_ylabels = ['{:,}'.format(y) + ' M' for y in (g_OpCash_a.get_yticks() / 1000000).astype('int64')]
        g_OpCash_a.set_yticklabels(g_OpCash_a_ylabels, size=5, color='gray')
        g_OpCash_a.minorticks_off()
        g_OpCash_a.axes.get_xaxis().set_visible(False)
        g_OpCash_a.set_xticklabels(g_OpCash_a.get_xticklabels(), rotation=90, fontsize=5, color='gray')
        g_OpCash_a.xaxis.label.set_visible(True)
        g_OpCash_a.spines['left'].set_color('gray')
        g_OpCash_a.spines['bottom'].set_color('gray')
        g_OpCash_a.tick_params(axis='x', colors='gray')
        g_OpCash_a.tick_params(axis='y', colors='gray')

        ### Sales annually
        g_Sale_a = sns.barplot(
            x = 'calendarYear_str'
            , y = 'revenue'
            , data = df_temp_a
            , palette = sns.color_palette('GnBu_d', 4)
            , alpha=.7
            , ci = None
            , ax = ax3
            )
        # formatting
        g_Sale_a.yaxis.label.set_visible(False)
        g_Sale_a.set_title('Sales and margins, annually', fontsize=8, color='gray')
        g_Sale_a_labels = ['{:,}'.format(y) + ' M' for y in (g_Sale_a.get_yticks() / 1000000).astype('int64')]
        g_Sale_a.set_yticklabels(g_Sale_a_labels, size=5, color='gray')
        g_Sale_a.minorticks_off()
        g_Sale_a.axes.get_xaxis().set_visible(False)
        g_Sale_a.set_xticklabels(g_Sale_a.get_xticklabels(), rotation=90, fontsize=5, color='gray')
        g_Sale_a.xaxis.label.set_visible(True)
        g_Sale_a.tick_params(axis='x', colors='gray')
        g_Sale_a.tick_params(axis='y', colors='gray')
        g_Sale_a.spines['left'].set_color('gray')
        g_Sale_a.spines['bottom'].set_color('gray')

        ### Margin annually
        g_Marg_a = sns.lineplot(
            x = 'calendarYear_str'
            , y = 'grossProfitRatio'
            , data = df_temp_a
            , color = '#798e95'
            , alpha=.3
            #, ci = None
            , ax = ax3_secondy
            )
        # formatting
        g_Marg_a.yaxis.label.set_visible(False)
        g_Marg_a_ylabels = ['{:,}'.format(y) + ' %' for y in (g_Marg_a.get_yticks() * 100).astype('int64')]
        g_Marg_a.set_yticklabels(g_Marg_a_ylabels, size=5, color='gray')
        g_Marg_a.minorticks_off()
        g_Marg_a.axes.get_xaxis().set_visible(False)
        g_Marg_a.xaxis.label.set_visible(False)
        g_Marg_a.tick_params(axis='x', colors='gray')
        g_Marg_a.tick_params(axis='y', colors='gray')
        g_Marg_a.spines['left'].set_color('gray')
        g_Marg_a.spines['bottom'].set_color('gray')
        g_Marg_a.grid(False)

        ### EQUITY DEBT CHARTS (stacked)
        # ticker / marg of safety and date as plot label
        today_d_str = d4 = date.today().strftime("%b-%d-%Y")
        ticker_str = df_temp_q['symbol_marg_of_saf'][0]
        ticker_and_date_str = ticker_str + ' / ' + today_d_str
        print(ticker_str,' / ',  i+1, ' out of ',df_symbols.index[-1])

        # reshape q data to create stacked bar chart
        # https://stackoverflow.com/questions/49046317/pandas-pivot-merge-multiple-columns-into-single-using-column-headers-as-values
        df_temp_q_Eq_D = df_temp_q[['symbol', 'yearQ_str', 'totalStockholdersEquity'
                                    , 'longTermDebt', 'shortTermDebt']]
        df_temp_q_Eq_D_stacked = (df_temp_q_Eq_D.set_index(['symbol', 'yearQ_str'])
                                  .stack()
                                  .reorder_levels([2,0,1])
                                  .reset_index(name='values')    # after reshaping, name a column AND set index
                                  .rename(columns={'level_0':'type'})
                                  .drop_duplicates(keep=False, inplace=False))
        # plot equity, long term and short term debt in a stacked-bar chart (matplotlib, not seaborn)
        # https://stackoverflow.com/questions/67320415/stacked-barplot-in-seaborn-using-numeric-data-as-hue
        g_EqD_pivot_temp = pd.pivot_table(df_temp_q_Eq_D_stacked
                                     , index='yearQ_str', columns='type', values='values', aggfunc='sum')
        g_EqD_pivot = g_EqD_pivot_temp[['totalStockholdersEquity','longTermDebt','shortTermDebt']].copy()
        #g_EqD_pivot.to_csv(os.path.join(cwd, input_folder, "test.csv"))
        #sys.exit()
        g_EqD = g_EqD_pivot.plot.bar(stacked=True
            #, alpha=.7
            , color=['#798e95','#94c3cf', '#b0d3cf']
            , edgecolor='#798e95'
            , width=1               # no gap between columns
            , ax=ax4
            )
        # formatting
        g_EqD.set_title(ticker_str, fontsize=8, color='gray')
        ylabels = ['{:,}'.format(y) + ' M' for y in (g_EqD.get_yticks() / 1000000).astype('int64')]
        g_EqD.set_yticklabels(ylabels, size=5, color='gray')
        g_EqD.minorticks_off()
        g_EqD.axes.get_xaxis().set_visible(False)
        g_EqD.xaxis.label.set_visible(False)
        g_EqD.yaxis.label.set_visible(False)
        g_EqD.legend(loc='upper left', frameon=False, ncol=3, fontsize=5)
        g_EqD.spines['left'].set_color('gray')
        g_EqD.spines['bottom'].set_color('gray')
        g_EqD.tick_params(axis='x', colors='gray')
        g_EqD.tick_params(axis='y', colors='gray')

        # INVENTORY CF quarterly
        g_Inv_q = sns.barplot(
            x = 'yearQ_str'
            , y = 'inventory_cf'
            , data = df_temp_q
            , palette = sns.color_palette('GnBu_d', 4)
            , alpha=.7
            , ci=None # error bars
            , ax = ax5
            )
        # formatting
        g_Inv_q.yaxis.label.set_visible(False)
        g_Inv_q.set_title('Inventory CF in M, quarterly', fontsize=8, color='gray')
        g_Inv_q_ylabels = ['{:,}'.format(y) + ' M' for y in (g_Inv_q.get_yticks() / 1000000).astype('int64')]
        g_Inv_q.set_yticklabels(g_Inv_q_ylabels, size=5, color='gray')
        g_Inv_q.minorticks_off()
        g_Inv_q.set_xticklabels(g_Inv_q.get_xticklabels(), rotation=90, fontsize=5, color='gray')
        g_Inv_q.xaxis.label.set_visible(False)
        g_Inv_q.spines['left'].set_color('gray')
        g_Inv_q.spines['bottom'].set_color('gray')
        g_Inv_q.tick_params(axis='x', colors='gray')
        g_Inv_q.tick_params(axis='y', colors='gray')
        #df_temp_a.to_csv(os.path.join(cwd, input_folder, "test.csv"), index=False)

        # OwnEa annually
        g_OwnEa_a = sns.barplot(
            x='calendarYear'
            , y='OwnEa'
            , data=df_temp_a
            , palette=sns.color_palette('GnBu_d', 4)
            , alpha=.7
            , color='blue'
            , ci=None
            , ax=ax6
            )

        # formatting
        g_OwnEa_a.set_title('Owners Earnings, annually', fontsize=8, color='gray')
        g_OwnEa_a.yaxis.label.set_visible(False)
        g_OwnEa_a_ylabels = ['{:,}'.format(y) + ' M' for y in (g_OwnEa_a.get_yticks() / 1000000).astype('int64')]
        g_OwnEa_a.set_yticklabels(g_OwnEa_a_ylabels, size=5, color='gray')
        g_OwnEa_a.set_xticklabels(g_OwnEa_a.get_xticklabels(), rotation=90, fontsize=5, color='gray')
        g_OwnEa_a.minorticks_off()
        g_OwnEa_a.xaxis.label.set_visible(False)
        g_OwnEa_a.spines['left'].set_color('gray')
        g_OwnEa_a.spines['bottom'].set_color('gray')
        g_OwnEa_a.tick_params(axis='x', colors='gray')
        g_OwnEa_a.tick_params(axis='y', colors='gray')

        ### Description
        descr_str = df_temp_a['description'][0]
        plt.figtext(0.81, 0.51
                    , descr_str
                    , verticalalignment='top'
                    , horizontalalignment='left'
                    , fontsize=8
                    , color='gray'
                    , fontstyle='italic'
                    , wrap = True)

    #######################

        # save plots as pdf
        sns.despine()                                       # remove some frame lines from seaborn plots
        plt.tick_params(axis='both', which='both', left=False, right=False, bottom=False, top=False, labelbottom=False)
        output_raw = df_temp_q['symbol'][0] + '.pdf'
        #print(output_raw)

        plt.savefig(os.path.join(cwd, input_folder, charts_folder, output_raw), dpi=300)
        plt.tight_layout()
        #plt.show()
        #sys.exit()

        # reset
        mpl.rc_file_defaults()
        plt.close('all')
    except:
        pass
