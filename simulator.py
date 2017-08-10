import datetime
import pandas as pd
from pandas_datareader import data, wb
import numpy as np
from scipy.signal import argrelextrema

# Testing libs
import matplotlib.pyplot as plt
import time

import owlbroker as ob
from portfolio import *
from stock import *


start_date = datetime.datetime(2017, 7, 1)
end_date = datetime.datetime(2017, 7, 31)
ticker_list = ["IBM", "AMZN", "TSLA"]
inital_fund = 50000
transaction_fee = 10

ss = Stock(inital_fund, ticker_list, start_date, end_date, transaction_fee)
ss.print_portfolio()

# TESTING HEAD AND SHOULDERS
ibm_data = ss.get_ticker('IBM')
## THIS DOES FIND THE HS PATTERN :)
hs_data = np.array([300, 310, 320, 350, 340, 315, 290, 295, 310, 330, 360, 330, 300, 295, 285, 320, 345, 346, 347, 348])
ss.ticker_data_list.append(['HS', ibm_data[1]])
print(ob.match_pattern(ss.ticker_data_list, 'HS', 'head_shoulders', hs_data))
## THIS DOES FIND THE DT PATTERN :)
dt_data = np.array([300, 280, 290, 300, 320, 360, 350, 340, 310, 290, 300, 320, 340, 365, 357, 343, 338, 317, 285, 280])
ss.ticker_data_list.append(['DT', ibm_data[1]])
print(ob.match_pattern(ss.ticker_data_list, 'DT', 'double_top', dt_data))
## THIS DOES FIND THE DB PATTERN :)
db_data = np.array([300, 310, 320, 315, 305, 360, 350, 340, 310, 290, 300, 320, 340, 330, 357, 343, 300, 317, 358, 364])
ss.ticker_data_list.append(['DB', ibm_data[1]])
print(ob.match_pattern(ss.ticker_data_list, 'DB', 'double_bottom', db_data))
