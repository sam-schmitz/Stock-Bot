#testCreateServer.py
#By: Sam Schmitz
#test code for createServer.py

import unittest
from unittest.mock import MagicMock

import sb.createServer

class testCreateServer(unittest.TestCase):

    def setUp(self):
        self.cnxn = MagicMock()
        self.cnxn.cursor = MagicMock()
        self.cursor = self.cnxn.cursor()

    def test_create_server_makes_database(self):
        sb.createServer.create_server(self.cnxn, self.cursor)
        e1 = ("CREATE DATABASE CongressTrades")
        execute_calls = self.cursor.execute.call_args_list
        self.assertEqual(e1, execute_calls[0][0][0])

    def test_create_server_makes_trades_table(self):
        sb.createServer.create_server(self.cnxn, self.cursor)
        self.cursor.execute.assert_called_with("USE [CongressTrades]"
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

    def test_create_member_table(self):
        sb.createServer.create_member_table(self.cnxn, self.cursor, "BidenJoe")
        self.cursor.execute.assert_called_with("USE [CongressTrades]"
                                               "CREATE TABLE BidenJoe("
                                               "Tick char(10) NOT NULL"
                                               "Crossover(bit)"
                                               "ProfitMember float NOT NULL"
                                               "ProfitUS float NOT NULL"
                                               "BoughtPriceM float NOT NULL"
                                               "BoughtPriceU float NOT NULL"
                                               "Owned bit NOT NULL"
                                               "TradeDelay int NOT NULL"
                                               ");")
