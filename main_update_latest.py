#!/usr/bin/python

from datetime import datetime
start_time = datetime.now()

bundle_process = "bundle_process_first_time"
bundle_update = "bundle_update"
bundle_merge_output = "bundle_merge_output"
bundle_other = "bundle_other"
bundle_charts = "bundle_plots"

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))