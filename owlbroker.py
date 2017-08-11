import datetime
import pandas as pd
from pandas_datareader import data, wb
import numpy as np
from scipy.signal import argrelextrema

# Testing libs
import matplotlib.pyplot as plt
import time
import math

from portfolio import *
from stock import *

PATTERNS = ["head_shoulders", "triangle", "double_top", "double_bottom"]
ORDERS = ["maxprofit", "maxvol", "minvol"]

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

        res = req_1 and req_2 and req_3

    elif pattern == 'triangles':
        res = False

    elif pattern == 'double_top':
        req_1 = (e2 - e1) > 0
        req_2 = (e3 - e2) < 0
        req_3 = (e4 - e3) > 0
        req_4 = (e5 - e4) < 0
        res = req_1 and req_2 and req_3 and req_4

    elif pattern == 'double_bottom':
        req_1 = (e2 - e1) < 0
        req_2 = (e3 - e2) > 0
        req_3 = (e4 - e3) < 0
        req_4 = (e5 - e4) > 0
        res = req_1 and req_2 and req_3 and req_4

    else:
        res = False

    return (res, e3, e4, e5)

def match_pattern(pattern_type, data):
    #data = ss.get_ticker_moving_average(ticker).values
    # order is the amount of data around a point to determine if is a local max/min
    max_idx = list(argrelextrema(data, np.greater, order=1)[0])
    min_idx = list(argrelextrema(data, np.less, order=1)[0])
    # added the very last data point as the future is unknown
    all_idx = max_idx + min_idx + [len(data)-1]
    all_idx.sort()
    all_idx = all_idx[-5:]
    # testing
    #plt.plot(data)
    #plt.scatter(all_idx, data[all_idx], c='r')
    #plt.show()
    return match_helper(data, all_idx, pattern_type)

def check_eligibility(sm, stock, e3, e4, e5, pattern):
    # Check if 10% of the investment modal is enough to purchase the company stock
    if (sm.get_current_fund() * 0.1 < e5):
        return False

    # Vol is the number of stocks we can buy.
    # We assume that the max amount we can spend on a company is max_investment of investment
    vol = math.floor((sm.get_current_fund() * sm.max_investment) / e5)

    # Check: Potential for profit needs to be greater than transaction fee
    if (abs(e3 - e4) * 0.9 < sm.get_transaction_fee()):
        return False

    profit_margin = abs(e5 - e3) * 0.8
    if profit_margin * vol > sm.get_transaction_fee():
        if e5 > e3:
            target_price = e5 - profit_margin
        else:
            target_price = e5 + profit_margin
    else:
        return False

    stock.vol = vol
    stock.target_price = target_price
    stock.profit_margin = profit_margin
    stock.current_price = e5
    return True

# Orders stock in different ways based on profits, volumes bought
def order(type, stock_list):
    if type == "maxprofit":
        newlist = sorted(stock_list, key=lambda x: x.vol * x.profit_margin, reverse=True)
    elif type == "maxvol":
        newlist = sorted(stock_list, key=lambda x: x.vol , reverse=True)
    elif type == "minvol":
        newlist = sorted(stock_list, key=lambda x: x.vol)
    else:
        newlist = stock_list
    return newlist

def eval(sm, p):
    for stockname, stock in sm.stocks.items():
        date = stock.target_time()
        if date:
            p.remove_stock(stockname, stock.data[-1], stock.vol, date)

    p.print_portfolio()

# Main function to run functionality of owl broker
def run(start_date, end_date, period, initial_fund, max_stocks, ticker_list, transaction_fee):
    sm = StockManagement(initial_fund, ticker_list, start_date, end_date, transaction_fee, period, max_stocks)

    stock_list=[]
    for stock_name in sm.stocks:
        stock = sm.stocks[stock_name]
        data = stock.get_moving_average().values
        for pattern in PATTERNS:
            result = match_pattern(pattern, data[0:stock.period-1])
            if result[0]:
                print("{} stock matches with pattern {}".format(stock.ticker, pattern))
                if check_eligibility(sm, stock, result[1], result[2], result[3], pattern):
                    stock_list.append(stock)

    for order_type in ORDERS:
        print("ordering stocks by {}".format(order_type))
        # Take top MAX_STOCKS investments
        lst = order(order_type, stock_list)[0:max_stocks-1]
        # Update portfolio
        p = Portfolio(initial_fund, transaction_fee)
        for stock in lst:
            p.add_stock(stock.ticker, stock.current_price, stock.vol, sm.start_date + datetime.timedelta(days = stock.period), stock.target_price)
        eval(sm, p)
