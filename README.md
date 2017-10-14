# Stock-Market-Database

A real-time self-updating database. The database tracks given stocks' prices and volumes in every minute from 2012-01-01 to present. Database is organized in a way that is convenient especially for deep learning training. Data will be collected through Alpha Vantage(Copyright © Alpha Vantage Inc. 2017). 

## Structure:

data: stocks; history(); update(); add_stock();
- stock: 
  - year:
    - date:
      - price list
      - volume list

### data.stocks
return a list of tracked stock identification strings

### data.history(self, start_date, end_year_date):
Given a start date and an end date, return a truncated data in the given time slot

### data.update(self):
Update the database with the stock market

### data.add_stock(self, stock_identification_string):
Add stock(s) to the database given a stock identification string or a list of stock identification strings
