#testStockServer.py
#By: Sam Schmitz
#test code for stockServer.py

import unittest
from unittest.mock import (MagicMock, patch, Mock)
from datetime import datetime

import sb.stockServerV2

def _cPrice(tick):
        if tick == 'MSFT':
            return 100
        elif tick == 'AMZN':
            return 100
        elif tick == 'AAPL':
            return 100
        return None

def _pPrice(tick, d):
    if (tick=='MSFT'):
        if (d == datetime(2023, 8, 1)):
            return 20
        elif d == datetime(2023, 8, 15):
            return 40
        elif d == datetime(2023, 8, 25):
            return 60
        elif d == datetime(2023, 8, 30):
            return 80
        elif d == datetime(2023, 9, 1):
            return 100
    if tick == 'AMZN':
        if (d == datetime(2023, 8, 1)):
            return 20
        elif d == datetime(2023, 8, 15):
            return 40
        elif d == datetime(2023, 8, 25):
            return 60
        elif d == datetime(2023, 8, 30):
            return 80
        elif d == datetime(2023, 9, 1):
            return 100
    if tick == "AAPL":
        if (d == datetime(2023, 8, 1)):
            return 20
        elif d == datetime(2023, 8, 15):
            return 40
        elif d == datetime(2023, 8, 25):
            return 60
        elif d == datetime(2023, 8, 30):
            return 80
        elif d == datetime(2023, 9, 1):
            return 100

def _stock_sector(tick):
    if tick == 'MSFT':
        return "INFORMATION TECHNOLOGY"
    if tick == 'AMZN':
        raise Exception("could not find sector")

sb.stockServerV2.cPrice = _cPrice
sb.stockServerV2.pPrice = _pPrice
sb.stockServerV2.stock_sector = _stock_sector
sb.stockServerV2.create_member_table = MagicMock()
from sb.stockServerV2 import sbServer
    
