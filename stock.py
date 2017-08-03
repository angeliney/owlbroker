class Stock:
'''Class for defining stock data structure. On initialization the
       stock object should be given a name. Stock prices can be added later on.
'''
    #
    #set up and info methods
    #
    def __init__(self, name, prices=[]):
        '''Create a stock object, specifying its name (a
        string). Optionally specify available stock price history.
        '''
        self.name = name                #text name for variable
        self.prices = list(prices)         #Make a copy of passed domain
        self.assignedAction = None

    def add_prices(self, values):
        '''Add additional prices to the domain.
           Removals are not supported.'''
        for val in values:
            self.dom.append(val)
            self.curdom.append(True)

    def price_size(self):
        '''Return the size of the (permanent) prices stored'''
        return(len(self.prices))

    def domain(self):
        '''return the variable's (permanent) domain'''
        return(list(self.dom))
