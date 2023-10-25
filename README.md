# Stock-Bot
Description: Tracks the stock trades made by members of congress. Uses Selenium, python requests, and Beautiful Soup 4 to scrape data. Data is then processed into a SQL database using pyodbc.
Stock data is sourced from Yahoo Finance. Trades are from captioltrades.com and information about congress members is from congress.gov

Programs:
congressTrades.py:
Uses selenium to gather trade data from capitoltrades.com. This is done through getTrades(). 
skatepark.py: 
The bot itself. Function sb() gathers and stores the data. On init a command line interface can be brought up
stockChecker.py:
Uses BS4 to gather stock prices and other information from Yahoo Finance
stockServerV2.py:
A wrapper object for a pyodbc connection. Stores the stock data in the SQL server

Versions: 
Verison 1.0: Initial Version
This is a new verion of an old project I had created. Most programs were reworked to improve efficiency and add a SQL database. 
congressTrades.py: Created
Uses selenium to gather trade data from capitoltrades.com. This is done through getTrades(). 
skatepark.py: Created
The bot itself. Function sb() gathers and stores the data. On init a command line interface can be brought up
stockChecker.py: Created
Uses BS4 to gather stock prices and other information from Yahoo Finance
stockServerV2.py: Created
A wrapper object for a pyodbc connection. Stores the stock data in the SQL server