class testStockServer(unittest.TestCase):

    @patch.object(sb.stockServerV2.datetime, 'datetime')

    def setUp(self, mock_datetime):
        self.cnxn = MagicMock()
        self.cnxn.cursor = MagicMock()
        self.cursor = self.cnxn.cursor
        self.cnxn.cursor.execute.side_effect = self.cursor_response
        mock_datetime.now.return_value = datetime(2023, 9, 1)
        #print("set-up:")
        #print("cnxn: ", self.cnxn)
        #print("cursor: ", self.cnxn.cursor)

        self.server = sbServer(self.cnxn, self.cursor)
        self.tradeBuy = ['MSFT', 'BUY', datetime(2023, 8, 1), datetime(2023, 8, 15), 'Joe Biden']
        self.tradeIDBuy = 1
        self.tradeSell = ['MSFT', 'SELL', datetime(2023, 8, 25), datetime(2023, 8, 30), 'Joe Biden']
        self.tradeIDSell = 2
        self.tradeBuy2 = ['AMZN', 'BUY', datetime(2023, 8, 1), datetime(2023, 8, 15), 'Joe Biden']
        self.tradeSell2 = ['AMZN', 'SELL', datetime(2023, 8, 25), datetime(2023, 8, 30), 'Joe Biden']
        self.tradeBuy3 = ['MSFT', 'BUY', datetime(2023, 8, 1), datetime(2023, 8, 15), 'Donald Trump']
        #MSFT is owned in the server
        #AMZN is not owned

    def cursor_response(self, sql):
        #print("cursor_response: ")
        #print("sql: ")
        #print(sql)
        if sql == (f"USE [CongressTrades]\n"
        f"SELECT BoughtPriceM, BoughtPriceU, TradeDelay\n"
        f"FROM BidenJoe\n"
        f"WHERE Tick='MSFT'\n"
        f"AND Owned='1'\n"):
            self.cursor.fetchall.return_value = [[20, 40, 14]]
        elif sql == (f"""USE [CongressTrades]
        SELECT COUNT(1)
        FROM BidenJoe
        WHERE Tick='AMZN'
        AND Owned='1';
        """):
            self.cursor.fetchall.return_value = [[0]]
            #print([[0]])
        elif sql == (f"""USE [CongressTrades]
        SELECT COUNT(1)
        FROM BidenJoe
        WHERE Tick='MSFT'
        AND Owned='1';
        """):
            self.cursor.fetchall.return_value = [[1]]
        elif sql == ("USE [CongressTrades]\n"
                "IF OBJECT_ID('BidenJoe', 'U') IS NOT NULL\n"
                "SELECT 1\n"
                "ELSE\n"
                "SELECT 0;"):
            self.cursor.fetchall.return_value = [[1]]
        elif sql == ("USE [CongressTrades]\n"
                "IF OBJECT_ID('TrumpDonald', 'U') IS NOT NULL\n"
                "SELECT 1\n"
                "ELSE\n"
                "SELECT 0;"):
            self.cursor.fetchall.return_value = [[0]]
        elif sql == ("USE [CongressTrades]\n" 
              "SELECT Tick, BoughtPriceM, BoughtPriceU\n"
              f"FROM BidenJoe\n"
              "WHERE Owned='1';"):
            self.cursor.fetchall.return_value = ([["MSFT", "20", "40"], 
                                                  ["AMZN", "20", "40"], 
                                                  ["AAPL", "30", "35"]])
        elif sql == ("USE [CongressTrades]\n"
                     "SELECT Tick, BoughtPriceM, BoughtPriceU\n"
                     "FROM ObamaBarak"
                     "WHERE Owned='1';"):
            self.cursor.fetchall.return_value = ([["MSFT", "20", "40"], 
                                                  ["AMZN", "20", "40"], 
                                                  ["AAPL", "30", "35"]])
        elif sql == ("USE [CongressTrades]\n"
                     "SELECT Tick, BoughtPriceM, BoughtPriceU\n"
                     "FROM BushGeorge"
                     "WHERE Owned='1';"):
            self.cursor.fetchall.return_value = ([["MSFT", "20", "40"], 
                                                  ["AMZN", "20", "40"], 
                                                  ["AAPL", "30", "35"]])
        elif sql == ("USE [CongressTrades]"
              "SELECT"
              "*"
              "FROM"
              "information_schema.tables;"):
            self.cursor.fetchall.return_value = (["BidenJoe", "TrumpDonald", "ObamaBarak", "Trades"])
        #else:
            #print("no response")

    def make_table_name(self, name):
            if name == "Joe Biden":
                return "BidenJoe"
            elif name == "Donald Trump":
                return 'TrumpDonald'
            elif name == "Barak Obama":
                return "ObamaBarak"
            elif name == "George Bush":
                return "BushGeorge"

    def table_exists(self, tName):
        if tName == "BidenJoe":
            return True
        elif tName == "TrumpDonald":
            return False
        elif tName == "ObamaBarak":
            return True
        elif tName == "BushGeorge":
            return True

    def test_member_buy_sql(self):
        self.server._member_buy('BidenJoe', self.tradeBuy)
        self.cnxn.cursor.execute.assert_called_once()

    def test_member_buy_price(self):
        self.tradeBuy.append(14)
        self.server._member_buy('BidenJoe', (self.tradeBuy))
        e = ("USE [CongressTrades]\n"
        f"INSERT INTO BidenJoe (Tick, ProfitMember, ProfitUS, BoughtPriceM, BoughtPriceU, Owned, TradeDelay)\n"
        f"VALUES ('MSFT', 400, 150, 20, 40, '1', 14);\n")
        self.cnxn.cursor.execute.assert_called()
        self.cnxn.cursor.execute.assert_called_once_with(e)

    def test_member_sell_server_called(self):
        self.tradeSell.append(5)
        self.server._member_sell('BidenJoe', self.tradeSell)
        #check if the server is called for stock info
        self.cnxn.cursor.execute.assert_called()
        #check if the server is called to input info
        self.cnxn.cursor.execute.assert_called()

    def test_member_sell_price(self):
        self.tradeSell.append(5)
        self.server._member_sell('BidenJoe', self.tradeSell)
        #check if the values ask for the Bought Prices is correct
        e1 = (f"USE [CongressTrades]\n"
        f"SELECT BoughtPriceM, BoughtPriceU, TradeDelay\n"
        f"FROM BidenJoe\n"
        f"WHERE Tick='MSFT'\n"
        f"AND Owned='1'\n")
        #self.cnxn.cursor.execute.assert_called_with(e1)
        #check if the values in the sql are correct for update
        e2 = (f"USE [CongressTrades]\n"
        f"UPDATE BidenJoe\n"
        f"SET ProfitMember = '200', ProfitUS = '50', Owned= '0', TradeDelay= 10\n"
        f"WHERE Tick='MSFT'\n"
        f"AND Owned='1';\n")
        self.cnxn.cursor.execute.assert_called_with(e2)
        execute_calls = self.cnxn.cursor.execute.call_args_list
        self.assertEqual(e1, execute_calls[0][0][0])

    def test_update_member_database_calls_select(self):
        self.server._update_member_database('BidenJoe', self.tradeBuy+[14])
        #see that the sql is correct for the select
        e = (f"""USE [CongressTrades]
        SELECT COUNT(1)
        FROM BidenJoe
        WHERE Tick='MSFT'
        AND Owned='1';
        """)
        self.cnxn.cursor.execute.assert_called_with(e)

    def test_update_member_databse_buy_unowned(self):
        self.tradeBuy2.append(14)
        self.server._update_member_database('BidenJoe', self.tradeBuy2)
        #see that it checks if the trade already is in the member database
            #assume it is not
        #check that it calls _member_buy
        e1 = (f"""USE [CongressTrades]
        SELECT COUNT(1)
        FROM BidenJoe
        WHERE Tick='AMZN'
        AND Owned='1';
        """)
        e2 = ("USE [CongressTrades]\n"
        f"INSERT INTO BidenJoe (Tick, ProfitMember, ProfitUS, BoughtPriceM, BoughtPriceU, Owned, TradeDelay)\n"
        f"VALUES ('AMZN', 400, 150, 20, 40, '1', 14);\n")
        self.cnxn.cursor.execute.assert_called_with(e2)
        execute_calls = self.cnxn.cursor.execute.call_args_list
        self.assertEqual(e1, execute_calls[0][0][0])

    def test_update_member_database_buy_owned(self):
        self.server._update_member_database('BidenJoe', self.tradeBuy+[14])
        #see that it checks if the trade is already in the db
            #it is
        self.cnxn.cursor.execute.assert_called_with("""USE [CongressTrades]
        SELECT COUNT(1)
        FROM BidenJoe
        WHERE Tick='MSFT'
        AND Owned='1';
        """)

    def test_update_member_databse_sell_owned(self):
        self.tradeSell.append(5)
        self.server._update_member_database('BidenJoe', self.tradeSell)
        e = (f"USE [CongressTrades]\n"
        f"UPDATE BidenJoe\n"
        f"SET ProfitMember = '200', ProfitUS = '50', Owned= '0', TradeDelay= 10\n"
        f"WHERE Tick='MSFT'\n"
        f"AND Owned='1';\n")
        self.cnxn.cursor.execute.assert_called_with(e)

    def test_update_member_databse_sell_unowned(self):
        self.server._update_member_database('BidenJoe', self.tradeSell2+[5])
        #the stock is not in the table
        self.cnxn.cursor.execute.assert_called_once_with("""USE [CongressTrades]
        SELECT COUNT(1)
        FROM BidenJoe
        WHERE Tick='AMZN'
        AND Owned='1';
        """)
        #see that it does nothing else

    def test_update_trade_databse_query_1(self):
        #test that the query for tradeBuy is correct
        self.tradeBuy.append('INFORMATION TECHNOLOGY')
        self.tradeBuy.append(14)
        self.server._update_trade_database(self.tradeBuy)
        self.cnxn.cursor.execute.assert_called_with("USE [CongressTrades]\n"
                                                    "INSERT INTO Trades (Tick, Member, TradeType, DateBoughtM, DateBoughtU, Department, TradeDelay)\n"
                                                    "VALUES ('MSFT', 'Joe Biden', 'BUY', convert(datetime, '2023-08-01 00:00:00'), convert(datetime, '2023-08-15 00:00:00'), 'INFORMATION TECHNOLOGY', 14);\n")

    def test_update_trade_database_query_2(self):
        #test that the query for tradeSell2 is correct
        self.tradeSell2.append('INFORMATION TECHNOLOGY')
        self.tradeSell2.append(5)
        self.server._update_trade_database(self.tradeSell2)
        self.cnxn.cursor.execute.assert_called_with("USE [CongressTrades]\n"
                                                    "INSERT INTO Trades (Tick, Member, TradeType, DateBoughtM, DateBoughtU, Department, TradeDelay)\n"
                                                    "VALUES ('AMZN', 'Joe Biden', 'SELL', convert(datetime, '2023-08-25 00:00:00'), convert(datetime, '2023-08-30 00:00:00'), 'INFORMATION TECHNOLOGY', 5);\n")

    def test_add_trade_calls_update(self):
        self.server._update_trade_database = MagicMock()
        self.server.add_trade(self.tradeBuy)
        self.server._update_trade_database.assert_called_once()

    def test_add_trade_calculate(self):
        self.server._update_trade_database = MagicMock()
        self.server.add_trade(self.tradeBuy)
        self.server._update_trade_database.assert_called_with(['MSFT', 'BUY', datetime(2023, 8, 1), datetime(2023, 8, 15), 'Joe Biden', 'INFORMATION TECHNOLOGY', 14])

    def test_add_trade_calculate_error(self):
        self.server._update_trade_database = MagicMock()
        self.server.add_trade(self.tradeBuy2)
        self.server._update_trade_database.assert_not_called()

    def test_add_trades_calls_add_trade(self):
        self.server.add_trade = MagicMock()
        self.server.add_trades([self.tradeBuy, self.tradeSell2])
        self.server.add_trade.assert_called()

    def test_add_trades_calls_multiple(self):
        self.server.add_trade = MagicMock()
        self.server.add_trades([self.tradeBuy, self.tradeSell2])
        execute_calls = self.server.add_trade.call_args_list
        self.assertEqual(self.tradeBuy, execute_calls[0][0][0])
        self.assertEqual(self.tradeSell2, execute_calls[1][0][0])

    def test_add_trade_calls_update_member_database(self):
        self.server._update_member_database = MagicMock()
        self.server._make_table_name = MagicMock()
        self.server._make_table_name.side_effect = self.make_table_name
        self.server.add_trade(self.tradeBuy)
        self.server._update_member_database.assert_called_once_with('BidenJoe', ['MSFT', 'BUY', datetime(2023, 8, 1), datetime(2023, 8, 15), 'Joe Biden', 'INFORMATION TECHNOLOGY', 14])
        self.server._make_table_name.assert_called_once_with('Joe Biden')

    def test_add_trade_checks_if_member_table_exists(self):
        self.server._update_member_database = MagicMock()
        self.server._make_table_name = MagicMock()
        self.server._make_table_name.side_effect = self.make_table_name
        self.server.add_trade(self.tradeBuy)
        self.cnxn.cursor.execute.assert_called_with("USE [CongressTrades]\n"
                "IF OBJECT_ID('BidenJoe', 'U') IS NOT NULL\n"
                "SELECT 1\n"
                "ELSE\n"
                "SELECT 0;")

    def test_add_trade_member_table_doesnt_exist(self):
        self.server._update_member_database = MagicMock()
        self.server._make_table_name = MagicMock()
        self.server._make_table_name.side_effect = self.make_table_name
        self.server.add_trade(self.tradeBuy3)
        self.server._update_member_database.assert_called_with('TrumpDonald', ['MSFT', 'BUY', datetime(2023, 8, 1), datetime(2023, 8, 15), 'Donald Trump', 'INFORMATION TECHNOLOGY', 14])
        sb.stockServerV2.create_member_table.assert_called()

    def test_make_table_name_correct(self):
        self.assertEqual(self.server._make_table_name('Joe Biden'), 'BidenJoe')
        self.assertEqual(self.server._make_table_name('Shelly Moore Capito'), 'MooreCapitoShelly')
        self.assertEqual(self.server._make_table_name('Mario Diaz-Balart Caballero'), 'Diaz-BalartCaballeroMario')

    def test_refresh_server_one_member(self):
        self.server._table_exists = MagicMock()
        self.server._table_exists = self.table_exists
        self.server._make_table_name = MagicMock()
        self.server._make_table_name.side_effect = self.make_table_name
        self.server.refresh_server("Joe Biden")
        self.server._make_table_name.assert_called_once_with("Joe Biden")
        e1 = ("USE [CongressTrades]\n" 
              "SELECT Tick, BoughtPriceM, BoughtPriceU\n"
              "FROM BidenJoe\n"
              "WHERE Owned='1';")
        e2 = ("USE [CongressTrades]\n" 
              "UPDATE BidenJoe\n"
              "SET ProfitMember='400', ProfitUS='150'\n"
              "WHERE Tick='MSFT'\n"
              "AND Owned='1';")
        e3 = ("USE [CongressTrades]\n" 
              "UPDATE BidenJoe\n"
              "SET ProfitMember='400', ProfitUS='150'\n"
              "WHERE Tick='AMZN'\n"
              "AND Owned='1';")
        e4 = ("USE [CongressTrades]\n" 
              "UPDATE BidenJoe\n"
              "SET ProfitMember='233', ProfitUS='186'\n"
              "WHERE Tick='AAPL'\n"
              "AND Owned='1';")
        execute_calls = self.cnxn.cursor.execute.call_args_list
        self.assertEqual(e1, execute_calls[0][0][0])
        self.assertEqual(e2, execute_calls[1][0][0])
        self.assertEqual(e3, execute_calls[2][0][0])
        self.assertEqual(e4, execute_calls[3][0][0])

    def test_refresh_server_one_member_no_exist(self):
        self.server._table_exists = MagicMock()
        self.server._table_exists = self.table_exists
        self.server._make_table_name = MagicMock()
        self.server._make_table_name.side_effect = self.make_table_name
        self.server.refresh_server("Donald Trump")
        self.server._make_table_name.assert_called_once_with("Donald Trump")
        self.cursor.execute.assert_not_called()

    def test_refresh_server_multiple_members(self):
        self.server._table_exists = MagicMock()
        self.server._table_exists = self.table_exists
        self.server._make_table_name = MagicMock()
        self.server._make_table_name.side_effect = self.make_table_name
        self.server.refresh_server(["Joe Biden", "Donald Trump", "Barak Obama", "George Bush"])
        e1 = ("USE [CongressTrades]\n" 
              "SELECT Tick, BoughtPriceM, BoughtPriceU\n"
              "FROM BidenJoe\n"
              "WHERE Owned='1';")
        e2 = ("USE [CongressTrades]\n" 
              "SELECT Tick, BoughtPriceM, BoughtPriceU\n"
              "FROM BushGeorge\n"
              "WHERE Owned='1';")
        e3 = ("USE [CongressTrades]\n" 
              "UPDATE BidenJoe\n"
              "SET ProfitMember='400', ProfitUS='150'\n"
              "WHERE Tick='MSFT'\n"
              "AND Owned='1';")
        e4 = ("USE [CongressTrades]\n" 
              "UPDATE ObamaBarak\n"
              "SET ProfitMember='400', ProfitUS='150'\n"
              "WHERE Tick='AMZN'\n"
              "AND Owned='1';")
        e5 = ("USE [CongressTrades]\n" 
              "UPDATE BushGeorge\n"
              "SET ProfitMember='233', ProfitUS='186'\n"
              "WHERE Tick='AAPL'\n"
              "AND Owned='1';")
        execute_calls = self.cnxn.cursor.execute.call_args_list
        self.assertEqual(e1, execute_calls[0][0][0])
        self.assertEqual(e2, execute_calls[8][0][0])
        self.assertEqual(e3, execute_calls[1][0][0])
        self.assertEqual(e4, execute_calls[6][0][0])
        self.assertEqual(e5, execute_calls[11][0][0])

    def test_refresh_server_no_members(self):
        self.server._refresh_member_tables = MagicMock()
        self.server.refresh_server()
        e1 = ("USE [CongressTrades]"
              "SELECT"
              "*"
              "FROM"
              "information_schema.tables;")
        self.cursor.execute.assert_called_with(e1)
        self.server._refresh_member_tables.assert_called_with(["BidenJoe", "TrumpDonald", "ObamaBarak"])

    def test_add_trades_calls(self):
        self.server.add_trade = MagicMock()
        self.server.refresh_server = MagicMock()
        self.server.add_trades([self.tradeBuy])
        self.server.refresh_server.assert_called()


if __name__ == "__main__":
    unittest.main()
