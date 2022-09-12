# Import the module
import pip
# pip.main(['install', 'requests'])
import os
import jinja2
import pandas as pd
import numpy as np
import datetime as dt
from IPython.display import display
from powerservice import trading

def saveToFinalLocation(finalLocation):
    return tradesFinal.to_csv(finalLocation)

dateToIngest = "10/09/2022"
todayDate = dt.datetime.today().strftime("%Y%m%d")
todayTime = dt.datetime.today().strftime("%H%M")
finalLocation = 'C:/Users/AdetayoOyebola/Downloads/Powerservice/PowerPosition_' + todayDate + '_' + todayTime + '.csv'

tradesapi = trading.get_trades(dateToIngest)
trades = pd.DataFrame(tradesapi)
trades['row_num'] = np.arange(len(trades))

# # Handle missing values for time series
# dataAndTime = [pd.date_range(dateToIngest + ' ' + "00:00",dateToIngest + ' ' +  "23:55", freq="5min")]

tradesExplode = trades.explode(['time','volume'])


tradesExplode['dateTime'] = pd.to_datetime(tradesExplode['date'] + ' ' + tradesExplode['time'])
tradesExplode['dateTimeLocal'] = tradesExplode['dateTime']  + pd.Timedelta(hours = -1)
tradesExplode['Local Time'] =  tradesExplode['dateTimeLocal'].dt.strftime('%H:00')
tradesFinal = tradesExplode[['Local Time','volume']]
tradesFinal = tradesFinal.groupby('Local Time').sum()
# display(tradesFinal)

# todayDate = dt.datetime.today().strftime("%Y%m%d")
# todayTime = dt.datetime.today().strftime("%H%M")
# trades.to_csv('C:/Users/AdetayoOyebola/Downloads/Powerservice/trades.csv')
# tradesExplode.to_csv('C:/Users/AdetayoOyebola/Downloads/Powerservice/PowerPosition.csv')
saveToFinalLocation(finalLocation)