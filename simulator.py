import time
import owlbroker as ob
import datetime as dt

# inputs, can be changed by user
ticker_list = ["IBM", "AMZN", "TSLA", "DUST", "NUGT", "DIS", "GMM", "LULU", "JDST", "EXPD", "CENX", "UGAZ", "UGLD", "DGLD"]
initial_fund = 100000
transaction_fee = 10
max_stocks = 1
period = 30

# Stock market only availabe 9:40am to 5pm Monday to Friday excluding US federal holidays
end_date = dt.datetime.today()
start_date = end_date - dt.timedelta(days=2*period)

ob.run(start_date, end_date, period, initial_fund, max_stocks, ticker_list, transaction_fee)


# Some sample data to test pattern matching functionality:
# # TESTING HEAD AND SHOULDERS
# ibm_data = ss.get_ticker('IBM')
# ## THIS DOES FIND THE HS PATTERN :)
# hs_data = np.array([300, 310, 320, 350, 340, 315, 290, 295, 310, 330, 360, 330, 300, 295, 285, 320, 345, 346, 347, 348])
# ss.ticker_data_list.append(['HS', ibm_data[1]])
# print(ob.match_pattern('head_shoulders', hs_data))
# ## THIS DOES FIND THE DT PATTERN :)
# dt_data = np.array([300, 280, 290, 300, 320, 360, 350, 340, 310, 290, 300, 320, 340, 365, 357, 343, 338, 317, 285, 280])
# ss.ticker_data_list.append(['DT', ibm_data[1]])
# print(ob.match_pattern('double_top', dt_data))
# ## THIS DOES FIND THE DB PATTERN :)
# db_data = np.array([300, 310, 320, 315, 305, 360, 350, 340, 310, 290, 300, 320, 340, 330, 357, 343, 300, 317, 358, 364])
# ss.ticker_data_list.append(['DB', ibm_data[1]])
# print(ob.match_pattern('double_bottom', db_data))
