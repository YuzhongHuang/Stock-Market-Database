# Stock-Market-Database

A real-time self-updating database. The database tracks given stocks' prices and volumes in every minute from 2012-01-01 to present. Database is organized in a way that is convenient especially for deep learning training. Data will be collected through Alpha Vantage(Copyright © Alpha Vantage Inc. 2017). 

## Structure:
Outer structure: dictionary with stock ID string as key
Inner structure: pandas data frame with row names being time (up to which day) and high, low, open, close, volume as columns
data: stocks; history(); update(); add_stock();
- stock: 
  - date:
    - high, low, open, close, volume

### data.stocks
return a list of tracked stock identification strings

### data.history(self, start_date, end_year_date):
Given a start date and an end date, return a truncated data in the given time slot

### data.update(self):
Update the database with the stock market

### data.add_stock(self, stock_identification_string):
Add stock(s) to the database given a stock identification string or a list of stock identification strings
