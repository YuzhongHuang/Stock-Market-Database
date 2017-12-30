# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 10:12:57 2017

@author: Fei Ren
Details see trello board "任飞's Tasks" - card "Getting familiar with the ..."
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.sectorperformance import SectorPerformances

#%% load daily stock data from GOOGL, NVDA, TSLA, PG, BABA
myStocks = {
        "Google": None,
        "Nivada": None,
        "P&G": None,
        "Ali": None,
        "Tesla": None,
}
ts = TimeSeries(key='CAB2PSAH6XFZFA9C', output_format='pandas')
myStocks["Google"],_ = ts.get_daily(symbol='GOOGL')
myStocks["Nivada"],_ = ts.get_daily(symbol='NVDA')
myStocks["P&G"],_ = ts.get_daily(symbol='PG')
myStocks["Ali"],_ = ts.get_daily(symbol='BABA')
myStocks["Tesla"],_ = ts.get_daily(symbol='TSLA')

#%% Write Google's recent week (from 12/20)'s data to CSV file
toWrite = myStocks["Google"]
toWrite = toWrite[toWrite["date"]>"2017-12-19"]
toWrite.to_csv("Google_recent_week.csv", index = False)

#%% compare all sectors for past year and past 3 years with
# 5-number summary
pastYearStats = [None,None,None,None,None]
pastThreeYearsStats = [None,None,None,None,None]

sp = SectorPerformances(key='CAB2PSAH6XFZFA9C', output_format='pandas')
sectors,_ = sp.get_sector()
pastYearData = sectors["Rank F: Year-to-Date (YTD) Performance"]

# assign the 5 number summaries
pastYearStats[0] = pastYearData.min()
pastYearStats[2] = pastYearData.median()
pastYearStats[1] = pastYearData.quantile(q=0.25)
pastYearStats[3] = pastYearData.quantile(q=0.75)
pastYearStats[4] = pastYearData.max()


pastThreeYearsData = np.array(sectors.iloc[:,5:8])
pastThreeYearsData = np.nanmean(pastThreeYearsData, axis = 1)  # axis 1:
# every imbeded list
pastThreeYearsData = pd.Series(pastThreeYearsData)  # convert from array to series

pastThreeYearsStats[0] = pastThreeYearsData.min()
pastThreeYearsStats[2] = pastThreeYearsData.median()
pastThreeYearsStats[1] = pastThreeYearsData.quantile(q=0.25)
pastThreeYearsStats[3] = pastThreeYearsData.quantile(q=0.75)
pastThreeYearsStats[4] = pastThreeYearsData.max()

print('5-number summary for all sectors in the past year:\n')
print(pastYearStats)
print('5-number summary for all sectors in the past 3 years:\n')
print(pastThreeYearsStats)

#%% simulate trading for 10 days for 5 stocks
# parameters
initMoney = 10000

# Collect closing price from 8/31 - 9/8
prices = np.zeros([6,5])  # each row represent a day, each col represent
                           # each col represent a stock
prices[:,0] = myStocks["Google"]["close"][(myStocks["Google"]["date"]>"2017-08-30") 
              & (myStocks["Google"]["date"] < "2017-09-11")]
prices[:,1] = myStocks["Nivada"]["close"][(myStocks["Nivada"]["date"]>"2017-08-30") 
              & (myStocks["Nivada"]["date"] < "2017-09-11")]
prices[:,2] = myStocks["Tesla"]["close"][(myStocks["Tesla"]["date"]>"2017-08-30") 
              & (myStocks["Tesla"]["date"] < "2017-09-11")]
prices[:,3] = myStocks["P&G"]["close"][(myStocks["P&G"]["date"]>"2017-08-30") 
              & (myStocks["P&G"]["date"] < "2017-09-11")]
prices[:,4] = myStocks["Ali"]["close"][(myStocks["Ali"]["date"]>"2017-08-30") 
              & (myStocks["Ali"]["date"] < "2017-09-11")]

# calculate price change for each stock for each trading day
priceChange = np.zeros([5,5])
for i in range(5):  # iterate through stocks
    priceChange[:,i] = (prices[1:6,i]-prices[0:5,i])/prices[0:5,i]

# generate 5 actions vectors
# put stack them in a 2D array (5 x 6) with first column for money in 
# bank account (uninvested money)
np.random.seed(20172017)
actionMatrix = pd.DataFrame(np.random.rand(5, 6), columns = np.array(["Bank","Goog","Niv","Tesl","PG","Ali"]))

# normalize each row
for i in range(5):  # iterate through rows
    actionMatrix.iloc[i, :] = actionMatrix.iloc[i, :]*initMoney/sum(actionMatrix.iloc[i, :])
    
# calculate net profit for every trading day
profitMatrix = actionMatrix.iloc[:,1:] * priceChange
profit = profitMatrix.sum(axis = 1)  # 1D array with each element represents 
                                     # total net profit from all stocks in one trading day