#createServer.py
#By: Sam Schmitz
#creates a server for skatepark to use

import pyodbc

def create_server(cnxn, cursor):
    _create_database(cnxn, cursor)

def create_member_table(cnxn, cursor, tName):
    cursor.execute("USE [CongressTrades]"
                        f"CREATE TABLE {tName}("
                        "Tick char(10) NOT NULL"
                        "Crossover(bit)"
                        "ProfitMember float NOT NULL"
                        "ProfitUS float NOT NULL"
                        "BoughtPriceM float NOT NULL"
                        "BoughtPriceU float NOT NULL"
                        "Owned bit NOT NULL"
                        "TradeDelay int NOT NULL"
                        ");")
    cnxn.commit()

def _create_database(cnxn, cursor):
    cursor.execute("CREATE DATABASE CongressTrades")
    cursor.execute("USE [CongressTrades]"
                    "CREATE TABLE Trades("
                    "Tick varchar(10) NOT NULL"
                    "Member char(30) NOT NUll"
                    "TradeType char(10) NOT NULL"
                    "DateBoughtM date NOT NULL"
                    "DateBoughtU date NOT NULL"
                    "TradeID int IDENTITY(1,1) PRIMARY KEY"
                    "Department char(30) NOT NULL"
                    "Sector char(30)"
                    "TradeDelay int NOT NULL"
                    ");")
    cnxn.commit()

if __name__ == "main":
    print("enter the server name: ")
    server = input()
    print("enter the username: ")
    username = input()
    print("enter the password: ")
    password = input()
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=DESKTOP-T05LAAR\SBSERVER;ENCRYPT=Optional;UID='+username+';PWD='+password+';')
    create_server(cnxn, cnxn.cursor())
