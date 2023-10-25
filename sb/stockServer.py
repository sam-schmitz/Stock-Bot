#stockServer.py
#By: Sam Schmitz
#handles the storing and retriving of data from the sql server

import sb.stockChecker as sc
import pyodbc

class stockServer:

    def __init__(self, cnxn):
        #open the connection to the server
        self.cnxn = cnxn
        #print("connection established")
        self.cursor = self.cnxn.cursor()
        self._update_table_list()

    def get_date(self):
        """Gets the date/time for the most recent update to the server
        """
        self.cursor.execute("""SELECT Recent
        FROM Dates
        WHERE Trader='Overall'
        """)
        row = self.cursor.fetchone()
        print(row)
        return row[0]

    def new_trades(self, trades, same=False):
        """takes a list of trades and sorts them into buy and sell
        trades: a list of lists stored as returned by getTrades
        """
        print(trades)
        buy = []
        sell = []
        for trade in trades:
            if trade[0] != "N/A":   #some trades are US Treasury bonds and have a ticker of N/A (can't be bought)
                if trade[1] == "BUY":
                    buy.append(trade)
                else:
                    sell.append(trade)
        if same==False:
            self.buy_mixed(buy)
        else:
            self.buy_same(buy)
        self.sell_many(sell)

    def buy_mixed(self, trades):
        """stores a purchase with multiple traders
        trades: a list of lists stored as returned by getTrades, all BUY
        """
        _sort_trades(trades)
        hold = 0
        for t in range(0, len(trades)):
            if trades[t][4] == trades[t+1][4]:
                pass
            else:
                ts = []
                for y in range(hold, t+1):
                    ts.append(trades[y])
                self.buy_same(ts)
                hold = t+1


    def buy_same(self, trades):
        """stores a purchase with the same trader
        can be used for a single trade but it must be a list within a list [trade]
        trades: a list of lists stored as returned by getTrades, all BUY [trade, trade, trade]
        """
        tName = self._make_table_name(trades[0][4])
        print(trades)

        value = ""
        for trade in trades:
            value += "("
            priceB = sc.pPrice(trade[0], trade[2])
            priceR = sc.pPrice(trade[0], trade[3])
            price = priceR
            gap = int((trade[3] - trade[2]).days)
            gainB = price - priceB
            gainR = price - priceR
            sector = sc.stock_sector(trade[0])
            val = f"'{trade[4]}', '{trade[0]}', 'True', convert(datetime, '{trade[2]}'), convert(datetime, '{trade[3]}'), {priceB}, {priceR}, {gap}, {gainB}, {gainR}, '{sector}'"
            value += val
            value += "),"
        value = value[:-1]
        print("value:", value)

        self._store(tName, value)

    def _store(self, tName, value):
        """makes the query that inserts for a specified trader
        tName: the name for the trader
        value: a string that goes in the VALUES section of the query
        """
        if tName not in self.tables:
            self._update_table_list()
            if tName not in self.tables:
                self._create_table(tName, makeName=False)

        print("tName:", tName)
        print("test query: \n", f"""USE [CongressTrades]
            INSERT INTO {tName}
            ([Trader], [Tick], [Bought], [DateBought], [DateDis], [PriceB], [PriceR], [Gap], [GainB], [GainR], [Sector])
            VALUES
            {value};""")
        self.cursor.execute(f"""USE [CongressTrades]
            INSERT INTO {tName}
            ([Trader], [Tick], [Bought], [DateBought], [DateDis], [PriceB], [PriceR], [Gap], [GainB], [GainR], [Sector])
            VALUES
            {value};""")
        self.cnxn.commit()

    def sell_many(self, trades):
        """records multiple sales
        trades: a list of trades
        """
        for trade in trades:
            self.sell(trade)

    def sell(self, trade):
        """records a sale (singular)
        trade: a trade as given by getTrades [tick, saleType, dateBought, dateDis, member]
        """
        priceS = sc.pPrice(trade[0], trade[2])  #priceS = the price the trader sold at
        priceD = sc.pPrice(trade[0], trade[3])  #priceD = the price when the trade was disclosed
        tName = self._make_table_name(trade[4])

        self.cursor.execute(f"""USE [CongressTrades]
            SELECT PriceB, PriceR, TradeID
            FROM {tName}
            WHERE Tick='{trade[0]}'
            AND Bought='True'""")
        rows = self.cursor.fetchall()
        priceB = num(rows[-1][0])
        priceR = num(rows[-1][1])
        tradeID = num(rows[-1][2])

        gainR = priceD - priceR
        gainB = priceS - priceB

        self.cursor.execute(f"""USE [CongressTrades]
        UPDATE {tName}
        SET GainB = {gainB}, GainR = {gainR}, Bought = 'False'
        WHERE TradeID = {tradeID}
        """)

    #def close_server(self):
        #"""closes the server and updates values
        #"""
        #update the trade number counter
        #self.cursor.execute(f"""USE [CongressTrades]
            #UPDATE TradeIdNum
            #SET num = {self.tradeIdNum}
            #GO""")
        #self.cnxn.commit()"""

    def _redundant_trade(self, trade):
        """checks if a trade has already been made
        """
        return False

    def _create_table(self, name, makeName=True):
        """Creates a table based on the name of a congress member
        ex: name = 'Doe, John'
        """
        if makeName == True:
            name = self._make_table_name(name)
        print(name)
        self.cursor.execute(f"""CREATE TABLE {name} (
        TradeID int IDENTITY(1,1) PRIMARY KEY,
        Trader varchar(255),
        Tick varchar (255),
        Bought varchar(255),
        DateBought datetime,
        DateDis datetime,
        PriceB int,
        PriceR int,
        Gap int,
        GainB int,
        GainR int,
        Sector varchar(255)
        )""")
        self.cnxn.commit()
        self._update_table_list()

    def _make_table_name(self, name):
        """Generates the cooredsponding table name to a congress member's name"""
        return name.replace(" ", "")
        comPos = name.find(",")
        return name[0:comPos] + name[comPos+2:]

    def _update_table_list(self):
        """Updates the list of tables in the system
        This is done to check if a table exists in the database
        """
        self.cursor.execute(f"""SELECT TABLE_NAME
        FROM [CongressTrades].INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'""")
        #self.cnxn.commit()
        self.tables = []
        for name in self.cursor.fetchall():
            self.tables.append(name[0])
        print(self.tables)

