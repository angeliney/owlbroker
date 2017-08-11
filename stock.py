import datetime
import pandas as pd
from pandas_datareader import data, wb
import numpy as np
from scipy.signal import argrelextrema
import time

from portfolio import *

class StockManagement():
    def __init__(self, inital_fund, ticker_list, start_date, end_date, transaction_fee, period, max_stocks=10):
        """
        Create a new Stock Simulator.

        """
        self.start_date = start_date
        self.end_date = end_date
        self.portfolio =  Portfolio(inital_fund,transaction_fee)
        self.max_investment = 1/max_stocks
        self.stocks = {}
        for ticker in ticker_list:
            self.add_ticker(ticker, start_date, end_date, period)


    def get_transaction_fee(self):
        return self.portfolio.transaction_fee

    def get_initial_fund(self):
        return self.portfolio.inital_fund

    def get_current_fund(self):
        return self.portfolio.fund

    def print_portfolio(self):
        return self.portfolio.print_portfolio()

    def get_ticker_data(self, ticker):
        if ticker in self.stocks:
            self.stocks[ticker].data
        else:
            raise ValueError("Ticker not tracked")

    def get_ticker_moving_average(self, ticker):
        if ticker in self.stocks:
            self.stocks[ticker].get_moving_average()
        else:
            raise ValueError("Ticker not tracked")

    def add_ticker(self, ticker, start_date, end_date, period):
        if ticker in self.stocks:
            raise ValueError("Ticker already tracked")

        self.stocks[ticker] = Stock(ticker, start_date, end_date, period)

    # hopefully we don't need to do threads
    def nextMinute():
        sleeptime = 60 - datetime.utcnow().second
        time.sleep(sleeptime)

class Stock():
    def __init__(self, ticker, start_date, end_date, period):
        self.ticker = ticker
        self.data = data.DataReader(ticker, "google", start_date, end_date)
        self.target_price = -1
        self.vol = 0
        self.profit_margin = -1
        self.current_price = -1
        self.start_date = start_date #datetime object
        self.end_date = end_date #datetime object
        self.period = period #integer

    def get_moving_average(self):
        self.data['HL-MovAvg'] = self.data[['High', 'Low']].mean(axis=1)
        return self.data['HL-MovAvg']

    # Return the date when price is within open and close
    def target_time(self):
        if (self.target_price < 0):
            return False

        # TODO check format of self.data and fix this
        day_count = 0
        for v1, v2 in self.data[['Open', 'Close']][self.period:]:
            if (self.target_price <= v1 and self.target_price >= v2) or (self.target_price >= v1 and self.target_price <= v2):
                return start_date + datetime.timedelta(days = period + day_count)
            day_count += 1

        return self.end_date
