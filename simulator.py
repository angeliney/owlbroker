import datetime
import pandas as pd
from pandas_datareader import data, wb
import numpy as np
from scipy.signal import argrelextrema

# Testing libs
import matplotlib.pyplot as plt
import time

from portfolio import *

class StockSimulator():
    def __init__(self, inital_fund, tickerList, start_date, end_date, transaction_fee):
        """
        Create a new Stock Simulator.

        """
        self.tickerList = tickerList
        self.start_date = start_date
        self.end_date = end_date
        self.portfolio =  Portfolio(inital_fund,transaction_fee)
                
        self.ticker_data_list = []
        for ticker in tickerList:
            self.ticker_data_list.append([ticker, data.DataReader(ticker, "google", start_date, end_date)])
            
    def transaction_fee(self):
        return self.portfolio.transaction_fee
    
    def initial_fund(self):
        return self.portfolio.inital_fund
    
    def current_fund(self):
        return self.portfolio.fund
    
    def print_portfolio(self):
        return self.portfolio.print_portfolio()
    
    def get_ticker(self, ticker):
        for ticker_data in self.ticker_data_list:
            if ticker_data[0] == ticker:
                return ticker_data
        raise ValueError("Ticker not tracked")

    def get_ticker_moving_average(self, ticker):
        for ticker_data in self.ticker_data_list:
            if ticker_data[0] == ticker:
                ticker_data[1]['HL-MovAvg'] = ticker_data[1][['High', 'Low']].mean(axis=1)
                return ticker_data[1]['HL-MovAvg']
        raise ValueError("Ticker not tracked")
    
    def add_ticker(self, ticker):
        if ticker in self.tickerList:
            raise ValueError("Ticker already tracked")
        
        self.tickerList.append(ticker)
        self.ticker_data_list.append[ticker, data.DataReader(ticker, "google", start_date, end_date)]
    
    # hopefully we don't need to do threads
    def nextMinute():
        sleeptime = 60 - datetime.utcnow().second
        time.sleep(sleeptime)

    def match_helper(self, data, indices, pattern):
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

    def match_pattern(self, ticker, pattern_type, data):
        for ticker_data in self.ticker_data_list:
            if ticker_data[0] == ticker:
                #data = self.get_ticker_moving_average(ticker).values
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
                return self.match_helper(data, all_idx, pattern_type)
        raise ValueError("Ticker not tracked")
        
def main():
    start_date = datetime.datetime(2017, 7, 1)
    end_date = datetime.datetime(2017, 7, 31)
    ticker_list = ["IBM", "AMZN", "TSLA"]
    inital_fund = 50000
    transaction_fee = 10
    
    ss = StockSimulator(inital_fund, ticker_list, start_date, end_date, transaction_fee)
    ss.print_portfolio()
    
    # TESTING HEAD AND SHOULDERS
    ibm_data = ss.get_ticker('IBM')
    ## THIS DOES FIND THE HS PATTERN :)
    hs_data = np.array([300, 310, 320, 350, 340, 315, 290, 295, 310, 330, 360, 330, 300, 295, 285, 320, 345, 346, 347, 348])
    ss.ticker_data_list.append(['HS', ibm_data[1]])
    print(ss.match_pattern('HS', 'head_shoulders', hs_data))
    ## THIS DOES FIND THE DT PATTERN :)
    dt_data = np.array([300, 280, 290, 300, 320, 360, 350, 340, 310, 290, 300, 320, 340, 365, 357, 343, 338, 317, 285, 280])
    ss.ticker_data_list.append(['DT', ibm_data[1]])
    print(ss.match_pattern('DT', 'double_top', dt_data))
    ## THIS DOES FIND THE DB PATTERN :)
    db_data = np.array([300, 310, 320, 315, 305, 360, 350, 340, 310, 290, 300, 320, 340, 330, 357, 343, 300, 317, 358, 364])
    ss.ticker_data_list.append(['DB', ibm_data[1]])
    print(ss.match_pattern('DB', 'double_bottom', db_data))

    
    

if __name__ == "__main__":
    main()
