import datetime
import pandas as pd
from pandas_datareader import data, wb
import numpy as np
from scipy.signal import argrelextrema
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

    def match_helper(self, data, indices):
        '''
        This function returns wether:
            1) E3 > E1 and E3 > E5
            and
            2) E1 and E5 are within 1.5 percent of their average
            and 
            3) E2 and E4 are within 1.5 percent of their average

        E1...E5 are the last 5 local max/min point
        '''
        e1 = data[indices[0]]
        e2 = data[indices[1]]
        e3 = data[indices[2]]
        e4 = data[indices[3]]
        e5 = data[indices[4]]
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

    def match_head_shoulders(self, ticker):
        for ticker_data in self.ticker_data_list:
            if ticker_data[0] == ticker:
                data = self.get_ticker_moving_average(ticker).values
                # order is the amount of data around a point to determine if is a local max/min
                max_idx = list(argrelextrema(data, np.greater, order=1)[0])
                min_idx = list(argrelextrema(data, np.less, order=1)[0])
                all_idx = max_idx + min_idx
                all_idx.sort()
                all_idx = all_idx[-5:]
                return self.match_helper(data, all_idx)
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
    ma = ss.get_ticker_moving_average('TSLA')
    ma[0] = 300
    ma[1] = 310
    ma[2] = 320
    ma[3] = 350
    ma[4] = 340
    ma[5] = 315
    ma[6] = 290
    ma[7] = 295
    ma[8] = 310
    ma[9] = 330
    ma[10] = 360
    ma[11] = 330
    ma[12] = 300
    ma[13] = 295
    ma[14] = 285
    ma[15] = 320
    ma[16] = 345
    ma[17] = 340
    ma[18] = 332
    ma[19] = 305
    ibm_data = ss.get_ticker('IBM')
    ibm_data[1]['HL-MovAvg'] = ma.values
    ss.ticker_data_list.append(['MYSTK', ibm_data[1]])
    data = ibm_data[1]['HL-MovAvg']
    ## THIS DOES FIND THE HS PATTERN :)
    #print(ss.match_head_shoulders('MYSTK', data.values))
    

if __name__ == "__main__":
    main()