#trade sorting methods

def _sort_trades(trades, l=0, r=None):
    """sorts a list of trades into alphabetical order by trader name
    uses quick sort, therefore recursive
    trades: a list of lists stored as returned by getTrades
    l:  the leftmost index
    r: the rightmost index
    """
    if r == None:
        r = len(trades) - 1
    if l < r:
        s = _partition_trades(trades, l, r)
        _sort_trades(trades, l, (s-1))
        _sort_trades(trades, (s+1), r)

def _partition_trades(trades, l, r):
    """helper function for _sort_trades()
    trades: a list of lists stored as returned by getTrades
    l:  the leftmost index
    r: the rightmost index
    """
    p = trades[r][4]
    i = l - 1
    for j in range(l, r):
        if (trades[j][4] <= p):
            i += 1
            trades[i], trades[j] = trades[j], trades[i]
    trades[i+1], trades[r] = trades[r], trades[i+1]
    return (i + 1)

if __name__ == "__main__":
    #[tick, saleType, dateBought, dateDis, member]
    from datetime import datetime
    server = 'DESKTOP-T05LAAR\SBSERVER'
    database = 'CongressTrades'
    username = 'ss'
    password = 'SuperSoaker#295'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=DESKTOP-T05LAAR\SBSERVER;DATABASE=CongressTrades;ENCRYPT=Optional;UID='+username+';PWD='+password+';')
    server = stockServer(cnxn)
    #trades = [['tick', 'BUY', 1, 1, 'ghi'], ['tick', 'BUY', 2, 2, 'jkl'], ['tick', 'SELL', 3, 3, 'abc'], ['tick', 'BUY', 4, 4, 'def']]
    #_sort_trades(trades)
    #print(trades)
    #server._create_table("test", makeName=False)
    #print("table made")
    #[Trader], [Tick], [Bought], [DateBought], [DateDis], [PriceB], [PriceR], [Gap], [GainB], [GainR], [Sector]
    trade = ['tick', 'BUY', datetime(2023, 6, 26), datetime(2023, 6, 26), "test"]
    #server.buy_same([trade])
    value = f"('{trade[4]}', '{trade[0]}', 'True', convert(datetime, '{trade[2]}'), convert(datetime, '{trade[3]}'), 22.00, 22.00, 0, 0, 0, 'test sector' \n)"
    server._store("test", value)
    print("stock stored")
