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
Version 1.1: Added createServer, MemberTables, and refresh_server()
createServer.py : Created
adds the CongressTrades database to a server and sets it up
create_member_table adds a new member table to the db
stockServerV2: added refresh_server
the prices and profits in the server can now be updated using refresh_server
_update_member_tables was added to track trades by member and the profits they gained compared to our potential
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
