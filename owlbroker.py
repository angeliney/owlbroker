import datetime
import pandas as pd
from pandas_datareader import data, wb
import numpy as np
from scipy.signal import argrelextrema

# Testing libs
import matplotlib.pyplot as plt
import time

from portfolio import *

def match_helper(data, indices, pattern):
    """
    data: list of ticker values
    indices: indices where peaks occur
    pattern: which pattern to match (head_shoulders, triangles, double_top, or double_bottom)

    E1...E5 are the last 5 local max/min point

    Head and Shoulders pattern returns wether:
        1) E3 > E1 and E3 > E5
        and
        2) E1 and E5 are within 1.5 percent of their average
        and
        3) E2 and E4 are within 1.5 percent of their average


    Double Top pattern return wether:
        Data formes a M patther, that is:
        1) E2 - E1 is possitive
        2) E3 - E2 is negative
        3) E4 - E3 is possitive
        4) E5 - E4 is negative
    """

    e1 = data[indices[0]]
    e2 = data[indices[1]]
    e3 = data[indices[2]]
    e4 = data[indices[3]]
    e5 = data[indices[4]]

    if pattern == 'head_shoulders':
        # req 1: E3>E1,E3>E
        req_1 = e3 > e1 and e3 > e5

        # req 2: E1 and E5 are within 1.5 percent of their average
        e1_e5_avg = (e1 + e5) / 2
        percent = e1_e5_avg * 0.015
        lower_bound = e1_e5_avg - percent
        upper_bound = e1_e5_avg + percent
            # E1 and E5 are >= lower bound
        e1_lower = lower_bound <= e1
        e5_lower = lower_bound <= e5
            # E1 and E5 are <= upper bound
        e1_upper = upper_bound >= e1
        e5_upper = upper_bound >= e5

        req_2 = e1_lower and e5_lower and e1_upper and e5_upper

        # req 3: E2 and E4 are within 1.5 percent of their average
        e2_e4_avg = (e2 + e4) / 2
        percent_2 = e2_e4_avg * 0.015
        lb = e2_e4_avg - percent_2
        ub = e2_e4_avg + percent_2
            # E2 and E4 are >= lower bound
        e2_lower = lb <= e2
        e4_lower = lb <= e4
            # E2 and E4 are >= lower bound
        e2_upper = ub >= e2
        e4_upper = ub >= e4

        req_3 = e2_lower and e4_lower and e2_upper and e4_upper

        return req_1 and req_2 and req_3

    if pattern == 'triangles':
        return False

    if pattern == 'double_top':
        req_1 = (e2 - e1) > 0
        req_2 = (e3 - e2) < 0
        req_3 = (e4 - e3) > 0
        req_4 = (e5 - e4) < 0
        return req_1 and req_2 and req_3 and req_4

    if pattern == 'double_bottom':
        req_1 = (e2 - e1) < 0
        req_2 = (e3 - e2) > 0
        req_3 = (e4 - e3) < 0
        req_4 = (e5 - e4) > 0
        return req_1 and req_2 and req_3 and req_4

def match_pattern(ticker_data_list, ticker, pattern_type, data):
    for ticker_data in ticker_data_list:
        if ticker_data[0] == ticker:
            #data = get_ticker_moving_average(ticker).values
            # order is the amount of data around a point to determine if is a local max/min
            max_idx = list(argrelextrema(data, np.greater, order=1)[0])
            min_idx = list(argrelextrema(data, np.less, order=1)[0])
            # added the very last data point as the future is unknown
            all_idx = max_idx + min_idx + [len(data)-1]
            all_idx.sort()
            all_idx = all_idx[-5:]
            # testing
            plt.plot(data)
            plt.scatter(all_idx, data[all_idx], c='r')
            plt.show()
            return match_helper(data, all_idx, pattern_type)
    raise ValueError("Ticker not tracked")
