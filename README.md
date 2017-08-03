# owlbroker
csc384 assignment to decide when to buy, sell, or short stocks


# Data Structure (WIP)
Engine
```
def __init__(self, param1, param2, param3, param4, param5):
    Args:
        param1: List of symbols
        param2: start date
        param3: end date
        param4: amount
        param5: transaction fee (per action)
        
    
    Description
        - The engine will tick every minute simulating a live market
```


Getter methods:
```
def get_transactionfee() -> int:
```
```
def get_amount() -> int:
  - amount of money remaining
```
```
def get_portfolio() -> [ [symbol, amount, bought_date, bought_price, current_price]... ]
```

Action methods:
```
def buy(symbol,amount, target_upper_limit, target_lower_limit) -> bool
- buys the amount of stock of the symbol
- when either limit is reach, the stock is automatically sold (adjustable)
```
```
def sell(symbol, amount) -> bool
- sell the amount of stock of the symbol you own
```

Others:
```
def get_raw_data() -> 
Returns a list of tuples of timestamp and price.
[(2017-01-01 10:00, 100.23), (2017-01-01 10:01, 100.25) ...]
```


