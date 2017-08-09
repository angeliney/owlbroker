import datetime
import pandas as pd
from pandas_datareader import data, wb
import numpy as np
from scipy.signal import argrelextrema

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

    def match_head_shoulders_helper(head_shoulder_df):
        '''
        This function returns wether:
            1) E1 and E5 are within 1.5 percent of their average
            and 
            2) E2 and E4 are within 1.5 percent of their average

        E1...E5 are the 3 highest and 2 lowest data points
        '''
        # E1 and E5 are within 1.5 percent of their average
        e1_e5_avg = (head_shoulder_df[1] + head_shoulder_df[5]) / 2
        percent = e1_e5_avg * 0.015
        lower_bound = e1_e5_avg - percent
        higher_bound = e1_e5_avg + percent
            # E1 and E5 are >= lower bound
        e1_lower = lower_bound <= head_shoulder_df[1]
        e5_lower = lower_bound <= head_shoulder_df[5]
            # E1 and E5 are <= upper bound
        e1_upper = upper_bound >= head_shoulder_df[1]
        e5_upper = upper_bound >= head_shoulder_df[5]
        if e1_lower and e5_lower and e1_upper and e5_upper:
            # E2 and E4 are within 1.5 percent of their average
            e2_e4_avg = (head_shoulder_df[2] + head_shoulder_df[4]) / 2
            percent_2 = e2_e4_avg * 0.015
            lb = e2_e4_avg - percent_2
            ub = e2_e4_avg + percent_2
                # E2 and E4 are >= lower bound
            e2_lower = lb <= head_shoulder_df[2]
            e4_lower = lb <= head_shoulder_df[4]
                # E2 and E4 are >= lower bound
            e2_upper = ub >= head_shoulder_df[2]
            e4_upper = ub >= head_shoulder_df[4]
            return e2_lower and e4_lower and e2_upper and e4_upper
        return False

    def match_head_shoulders(self, ticker):
        for ticker_data in self.ticker_data_list:
            if ticker_data[0] == ticker:
                # From moving average, get the 3 highest and the 2 lowest points
                mov_avg = self.get_ticker_moving_average(ticker)
                ups = mov_avg.nlargest(3)
                downs = mov_avg.nsmallest(2)
                head_shoulder = pd.concat([ups, downs])
                head_shoulder_s = head_shoulder.sort_index()
                ## Based on this link: https://quant.stackexchange.com/questions/1937/how-to-identify-technical-analysis-chart-patterns-algorithmically
                if head_shoulder_s[1] in ups and head_shoulder_s[3] > head_shoulder_s[1] and head_shoulder_s[3] > head_shoulder_s[5]:
                    return self.match_head_shoulders_helper(head_shoulder_s)
                else:
                    return False
        raise ValueError("Ticker not tracked")
        
def main():
    start_date = datetime.datetime(2017, 7, 1)
    end_date = datetime.datetime(2017, 7, 31)
    ticker_list = ["IBM", "AMZN", "TSLA"]
    inital_fund = 50000
    transaction_fee = 10
    
    ss = StockSimulator(inital_fund, ticker_list, start_date, end_date, transaction_fee)
    ss.print_portfolio()
    # TESTING
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
    ibm = ss.get_ticker('IBM')
    my_t = ['myt', ma]
    print(ibm)
    print(my_t)
    print(ss.match_head_shoulders(my_t))
    

if __name__ == "__main__":
    main()
