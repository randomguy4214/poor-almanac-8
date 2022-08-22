#!/usr/bin/python

from datetime import datetime
start_time = datetime.now()

bundle_process = "bundle_process_first_time"
bundle_update = "bundle_update"
bundle_merge_output = "bundle_merge_output"
bundle_other = "bundle_other"
bundle_charts = "bundle_plots"

from bundle_other import put_reduced_symbols

from bundle_update import update_financials_a
from bundle_update import update_financials_q
from bundle_update import update_other
from bundle_update import update_EV
from bundle_update import update_commodities
from bundle_update import update_FED_balance_sheet
#from bundle_update import update_sec_fillings

from bundle_process_incremental import process_financials_a_incr
from bundle_process_incremental import process_financials_q_incr
from bundle_process_incremental import process_other_incr
from bundle_process_incremental import process_EV_incr

from bundle_merge_output import a_OwnEa_annually
from bundle_merge_output import a_OwnEa_quarterly
from bundle_merge_output import a_OwnEa_last_8_quarters
from bundle_merge_output import a_net_debt_to_equity
from bundle_merge_output import a_OwnEa

from bundle_update import update_prices
from bundle_process_first_time import process_prices
from bundle_merge_output import a_recent_EV_prices_diff
from bundle_merge_output import output

from bundle_process_incremental import process_plot_folder_setup
from bundle_plots import plot_commodities
from bundle_plots import plot_BS_FED
from bundle_plots import plot_BS_FED_b
from bundle_plots import plot_freight
from bundle_plots import plot_scatterplot_marg_of_safety
from bundle_process_incremental import process_pdfs_reduce_size_for_non_stock

from bundle_plots import plot_companies_incr
from bundle_update import update_new_plots_to_all_plots_folder
from bundle_pdf import pdfs_all_to_one
#from bundle_process_first_time import process_pdfs_reduce_size

from bundle_other import put_original_symbols
from bundle_update import put_latest_updated_date

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
