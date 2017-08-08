import datetime
import pandas as pd
from pandas_datareader import data, wb

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
    
    def add_ticker(self, ticker):
        if ticker in self.tickerList:
            raise ValueError("Ticker already tracked")
        
        self.tickerList.append(ticker)
        self.ticker_data_list.append[ticker, data.DataReader(ticker, "google", start_date, end_date)]
    
    # hopefully we don't need to do threads
    def nextMinute():
        sleeptime = 60 - datetime.utcnow().second
        time.sleep(sleeptime)
        
def main():
    start_date = datetime.datetime(2017, 7, 1)
    end_date = datetime.datetime(2017, 7, 31)
    ticker_list = ["IBM", "AMZN", "TSLA"]
    inital_fund = 50000
    transaction_fee = 10
    
    ss = StockSimulator(inital_fund, ticker_list, start_date, end_date, transaction_fee)
    # TESTING
    IBM = ss.get_ticker('TSLA')
    IBM_data = IBM[1]
    IBM_data['HL-MovAvg'] = IBM_data[['High', 'Low']].mean(axis=1)
    ss.add_ticker(['GOOG'])
    ss.print_portfolio()
    
    
    
    

if __name__ == "__main__":
    main()
