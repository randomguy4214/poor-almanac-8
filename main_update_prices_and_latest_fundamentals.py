#!/usr/bin/python

from datetime import datetime
start_time = datetime.now()

bundle_process = "bundle_process"
bundle_update = "bundle_update"
bundle_merge_output = "bundle_merge_output"
bundle_other = "bundle_other"
bundle_charts = "bundle_plots"

from bundle_other import put_reduced_symbols
from bundle_update import update_financials_q
from bundle_update import update_financials_a
from bundle_update import update_other
from bundle_update import update_EV
from bundle_update import update_commodities
from bundle_update import update_FED_balance_sheet

from bundle_process import process_financials_q
from bundle_process import process_financials_a
from bundle_process import process_other
from bundle_process import process_EV
from bundle_other import put_original_symbols

from bundle_merge_output import a_OwnEa_annually
from bundle_merge_output import a_OwnEa_quarterly
from bundle_merge_output import a_OwnEa_last_8_quarters
from bundle_merge_output import a_net_debt_to_equity
from bundle_merge_output import a_OwnEa

from bundle_update import update_prices
from bundle_process import process_prices
from bundle_other import put_latest_updated_date
from bundle_merge_output import a_recent_EV_prices_diff
from bundle_merge_output import output

from bundle_plots import plot_folder_setup
from bundle_plots import plot_commodities
from bundle_plots import plot_BS_FED
from bundle_plots import plot_BS_FED_b
from bundle_plots import plot_freight
from bundle_plots import plot_scatterplot_marg_of_safety
from bundle_plots import plot_companies
from bundle_plots import plots_to_pdf

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
