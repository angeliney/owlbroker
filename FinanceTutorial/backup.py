import time
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

stock_input = input("Please enter a list, comma separated, of stocks you are interested in : ")
stock_list = stock_input.split(",")
print(stock_list)

start = dt.datetime(2017,1,1)
# calculating and formating current date
current_year = int(time.strftime("%Y"))
current_month = time.strftime("%m")
if int(current_month) < 10:
    current_month = int(current_month[-1])
current_day = time.strftime("%d")
if int(current_day) < 10:
    current_day = int(current_day[-1])
end = dt.datetime(current_year,current_month,current_day)

df = web.DataReader('TSLA', 'yahoo', start, end)
#Moving average -100ma: last 100 averages to find trends
df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
df['100ma-H'] = df['High'].rolling(window=100, min_periods=0).mean()
df['100ma-L'] = df['Low'].rolling(window=100, min_periods=0).mean()
#df[['High', 'Low', '100ma-H', '100ma-L']].plot()
#plt.show()
print(df.tail())

##i = 0
##while i < 10:
##    print(web.get_quote_google('TSLA'))
##    time.sleep(60)
##    i += 1

