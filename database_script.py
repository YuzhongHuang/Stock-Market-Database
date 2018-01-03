# -*- coding: utf-8 -*-
"""
Created on Jan 2 2018

@author: Fei Ren
@brief: database of stocks' data for the deep learning algorithm.
@details:   Load stocks data from alpha vantage api. 
            Store data as dictionary with stock string IDs as keys.
            Implementation of querying and updating the data base.

"""
import numpy as np
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
#from alpha_vantage.sectorperformance import SectorPerformances

#%% class definitions

class data(object):
    """A class to hold all functions and attributes related to the database

    Attributes:
        stocks (dict): keys are stock ID's and values are price and volume data as tables.
        startDate (string): data before this date will not be loaded
    """
    startDate = "2012-01-01"
    stocks = {}  # ok to make stocks public??
    
#    def __init__(self, keyValPairs):
#        """
#        Args:
#            keyValPairs (dict): keys are stock IDs and values are corresponding tables.
#            
#        Constructor with parameters
#        """
#        self.stocks = keyValPairs

    def trim(self, rawData):
        """Only keep data after the given date. Simplify stock table format
        
        Args:
            rawData(pandas DataFrame): 20 years' full stock data with default
                                       row names.
        """
        # get a subset of data depending on startDate
        rawData = rawData[rawData['date']>=self.startDate]
        
        # reformat the table with dates as row names
        rawData.index = rawData.iloc[:,0]
        rawData = rawData.iloc[:,1:]
        
        return rawData

    # setter member functions
    def add_stock(self, stock_identification_string):
        """Add stock(s) to the database given a stock identification string or 
        a list of stock identification strings

        Args:
            stock_identification_string(list/string):  stock ID(s).        
        """
        ts = TimeSeries(key=apiKey, output_format='pandas')

        if isinstance(stock_identification_string, str):
            stock_identification_string = [stock_identification_string]
            
        # iterate through all stock IDs
        for id in stock_identification_string:
            rawData,_ = ts.get_daily(symbol=id, outputsize="full")        
            self.stocks[id] = self.trim(rawData)
                
            
#%% Module-level parameters
apiKey = "CAB2PSAH6XFZFA9C"
ids = ['GOOGL', 'TSLA', 'NVDA', 'PG', 'BABA', 'DAL', 'MMM', 'MGM', 'YELP', 'T' ]  # 10 test stocks on NYSE


#%% Test section
test = data()
test.add_stock('BABA')

#%% store 10 stocks' data locally for testing
test = data()
test.add_stock(ids)

