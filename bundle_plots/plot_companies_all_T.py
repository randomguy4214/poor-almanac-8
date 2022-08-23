#!/usr/bin/python
print('drawing companies')
#import warnings
#warnings.filterwarnings("ignore")
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from datetime import datetime
from pathlib import Path
import sys
import subprocess

pd.options.mode.chained_assignment = None  # default='warn'
pd.options.mode.use_inf_as_na = True

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
charts_folder = "5_charts_all"

# import files
########## margin of safety
df_5_symbols_marg_of_safety = pd.read_csv(os.path.join(cwd,input_folder,"5_symbols_marg_of_safety.csv")
                                          , low_memory=False)
########## quarterly
df_q = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_q.csv")
                   , usecols = ['symbol','date', 'grossProfitRatio', 'operatingCashFlow', 'calendarYear'
                                    , 'period', 'shortTermDebt', 'longTermDebt', 'totalStockholdersEquity'
                                , 'inventory', 'accountsReceivables', 'accountsPayables', 'netIncome'
                                , 'revenue', 'cashAndCashEquivalents']
                   , low_memory=False)
df_merged = pd.merge(df_q, df_5_symbols_marg_of_safety
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
#df_q = df_merged #.head(150)
df_q = df_merged.groupby('symbol').head(80).reset_index(drop=True) # selecting only 20 years per symbol
#df_q.to_csv(os.path.join(cwd, input_folder, charts_folder, 'test_df_q_original.csv'), index=False)
#sys.exit()
########## annual
df_a = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_financials_a.csv")
                   , usecols = ['symbol','date', 'grossProfitRatio', 'operatingCashFlow', 'calendarYear'
                                    , 'period', 'shortTermDebt', 'longTermDebt', 'totalStockholdersEquity'
                                , 'inventory', 'revenue', 'netIncome']
                   , low_memory=False)
df_a = df_a.groupby('symbol').head(20).reset_index(drop=True) # selecting only 20 years per symbol
#df_a.to_csv(os.path.join(cwd, input_folder, charts_folder, 'test_df_a_original.csv'), index=False)
########## other
df_other = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_other.csv")
                   , usecols = ['symbol','description', 'country', 'industry'], low_memory=False)
df_other.fillna('N/A', inplace=True)
########## EV / marcap / SharesOutstanding
df_EV = pd.read_csv(os.path.join(cwd,input_folder,"3_processed_EV_q.csv")
                   , usecols = ['symbol','stockPrice', 'numberOfShares', 'date'], low_memory=False)
df_EV.fillna(0, inplace=True)
########## own_ea
df_own_ea = pd.read_csv(os.path.join(cwd,input_folder,"4_recent_OwnEa_a.csv")
                        , usecols = ['symbol', 'maint_capex_ratio'], low_memory=False)
########## latest price
df_price = pd.read_csv(os.path.join(cwd,input_folder,'2_processed_prices.csv')
                       , usecols=['symbol', 'price'], low_memory=False)

    # QUARTERLY DATAFRAME with margin of safety
#df = df_merged[(df_merged['symbol'].str.contains('SKM|SPWH|RBB'))]
df_q = df_q[df_q['operatingCashFlow'].notna()]
df_q = df_q[df_q['date'].notna()]
df_q = df_q[df_q['calendarYear'].notna()]
df_q['calendarYear'] = df_q['calendarYear'].astype('Int64')
df_q['marg_of_saf_perp'] = df_q['marg_of_saf_perp'].astype('Int64')
df_q['yearQ_str'] = df_q['calendarYear'].astype(str) + ' ' + df_q['period'].astype(str)
df_q['symbol_marg_of_saf'] = df_q['symbol'].astype(str) + ' / ' + df_q['marg_of_saf_perp'].astype(str) + ' %'
df_q = df_q.sort_values(['symbol','date'], ascending=[True, True])
#df_q.to_csv(os.path.join(cwd, input_folder, charts_folder, 'test_df_q_original_full.csv'), index=False)
#sys.exit()
    # ANNUAL DATAFRAME with Other and OwnEa
