#!/usr/bin/python
bundle_main = "bundle_main"
from bundle_main import checks
# multithreaded import of prices and fundamentals.
from threading import Thread
def a():
    from bundle_main import update_prices
    from bundle_main import process_prices
def b():
    from bundle_main import update_financials_q
    from bundle_main import process_financials_q
def c():
    from bundle_main import update_financials_a
    from bundle_main import process_financials_q

# initiate multithreading
Thread(target=a).start()
Thread(target=b).start()
Thread(target=c).start()

# wait until they will finish
Thread(target=a).join()
Thread(target=b).join()
Thread(target=c).join()

from bundle_main import datasets_merge
from bundle_main import output