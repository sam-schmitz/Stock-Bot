#stockServerV2.py
#By: Sam Schmitz

from stockChecker import cPrice, pPrice, stock_sector


class sbServer:

    def __init__(self, cnxn, cursor):
        #open the connection to the server
        self.cnxn = cnxn
        self.cursor = cursor

    def add_trades(self, trades):
        #adds a list of trades to the server
        for trade in trades:
            response = self.add_trade(trade)
            if response != None:
                print("error: ", response)
        #self.refresh_server()

    def add_trade(self, trade):
        delay = -1
        try:
            #calculate department
            department = stock_sector(trade[0])
            print(department)
            trade.append(department)
            #calculate delay
            delay = int((trade[3] - trade[2]).days)
            trade.append(delay)
            print(delay)
            #tradeID = self._update_trade_database(trade)
        except:
            return trade
        if delay > -1:
            tradeID = self._update_trade_database(trade)
            self.cnxn.commit()
            tName = self._make_table_name(trade[4])
            e1 = ("USE [CongressTrades]\n"
                f"IF OBJECT_ID('{tName}', 'U') IS NOT NULL\n"
                "SELECT 1\n"
                "ELSE\n"
                "SELECT 0;")
            self.cursor.execute(e1)
            while self.cursor.nextset():
                try:
                    rows = self.cursor.fetchall()
                    break
                except pyodbc.ProgrammingError:
                    continue
            myresult = rows[-1][-1]
            if myresult != 1:
                print("table not found: ", tName)
            else:
                self._update_member_database(tName, trade)
        #find memberDatabase
        #self._update_member_database(table, trade, tradeID)

    def refresh_server(self):
        #updates the member databases
        self._refresh_member_databases()

    def close(self):
        self.cursor.close()
        self.cnxn.close()

    def _update_trade_database(self, trade):
        self.cursor.execute("USE [CongressTrades]\n"
        "INSERT INTO Trades (Tick, Member, TradeType, DateBoughtM, DateBoughtU, Department, TradeDelay)\n"
        f"VALUES ('{trade[0]}', '{trade[4]}', '{trade[1]}', convert(datetime, '{trade[2]}'), convert(datetime, '{trade[3]}'), '{trade[5]}', {trade[6]});\n")

    def _update_member_database(self, table, trade):
        #determine if owned
        e1 = (f"""USE [CongressTrades]
        SELECT COUNT(1)
        FROM {table}
        WHERE Tick='{trade[0]}'
        AND Owned='1';
        """)
        self.cursor.execute(e1)
        while self.cursor.nextset():
            try:
                rows = self.cursor.fetchall()
                break
            except pyodbc.ProgrammingError:
                continue
        myresult = rows[-1][-1]     #if == 1 the stock is owned
        if myresult == 1:
            if trade[1] == "SELL":
                self._member_sell(table, trade)
                self._update_stock_database(trade[0], trade[1])
        else:
            #print("trade[1]", trade[1])
            if trade[1] == "BUY":
                self._member_buy(table, trade)
                self._update_stock_database(trade[0], trade[1])
        #update the stock database
        #self._update_DB_of_members(member)

    def _member_buy(self, table, trade):
        #get the current price
        cp = cPrice(trade[0])
        #get the bought price member
        pp1 = pPrice(trade[0], trade[2])
        #get the bought price us
        pp2 = pPrice(trade[0], trade[3])
        #calculate the % profit member
        profitM = round(((cp-pp1)/pp1) * 100)
        #calculate % profit us (should be 0)
        profitU = round(((cp-pp2)/pp2) * 100)
        #add a new row to the table
        e = (f"USE [CongressTrades]\n"
        f"INSERT INTO {table} (Tick, ProfitMember, ProfitUS, BoughtPriceM, BoughtPriceU, Owned, TradeDelay)\n"
        f"VALUES ('{trade[0]}', {profitM}, {profitU}, {pp1}, {pp2}, '1', {trade[-1]});\n")
        self.cursor.execute(e)

    def _member_sell(self, table, trade):
        #get the data from the server
        self.cursor.execute(f"USE [CongressTrades]\n"
        f"SELECT BoughtPriceM, BoughtPriceU, TradeDelay\n"
        f"FROM {table}\n"
        f"WHERE Tick='{trade[0]}'\n"
        f"AND Owned='1'\n")
        rows = self.cursor.fetchall()
        #print(rows)
        boughtPriceM, boughtPriceU, tradeDelay = rows[-1][0], rows[-1][1], rows[-1][2]
        #calculate the new % profits
        pp1 = pPrice(trade[0], trade[2])
        pp2 = pPrice(trade[0], trade[2])
        profitM = round(((pp1-boughtPriceM)/boughtPriceM)*100)
        profitU = round(((pp2-boughtPriceU)/boughtPriceU)*100)
        tradeDelay = round((tradeDelay + int(trade[-1])) / 2)
        #update member database
        self.cursor.execute(f"USE [CongressTrades]\n"
        f"UPDATE {table}\n"
        f"SET ProfitMember = '{profitM}', ProfitUS = '{profitU}', Owned= '0', TradeDelay= {tradeDelay}\n"
        f"WHERE Tick='{trade[0]}'\n"
        f"AND Owned='1';\n")

    def _update_DB_of_members(self, member):
        pass
        #number of trades += 1
        #the average profits for all of the members will be calculated after the trade(s) are added
    
    def _update_stock_database(self, tick, tradeType):
        pass
        if tradeType == "BUY":
            score = 1
        else: 
            score = -1
        #if tick is not in stockDatabase create a new row
            #self._createStock(tick)
        #get the current score 
        #add tradeID to database list
        #update buy score

    def _create_stock(self, tick):
        pass
        #SQL

    def _refresh_member_databases(self):
        pass
        #for each member
            #self._refresh_member_database(member)
            #self._refresh_DB_of_members(member)

    def _refresh_member_database(self, member):
        pass
        #for each trade
            #if owned == True get the new % profits

    def _refresh_DB_of_members(self, memner):
        pass
        #get the new average %s for each member

    def _make_table_name(self, memName):
        space = memName.index(" ")
        n = memName.replace(" ", "")
        return n[space:] + n[:space]


        