df_merged = pd.merge(df_a, df_other
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
#df_merged.to_csv(os.path.join(cwd, input_folder, charts_folder, 'test_df_a_other.csv'), index=False)
df_to_merge = df_merged
df_merged = pd.merge(df_to_merge, df_own_ea
                     , how='left', left_on=['symbol']
                     , right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_a = df_merged.fillna(0)
df_a['OwnEa'] = df_a['operatingCashFlow'] + (((-1 * df_a['revenue'])) * (df_a['maint_capex_ratio']/100))
df_a['OwnEa'] = df_a['OwnEa'].round(0)
df_a['calendarYear_str'] = df_a['calendarYear'].astype(int).astype(str) + ' ' + df_a['period'].astype(str)
#df_a.to_csv(os.path.join(cwd, input_folder, charts_folder, 'test_df_a_ownea_other.csv'), index=False)
#sys.exit()
# create symbols from margin of safety file, should be pre-sorted in specific way
df_symbols_temp = df_5_symbols_marg_of_safety['symbol'].drop_duplicates().reset_index(drop=False).drop(columns='index')

# merge them with recently updated symbols and filter out
tickers_narrowed = pd.read_csv(os.path.join(cwd,"0_symbols.csv"))
df_merged = pd.merge(tickers_narrowed, df_other, how='left', left_on=['symbol'], right_on=['symbol'],
                     suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
#filter useless shit
useless_industries = 'asset management|shell|biotechnology|banks|capital markets|credit|REIT|insurance'
df_merged_reduced = df_merged[~df_merged['industry'].str.contains(useless_industries, case=False, na=False)].drop_duplicates()
df_merged_reduced = df_merged_reduced[~df_merged_reduced['country'].str.contains('in', case=False, na=False)].drop_duplicates()
#df_merged_reduced.to_csv(os.path.join(cwd, 'test_df_merged_reduced.csv'), index=False)
#sys.exit()
#df_symbols = df_merged.reset_index(drop=True)
df_symbols = df_merged_reduced['symbol'].drop_duplicates()
df_symbols = df_symbols.reset_index(drop=False)
#df_symbols.to_csv(os.path.join(cwd, input_folder, charts_folder, 'test_df_symbols.csv'))
#print(df_symbols)
#df_symbols = df_symbols #.head(5)
#df_symbols = df_symbols.iloc[2: , :]
# loop through each ticker, create charts, and save pdfs
index_max = pd.to_numeric(df_symbols.index.values.max())
for i in range(0, df_symbols.index[-1]+1):
    try:
        # prepare ticker
        ticker_str = str(df_symbols['symbol'][i])
        undersc = '_'
        test_df_narrow_ticker_csv = 'test_df_narrow' + undersc + ticker_str + '.csv'
        test_df_q_ticker_csv = 'test_df_q' + undersc + ticker_str + '.csv'
        test_df_a_ticker_csv = 'test_df_a' + undersc + ticker_str + '.csv'
        test_df_EV_ticker_csv = 'test_df_EV' + undersc + ticker_str + '.csv'
        df_narrow = pd.DataFrame(df_symbols.iloc[i]).T              #whythefuck selecting a row is series and not DF???
        df_narrow.reset_index(inplace=True, drop=True)
        #df_narrow.to_csv(os.path.join(cwd, input_folder, charts_folder, test_df_narrow_ticker_csv), index=False)

        # prepare quarterly statements
        try:
            df_merged = pd.merge(df_narrow, df_q
                                 , how='left', left_on=['symbol']
                                 , right_on=['symbol'], suffixes=('', '_drop'))
            df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
        except:
            df_merged = []
        #df_merged.to_csv(os.path.join(cwd, input_folder, charts_folder, test_df_q_ticker_csv), index=False)
        if len(df_merged) > 2:
            df_temp_q = df_merged.fillna(0)
            df_temp_q = df_temp_q.sort_values(['symbol', 'date'], ascending=[False, False])
            df_temp_q['inventory_cf'] = df_temp_q['inventory'] - df_temp_q['inventory'].shift(-1) #get inventory diff
            df_temp_q.rename(columns={'accountsReceivables':'CF_AccReceiv', 'accountsPayables':'CF_AccPayab'}, inplace=True)
            df_temp_q.fillna(0, inplace=True)
            #print(df_temp_q)
            df_temp_q = df_temp_q.sort_values(['symbol', 'date'], ascending=[False, True])
            #df_temp_q.to_csv(os.path.join(cwd, input_folder, charts_folder, test_df_q_ticker_csv), index=False)
            #sys.exit()

            # prepare annual statements
            df_merged = pd.merge(df_narrow, df_a
                                 , how='left', left_on=['symbol']
                                 , right_on=['symbol'], suffixes=('', '_drop'))
            df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
            df_temp_a = df_merged.fillna(0)
            df_temp_a = df_temp_a.sort_values(['symbol', 'calendarYear'], ascending=[False, True])
            df_temp_a['industry'] = df_temp_a['industry'].astype('str')
            #df_temp_a.to_csv(os.path.join(cwd, input_folder, charts_folder, test_df_a_ticker_csv), index=False)
            #sys.exit()

            # prepare ticker price and shares outstanding
            df_merged = pd.merge(df_narrow, df_EV
                                 , how='left', left_on=['symbol']
                                 , right_on=['symbol'], suffixes=('', '_drop'))
            df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
            df_temp_EV = df_merged.fillna(0)
            df_temp_EV = df_temp_EV.sort_values(['symbol', 'date'], ascending=[False, True])
            #df_temp_EV.to_csv(os.path.join(cwd, input_folder, charts_folder, test_df_EV_ticker_csv), index=False)
            #sys.exit()

            # prepare some variables
            industry = str(df_temp_a['industry'][0])
            country = str(df_temp_a['country'][0])
            today_date = str(datetime.today().strftime('%Y-%m-%d'))
            ticker_industr = ticker_str + ' / ' + industry + ' / ' + country + ' / ' + today_date
            ############################################################################################
            # START PLOTTING ###########################################################################
            ### overall template for subplots
            fig, grid = plt.subplots(
                figsize=(11.69, 8.27) # transposed pdf dimensions
                , sharey=False, sharex=False            # do not sync axes
                , tight_layout=True
                , subplot_kw=dict(frameon=False         # switch off spines
                                  , visible=False     # fuck you stupid cunt. literally one week wasted for this shit.
                                  )
                );
            # create a grid for plots
            # https://matplotlib.org/3.5.0/gallery/userdemo/demo_gridspec03.html#sphx-glr-gallery-userdemo-demo-gridspec03-py
            grid = GridSpec(2 # rows
                            ,3 # columns
                            , height_ratios=[1, 1]
                            , width_ratios=[1, 1, 1])
            ax1 = fig.add_subplot(grid[0])  #
            ax1_secondy = ax1.twinx() # second Y axis
            ax2 = fig.add_subplot(grid[1])  #
            ax2_secondy = ax2.twinx() # second Y axis
            ax3 = fig.add_subplot(grid[2])  #
            ax3_secondy = ax3.twinx() #
            ax4 = fig.add_subplot(grid[3]) #
            ax4_secondy = ax4.twinx()
            ax5 = fig.add_subplot(grid[4])  #
            ax6 = fig.add_subplot(grid[5])  #
            #ax7 = fig.add_subplot(grid[6])  #
            #ax7.set_facecolor('black')
            #ax8 is where "text" plot should be, but its fucked up
            #plt.style.use('dark_background')

            try:
                ###  Quarterly Cash Op, Net Income, Revenue
                df_temp_q_Rev_q = df_temp_q[['yearQ_str', 'revenue']]
                g_Rev_q = df_temp_q_Rev_q.plot('yearQ_str', color='#05445E', alpha=1, width=1, kind='bar', ax=ax1, stacked=False, rasterized=False)
                df_temp_q_ni_q = df_temp_q[['yearQ_str', 'netIncome']]
                g_NI_q = df_temp_q_ni_q.plot('yearQ_str', color='#189AB4', alpha=1, width = 1, kind='bar', ax=ax1, stacked=False, rasterized=False)
                df_temp_q_opcash_q = df_temp_q[['yearQ_str', 'operatingCashFlow']]
                g_OpCash_q = df_temp_q_opcash_q.plot('yearQ_str', color='#C76280', alpha=1, width=1, kind='bar', ax=ax1, stacked=False, rasterized=False)

                # formatting
                g_OpCash_q.set_xticks(g_OpCash_q.get_xticks())
                g_OpCash_q.set_yticks(g_OpCash_q.get_yticks())
                g_OpCash_q.legend(loc='upper left', frameon=False, ncol=1, fontsize=5, labelcolor='white')
                g_OpCash_q.tick_params(axis='y', which='major', labelsize=5, color='white')
                g_OpCash_q.yaxis.label.set_visible(False)
                g_OpCash_q.set_title('Sales, NI & Operating CF, quarterly', fontsize=8, color='white')
                ylabels = ['{:,}'.format(y) + ' M' for y in (g_OpCash_q.get_yticks() / 1000000).astype('int64')]
                g_OpCash_q.set_yticklabels(ylabels, size=5, color='white')
                g_OpCash_q.minorticks_off()
                g_OpCash_q.set_xticklabels(g_OpCash_q.get_xticklabels(), rotation=90, fontsize=5, color='white')
                #g_OpCash_q.axes.get_xaxis().set_visible(False)
                g_OpCash_q.tick_params(axis='x', colors='white')
                g_OpCash_q.tick_params(axis='y', colors='white')
                g_OpCash_q.spines['left'].set_color('none')
                g_OpCash_q.spines['bottom'].set_color('none')
                g_OpCash_q.tick_params(axis='y', colors='white')
                g_OpCash_q.set_facecolor('black')
                every_nth = 4 # draw only some of the x labels
                for n, label in enumerate(g_OpCash_q.xaxis.get_ticklabels()):
                    if n % every_nth != 0 and n != len(g_OpCash_q.xaxis.get_ticklabels()):
                        label.set_visible(False)
            except:
                pass

            try:
                ### Annually Cash Op, Net Income, Revenue
                df_temp_q_Rev_a = df_temp_a[['calendarYear_str', 'revenue']]
                g_Rev_q = df_temp_q_Rev_a.plot('calendarYear_str', color='#05445E', alpha=1, width=1, kind='bar', ax=ax3, stacked=False, rasterized=False)
                df_temp_a_ni_a = df_temp_a[['calendarYear_str', 'netIncome']]
                g_NI_a = df_temp_a_ni_a.plot('calendarYear_str', color='#189AB4', alpha=1, width=1, kind='bar', ax=ax3, stacked=False, rasterized=False)
                df_temp_a_opcash_a = df_temp_a[['calendarYear_str', 'operatingCashFlow']]
                g_OpCash_a = df_temp_a_opcash_a.plot('calendarYear_str', color='#C76280', alpha=1, width = 1, kind='bar', ax=ax3, stacked=False, rasterized=False)

                # formatting
                g_OpCash_a.set_xticks(g_OpCash_a.get_xticks())
                g_OpCash_a.set_yticks(g_OpCash_a.get_yticks())
                g_OpCash_a.legend(loc='upper left', frameon=False, ncol=1, fontsize=5, labelcolor='white')
                g_OpCash_a.yaxis.label.set_visible(False)
                g_OpCash_a.set_title('Sales, NI & Operating CF, annually', fontsize=8, color='white')
                g_OpCash_a_ylabels = ['{:,}'.format(y) + ' M' for y in (g_OpCash_a.get_yticks() / 1000000).astype('int64')]
                g_OpCash_a.set_yticklabels(g_OpCash_a_ylabels, size=5, color='gray')
                g_OpCash_a.minorticks_off()
                #g_OpCash_a.axes.get_xaxis().set_visible(False)
                g_OpCash_a.set_xticklabels(g_OpCash_a.get_xticklabels(), rotation=90, fontsize=5, color='gray')
                g_OpCash_a.xaxis.label.set_visible(True)
                g_OpCash_a.spines['left'].set_color('none')
                g_OpCash_a.spines['bottom'].set_color('none')
                g_OpCash_a.tick_params(axis='x', colors='white')
                g_OpCash_a.tick_params(axis='y', colors='white')
                g_OpCash_a.set_facecolor('black')

                ### Margin annually
                df_temp_a_Marg_a = df_temp_a[['calendarYear_str','grossProfitRatio']]
                g_Marg_a = df_temp_a_Marg_a.plot('calendarYear_str', color = '#BF5757', kind='line', linewidth=0.
                                                 , alpha=0.5, linestyle='--', ax=ax3_secondy, rasterized=False)
                # formatting
                g_Marg_a.set_xticks(g_Marg_a.get_xticks())
                g_Marg_a.set_yticks(g_Marg_a.get_yticks())
                g_Marg_a.get_legend().set_visible(False)
                g_Marg_a.yaxis.label.set_visible(False)
                g_Marg_a_ylabels = ['{:,}'.format(y) + ' %' for y in (g_Marg_a.get_yticks() * 100).astype('int64')]
                g_Marg_a.set_yticklabels(g_Marg_a_ylabels, size=5, color='#12b8ff')
                g_Marg_a.axes.get_xaxis().set_visible(False)
                g_Marg_a.xaxis.label.set_visible(False)
                g_Marg_a.spines['left'].set_color('none')
                g_Marg_a.spines['bottom'].set_color('none')
                g_Marg_a.tick_params(axis='y', colors = '#BF5757')
                g_Marg_a.grid(False)
            except:
                pass

            try:
                ### Shares Outstanding
                df_temp_SO = df_temp_EV[['date', 'numberOfShares']].tail(100).reset_index(drop=True)
                g_SO_q = df_temp_SO.plot('date', color = '#BF5757', kind='line'
                                         , linewidth=0.5, alpha=0.8 , linestyle='--', ax=ax2_secondy
                                         , rasterized=False)
                # formatting
                g_SO_q.set_xticks([])
                g_SO_q.set_yticks(g_SO_q.get_yticks())
                g_SO_q.get_legend().set_visible(False)
                g_SO_q.yaxis.label.set_visible(False)
                g_SO_q_ylabels = ['{:,}'.format(y) + ' M' for y in (g_SO_q.get_yticks() / 1000000).astype('int64')]
                g_SO_q.set_yticklabels(g_SO_q_ylabels, size=5, color='#12b8ff')
                g_SO_q.set_ylim(0, max(g_SO_q.get_yticks()))
                g_SO_q.minorticks_off()

                g_SO_q.spines['left'].set_color('none')
                g_SO_q.tick_params(axis='y', colors = '#BF5757')
                g_SO_q.spines['bottom'].set_color('none')
                g_SO_q.grid(False)
                g_SO_q.set_facecolor('black')
            except:
                print('g_SO fail ' + ticker_str)

            try:
                ### Price
                periods_to_consider = 100
                df_temp_price = df_temp_EV[['date', 'stockPrice']].tail(periods_to_consider).reset_index(drop=True)
                df_temp_price['stockPrice'] = df_temp_price['stockPrice'].round(2)
                df_temp_price_to_append = df_price[df_price['symbol'] == df_symbols['symbol'][i]]
                df_temp_price_to_append['date'] = datetime.now().date().strftime("%Y-%m-%d")
                df_temp_price_to_append_two = df_temp_price_to_append[['date','price']]
                df_temp_price_to_append_two.rename(columns={'price': 'stockPrice'}, inplace=True)
                df_temp_price = pd.concat([df_temp_price, df_temp_price_to_append_two])
                df_temp_price.reset_index(drop=True, inplace=True)
                df_temp_price_max_index = len(df_temp_price) - 1
                #print(df_temp_price)
                #df_temp_price.to_csv(os.path.join(cwd, input_folder, charts_folder, test_df_EV_ticker_csv))
                g_Price_q = df_temp_price.plot('date', color='#05445E', kind='area', stacked=False, alpha=1
                                               , ax=ax2, rasterized=False)
                g_Price_q.set_title('Price vs shares outstanding, quarterly', fontsize=8, color='white')
                #g_Price_q.set_title('', fontsize=8, color='white')
                g_Price_q.get_legend().set_visible(False)
                g_Price_q.set_xticks(g_Price_q.get_xticks())
                g_Price_q.set_xticks(df_temp_price.index, labels = df_temp_price['date'])
                g_Price_q.set_xticklabels(g_Price_q.get_xticklabels(), rotation=90, fontsize=5, color='white')
                every_nth = periods_to_consider / 10

                for n, label in enumerate(g_Price_q.xaxis.get_ticklabels()):
                    if n % every_nth == 0: #https://stackoverflow.com/questions/8002217/how-do-you-check-whether-a-number-is-divisible-by-another-number
                        label.set_visible(True)
                    else:
                        label.set_visible(False)

                g_Price_q.set_facecolor('black')
                g_Price_q.set_yticks(g_Price_q.get_yticks())
                g_Price_q.yaxis.label.set_visible(False)
                g_Price_q_ylabels = ['{0:.2f}'.format(y) for y in ((g_Price_q.get_yticks()*100).astype('int64')/100)]
                g_Price_q.set_yticklabels(g_Price_q_ylabels, size=5, color='gray')
                g_Price_q.set_ylim(0, max(g_Price_q.get_yticks()))
                g_Price_q.set_yticklabels(g_Price_q.get_yticks(), size=5, color='white')
                g_Price_q.set_facecolor('black')
                g_Price_q.tick_params(axis='x', colors='white')
                g_Price_q.tick_params(axis='y', colors='white')
            except:
                print('g_Price fail / ' + ticker_str)


            try:
                ### EQUITY DEBT CHARTS

                # reshape q data to create stacked bar chart
                # https://stackoverflow.com/questions/49046317/pandas-pivot-merge-multiple-columns-into-single-using-column-headers-as-values
                df_temp_q_Eq_D = df_temp_q[['symbol', 'yearQ_str', 'totalStockholdersEquity'
                                            , 'longTermDebt', 'shortTermDebt', 'cashAndCashEquivalents']]
                df_temp_q_Eq_D['totalStockholdersEquity'][df_temp_q_Eq_D['totalStockholdersEquity'] < 0] = 0
                df_temp_q_Eq_D['longTermDebt'][df_temp_q_Eq_D['longTermDebt'] < 0] = 0
                df_temp_q_Eq_D['shortTermDebt'][df_temp_q_Eq_D['shortTermDebt'] < 0] = 0
                df_temp_q_Eq_D['cashAndCashEquivalents'][df_temp_q_Eq_D['cashAndCashEquivalents'] < 0] = 0
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
                g_EqD_pivot = g_EqD_pivot_temp[['longTermDebt','shortTermDebt', 'cashAndCashEquivalents','totalStockholdersEquity']]
                #df_g_EqD_pivot.to_csv(os.path.join(cwd, input_folder, "test_g_EqD_pivot.csv"))
                #sys.exit()
                g_EqD = g_EqD_pivot.plot(kind='area', alpha=.7, color=['#05445E', '#189AB4', '#C76280', '#304390']
                                         , ax=ax4, rasterized=False)
                # formatting
                g_EqD.set_xticks(g_EqD.get_xticks())
                g_EqD.set_yticks(g_EqD.get_yticks())
                g_EqD.set_title(ticker_industr, fontsize=12, color='white')
                ylabels = ['{:,}'.format(y) + ' M' for y in (g_EqD.get_yticks() / 1000000).astype('int64')]
                g_EqD.set_yticklabels(ylabels, size=5, color='white')
                g_EqD.set_ylim(0, max(g_EqD.get_yticks()))
                g_EqD.axes.get_xaxis().set_visible(False)
                g_EqD.xaxis.label.set_visible(False)
                g_EqD.yaxis.label.set_visible(False)
                g_EqD.legend(loc='upper left', frameon=False, ncol=1, fontsize=5, labelcolor='white')
                g_EqD.spines['left'].set_color('none')
                g_EqD.spines['bottom'].set_color('none')
                g_EqD.tick_params(axis='x', colors='white')
                g_EqD.tick_params(axis='y', colors='white')
                g_EqD.set_facecolor('black')
            except:
                ax2.set_facecolor('black')
                ax2.set_title(ticker_industr, fontsize=11, color='white')

            """ 
            # CF INVENTORY, AccReceiv, AccPayab  quarterly
            df_temp_q_Inv_q_AR_q_AP_q = df_temp_q[['yearQ_str', 'CF_AccReceiv', 'CF_AccPayab', 'inventory_cf']]
            g_Inv_q = df_temp_q_Inv_q_AR_q_AP_q.plot('yearQ_str' #x axis variable
                , color = ['#05445E','#ee2a41','#eeeff1'], alpha=0.5, kind='area'
                , stacked=False, ax=ax6, rasterized=False)
            # formatting
            g_Inv_q.set_title('Inventory CF, quarterly', fontsize=8, color='white')
            g_Inv_q.legend(loc='upper left', frameon=False, ncol=1, fontsize=5, labelcolor='white')
            g_Inv_q.set_xticks(df_temp_q_Inv_q_AR_q_AP_q.index, labels = df_temp_q_Inv_q_AR_q_AP_q['yearQ_str'])
            g_Inv_q.set_xticklabels(g_Inv_q.get_xticklabels(), rotation=90, fontsize=5, color='gray')
            every_nth = 4
            for n, label in enumerate(g_Inv_q.xaxis.get_ticklabels()):
                if n % every_nth != 0:
                    label.set_visible(False)

            g_Inv_q.xaxis.label.set_visible(False)
            g_Inv_q.yaxis.label.set_visible(False)
            g_Inv_q.set_yticks(g_Inv_q.get_yticks())
            g_Inv_q_ylabels = ['{:,}'.format(y) + ' M' for y in (g_Inv_q.get_yticks() / 1000000).astype('int64')]
            g_Inv_q.set_yticklabels(g_Inv_q_ylabels, size=5, color='gray')
            g_Inv_q.minorticks_off()
            g_Inv_q.spines['left'].set_color('none')
            g_Inv_q.spines['bottom'].set_color('none')
            g_Inv_q.tick_params(axis='x', colors='white')
            g_Inv_q.tick_params(axis='y', colors='white')
            g_Inv_q.set_facecolor('black')
            """
            ax6.set_facecolor('black')

            try:
                # OwnEa annually
                df_temp_a_OwneEa_a = df_temp_a[['calendarYear', 'OwnEa']].reset_index(drop=True)
                #print(df_temp_a_OwneEa_a)
                #df_temp_a_OwneEa_a.to_csv(os.path.join(cwd, input_folder, charts_folder, 'ownea.csv'), index=False)
                g_OwnEa_a = df_temp_a_OwneEa_a.plot(kind='bar', width=1, stacked=False
                                                    , alpha=1, color='#05445E', legend=None, ax=ax5, rasterized=False)
                # formatting
                g_OwnEa_a.set_xticks(df_temp_a_OwneEa_a.index, labels=df_temp_a_OwneEa_a['calendarYear'])
                g_OwnEa_a.set_xticklabels(g_OwnEa_a.get_xticklabels(), rotation=90, fontsize=5, color='white')
                g_OwnEa_a.set_yticks(g_OwnEa_a.get_yticks())
                g_OwnEa_a.set_title('Owners Earnings, annually', fontsize=8, color='white')
                g_OwnEa_a_ylabels = ['{:,}'.format(y) + ' M' for y in (g_OwnEa_a.get_yticks() / 1000000).astype('int64')]
                g_OwnEa_a.set_yticklabels(g_OwnEa_a_ylabels, size=5, color='white')
                g_OwnEa_a.tick_params(axis='x', colors='white')
                g_OwnEa_a.tick_params(axis='y', colors='white')
                g_OwnEa_a.yaxis.label.set_visible(False)
                g_OwnEa_a.xaxis.label.set_visible(False)
                g_OwnEa_a.spines['left'].set_color('none')
                g_OwnEa_a.spines['bottom'].set_color('none')
                g_OwnEa_a.set_facecolor('black')

                ### Description
                descr_str = df_temp_a['description'][0]
                today_and_desc = descr_str
                hor = 6.6/10
                ver = 1/2
                plt.figtext(hor, ver # location on plot in general
                            , today_and_desc
                            , verticalalignment='top'
                            , horizontalalignment='left'
                            , fontsize=11
                            , color='white'
                            , fontstyle='italic'
                            , wrap = True
                            , rasterized=False
                            )
            except:
                pass

        #######################
            # save plots as pdf
            plt.tick_params(axis='both', which='both', left=False, right=False, bottom=False, top=False, labelbottom=False)
            num_in_list = i+1
            num_in_list_str = str(num_in_list)
            underscore = '_'
            symbol_marg_pdf = df_temp_q['symbol'][0] + '.pdf'
            #output_raw = num_in_list_str + underscore + symbol_marg_pdf
            #print(output_raw)

            plt.savefig(os.path.join(cwd, input_folder, charts_folder, symbol_marg_pdf)
                        #, dpi=10
                        , facecolor='black'
                        )
            plt.tight_layout()
            #plt.show()
            #sys.exit()

            # reset
            mpl.rc_file_defaults()
            plt.close('all')

            print("plotted: " + ticker_str,' / ',  i+1, ' out of ',df_symbols.index[-1] + 1)

        #######################
            try:
                # start compressing
                #path to ghostscript = 'C:\Program Files\gs\gs9.56.1\bin'
                path_to_ghostscript = Path(os.path.join('C:\\Program Files\\gs\\gs9.56.1\\bin'))
                ticker_str_pdf = ticker_str + '.pdf'
                path_in_str = str(Path(os.path.join(cwd, input_folder, charts_folder, ticker_str_pdf)))
                #path to 4dots software = 'C:\Program Files (x86)\4dots Software\4dots Free PDF Compress\4dotsFreePDFCompress.exe'
                path_to_compressor = Path(
                    os.path.join('C:\\Program Files (x86)\\4dots Software\\4dots Free PDF Compress'))
                cmd = [
                    '4dotsFreePDFCompress.exe'
                    , path_in_str
                    , '/quality:15'
                    , '/overwrite'
                ]
                if os.path.isfile(path_in_str):
                    p = subprocess.run(cmd, cwd=path_to_compressor, shell=True)
                else:
                    pass
            except:
                pass
        else:
            pass
            #print('smth is wrong with ticker ' + df_temp_q['symbol'][0]+1)
    except UnicodeDecodeError as ue:
        print(str(ue))
        mpl.rc_file_defaults()
        plt.close('all')
        print('smth is wrong with ticker ' + df_temp_q['symbol'][0]+1)
        #test_q_ticker_csv = 'test_q_' + df_temp_q['symbol'][0] + '.csv'
        #df_temp_q.to_csv(os.path.join(cwd, input_folder, charts_folder, test_q_ticker_csv), index=False)
        #test_a_ticker_csv = 'test_a_' + df_temp_a['symbol'][0] + '.csv'
        #df_temp_a.to_csv(os.path.join(cwd, input_folder, charts_folder, test_a_ticker_csv), index=False)
        #sys.exit()