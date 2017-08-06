class Portfolio():
    def __init__(self, fund, transaction_fee, initial_holding=[]):
        self.inital_fund = fund
        self.fund = fund
        self.holding = initial_holding
        self.transaction_fee = transaction_fee
        '''
        holding data structure:
        [ [ticker, current_volume, [[price_bought, volume, buy/sell, transaction_date]...]]... ]
        '''
        
    def buyStock(self, ticker, price, volume, date):
        total_price = (price * volume) + self.transaction_fee
        if total_price > self.fund:
            raise ValueError('Insufficent funds')
        
        self.fund -= total_price
        
        if ticker not in [item[0] for item in self.holding]:
            self.holding.append([ticker, volume, [[price, volume, "buy", date]]])
        else:        
            for each_holding in self.holding:
                if each_holding[0] == ticker:
                    each_holding[1] = each_holding[1] + volume
                    each_holding[2].append([price, volume, "buy", date])
                    break
    def sellStock(self, ticker, price, volume, date):
        if ticker not in [item[0] for item in self.holding]:
            raise ValueError(ticker,' unowned')
        
        change = (price*volume) - self.transaction_fee
        
        if self.fund + (price*volume) - self.transaction_fee < 0:
            raise ValueError("Insufficent for selling")
        
        for each_holding in self.holding:
            if each_holding[0] == ticker:
                if each_holding[1] < volume:
                    raise ValueError("Insufficent volume")
                each_holding[1] -= volume
                each_holding[2].append([price, volume, "sell", date])
                self.fund += change
                break        
    
    def print_portfolio(self):
        print("=======Funds=======")
        print("Initial\t ",self.inital_fund)
        print("Current\t ",self.fund)
        
        
        print("=======Transactions=======")
        if not self.holding:
            print("none")    
        else:
            for each_holding in self.holding:
                print(each_holding[0],"-","remaining shares:",each_holding[1])
                for transactions in each_holding[2]:
                    print("\t",transactions[2]," ",transactions[0]," ",transactions[1]," ",transactions[3])
    
        
            