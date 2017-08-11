class Portfolio():
    def __init__(self, fund, transaction_fee, initial_holding={}):
        self.inital_fund = fund
        self.fund = fund
        self.holding = initial_holding
        self.transaction_fee = transaction_fee
        '''
        holding data structure:
         {ticker: current_volume, [[price_bought, volume, buy/sell, transaction_date]...]] }
        '''

    def add_stock(self, ticker, price, volume, date, sell_price):
        total_price = (price * volume) + self.transaction_fee
        if total_price > self.fund:
            raise ValueError('Insufficent funds')

        self.fund -= total_price

        if ticker not in self.holding:
            self.holding[ticker] = [volume, [[price, volume, "buy", date]]]
        else:
            each_holding = self.holding[ticker]
            each_holding[0] = each_holding[0] + volume
            each_holding[1].append([price, volume, "buy", date])

    def remove_stock(self, ticker, price, volume, date):
        if ticker not in self.holding:
            raise ValueError(ticker,' unowned')

        change = (price*volume) - self.transaction_fee

        if self.fund + (price*volume) - self.transaction_fee < 0:
            raise ValueError("Insufficent for selling")

        each_holding = self.holding[ticker]
        if each_holding[1] < volume:
            raise ValueError("Insufficent volume")
        each_holding[0] -= volume
        each_holding[1].append([price, volume, "sell", date])
        self.fund += change

    def print_portfolio(self):
        print("=======Funds=======")
        print("Initial\t ",self.inital_fund)
        print("Current\t ",self.fund)


        print("=======Transactions=======")
        if not self.holding:
            print("none")
        else:
            for ticker, each_holding in self.holding.items():
                print(ticker,"-","remaining shares:",each_holding[0])
                for transactions in each_holding[1]:
                    print("\t",transactions[2]," ",transactions[0]," ",transactions[1]," ",transactions[3])
